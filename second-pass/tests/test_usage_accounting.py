import json
import os
import socket
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest import mock

from tools import pipeline_contract
from tools import usage_accounting


TOKEN_FIELDS = (
    "input_tokens",
    "cached_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
    "total_tokens",
)


def counters(
    total: int,
    *,
    input_tokens: int | None = None,
    cached_input_tokens: int = 0,
    output_tokens: int | None = None,
    reasoning_output_tokens: int = 0,
) -> dict[str, int]:
    return {
        "input_tokens": total if input_tokens is None else input_tokens,
        "cached_input_tokens": cached_input_tokens,
        "output_tokens": total if output_tokens is None else output_tokens,
        "reasoning_output_tokens": reasoning_output_tokens,
        "total_tokens": total,
    }


class UsageAccountingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write_trace(
        self,
        totals: list[dict[str, int]],
        *,
        relative: str = "2026/07/24/rollout.jsonl",
    ) -> Path:
        trace = self.root / "trace"
        rollout = trace / relative
        rollout.parent.mkdir(parents=True, exist_ok=True)
        events = [
            {
                "type": "event_msg",
                "payload": {
                    "type": "token_count",
                    "info": {"total_token_usage": total},
                },
            }
            for total in totals
        ]
        rollout.write_text("".join(json.dumps(item) + "\n" for item in events))
        return trace

    def test_uses_terminal_cumulative_count_and_computes_delta(self) -> None:
        trace = self.write_trace(
            [
                {
                    "input_tokens": 100,
                    "cached_input_tokens": 40,
                    "output_tokens": 20,
                    "reasoning_output_tokens": 8,
                    "total_tokens": 120,
                },
                {
                    "input_tokens": 180,
                    "cached_input_tokens": 70,
                    "output_tokens": 35,
                    "reasoning_output_tokens": 12,
                    "total_tokens": 215,
                },
            ]
        )

        document = usage_accounting.extract_trace_usage(
            trace,
            previous_cumulative={
                "input_tokens": 100,
                "cached_input_tokens": 40,
                "output_tokens": 20,
                "reasoning_output_tokens": 8,
                "total_tokens": 120,
            },
        )

        self.assertEqual(document["status"], "COMPLETE")
        self.assertEqual(document["cumulative"]["total_tokens"], 215)
        self.assertEqual(document["invocation_delta"]["total_tokens"], 95)
        self.assertEqual(document["invocation_delta"]["cached_input_tokens"], 30)
        self.assertEqual(
            document["selected_event"],
            {
                "relative_path": "2026/07/24/rollout.jsonl",
                "line_number": 2,
            },
        )

    def test_first_invocation_uses_zero_previous_counters(self) -> None:
        trace = self.write_trace([counters(12, cached_input_tokens=2)])

        document = usage_accounting.extract_trace_usage(trace)

        self.assertEqual(
            document["previous_cumulative"],
            dict.fromkeys(TOKEN_FIELDS, 0),
        )
        self.assertEqual(
            document["invocation_delta"],
            counters(12, cached_input_tokens=2),
        )

    def test_selects_last_token_event_in_lexical_file_order(self) -> None:
        trace = self.write_trace(
            [counters(10)],
            relative="2026/07/24/a.jsonl",
        )
        later = trace / "2026/07/24/z.jsonl"
        later.write_text(
            "\n"
            + json.dumps({"type": "event_msg", "payload": {}})
            + "\n"
            + json.dumps(
                {
                    "type": "event_msg",
                    "payload": {
                        "type": "token_count",
                        "info": {"total_token_usage": counters(15)},
                    },
                }
            )
            + "\n"
        )

        document = usage_accounting.extract_trace_usage(trace)

        self.assertEqual(document["cumulative"]["total_tokens"], 15)
        self.assertEqual(
            document["selected_event"],
            {"relative_path": "2026/07/24/z.jsonl", "line_number": 3},
        )

    def test_sums_terminal_counters_for_root_and_subagent_sessions(self) -> None:
        trace = self.root / "trace"
        trace.mkdir()
        root_id = str(uuid.uuid4())
        child_id = str(uuid.uuid4())

        def write_session(name: str, session_id: str, total: int) -> None:
            (trace / name).write_text(
                json.dumps(
                    {
                        "type": "session_meta",
                        "payload": {"id": session_id},
                    }
                )
                + "\n"
                + json.dumps(
                    {
                        "type": "event_msg",
                        "payload": {
                            "type": "token_count",
                            "info": {
                                "total_token_usage": counters(total)
                            },
                        },
                    }
                )
                + "\n"
            )

        write_session("root.jsonl", root_id, 100)
        write_session("subagent.jsonl", child_id, 15)

        document = usage_accounting.extract_trace_usage(
            trace,
            previous_cumulative=counters(80),
        )

        self.assertEqual(document["cumulative"], counters(115))
        self.assertEqual(document["invocation_delta"], counters(35))
        self.assertEqual(
            {item["session_id"] for item in document["session_events"]},
            {root_id, child_id},
        )

    def test_missing_token_events_are_explicit_not_fatal(self) -> None:
        trace = self.root / "trace"
        trace.mkdir()
        (trace / "rollout.jsonl").write_text(
            '{"type":"event_msg","payload":{}}\n'
        )

        document = usage_accounting.extract_trace_usage(trace)

        self.assertEqual(document["status"], "MISSING")
        self.assertIsNone(document["cumulative"])
        self.assertIsNone(document["selected_event"])
        self.assertIsNone(document["invocation_delta"])
        self.assertEqual(
            document["monetary_cost"]["status"],
            "UNAVAILABLE",
        )

    def test_ignores_token_count_events_without_usage_info(self) -> None:
        trace = self.write_trace([counters(12, cached_input_tokens=2)])
        rollout = trace / "2026/07/24/rollout.jsonl"
        rollout.write_text(
            json.dumps(
                {
                    "type": "event_msg",
                    "payload": {
                        "type": "token_count",
                        "info": None,
                        "rate_limits": {"plan_type": "pro"},
                    },
                }
            )
            + "\n"
            + rollout.read_text()
        )

        document = usage_accounting.extract_trace_usage(trace)

        self.assertEqual(document["status"], "COMPLETE")
        self.assertEqual(document["cumulative"], counters(12, cached_input_tokens=2))
        self.assertEqual(
            document["selected_event"],
            {
                "relative_path": "2026/07/24/rollout.jsonl",
                "line_number": 2,
            },
        )

    def test_rejects_counter_regression(self) -> None:
        trace = self.write_trace(
            [
                {
                    "input_tokens": 10,
                    "cached_input_tokens": 5,
                    "output_tokens": 2,
                    "reasoning_output_tokens": 1,
                    "total_tokens": 12,
                }
            ]
        )

        with self.assertRaisesRegex(
            usage_accounting.UsageAccountingError,
            "regressed",
        ):
            usage_accounting.extract_trace_usage(
                trace,
                previous_cumulative={
                    "input_tokens": 11,
                    "cached_input_tokens": 5,
                    "output_tokens": 2,
                    "reasoning_output_tokens": 1,
                    "total_tokens": 13,
                },
            )

    def test_rejects_malformed_json_and_counters(self) -> None:
        cases: tuple[tuple[str, object, str], ...] = (
            ("not-object", [], "token counters must be an object"),
            ("missing", {"total_tokens": 1}, "input_tokens"),
            (
                "boolean",
                {**counters(1), "input_tokens": True},
                "input_tokens",
            ),
            (
                "negative",
                {**counters(1), "total_tokens": -1},
                "total_tokens",
            ),
            (
                "cached-category",
                counters(5, input_tokens=2, cached_input_tokens=3),
                "cached input exceeds input tokens",
            ),
            (
                "reasoning-category",
                counters(5, output_tokens=2, reasoning_output_tokens=3),
                "reasoning output exceeds output tokens",
            ),
        )
        for name, value, message in cases:
            with self.subTest(name=name):
                case_root = self.root / name
                trace = case_root / "trace"
                trace.mkdir(parents=True)
                event = {
                    "type": "event_msg",
                    "payload": {
                        "type": "token_count",
                        "info": {"total_token_usage": value},
                    },
                }
                (trace / "rollout.jsonl").write_text(json.dumps(event) + "\n")
                with self.assertRaisesRegex(
                    usage_accounting.UsageAccountingError,
                    message,
                ):
                    usage_accounting.extract_trace_usage(trace)

        malformed = self.root / "malformed-json"
        malformed.mkdir()
        (malformed / "rollout.jsonl").write_text("{not json}\n")
        with self.assertRaisesRegex(
            usage_accounting.UsageAccountingError,
            "malformed JSON",
        ):
            usage_accounting.extract_trace_usage(malformed)

    def test_rejects_linked_or_unsupported_trace_entries(self) -> None:
        trace = self.root / "trace"
        trace.mkdir()
        outside = self.root / "outside.jsonl"
        outside.write_text("{}\n")
        os.symlink(outside, trace / "rollout.jsonl")

        with self.assertRaisesRegex(
            usage_accounting.UsageAccountingError,
            "linked or unsupported",
        ):
            usage_accounting.extract_trace_usage(trace)

    def test_tree_hash_matches_pipeline_contract(self) -> None:
        trace = self.root / "trace"
        (trace / "empty").mkdir(parents=True)
        (trace / "nested").mkdir()
        (trace / "nested/data.jsonl").write_bytes(b"first\nsecond\n")
        (trace / "root.jsonl").write_bytes(b"root\n")

        self.assertEqual(
            usage_accounting.sha256_tree(trace),
            pipeline_contract.sha256_tree(trace),
        )

    def test_write_trace_usage_publishes_stable_json_atomically(self) -> None:
        trace = self.write_trace([counters(9)])
        destination = self.root / "output/usage.json"
        calls: list[str] = []
        real_fsync = os.fsync
        real_replace = os.replace

        def tracked_fsync(descriptor: int) -> None:
            calls.append("fsync")
            real_fsync(descriptor)

        def tracked_replace(source: str | Path, target: str | Path) -> None:
            calls.append("replace")
            real_replace(source, target)

        with (
            mock.patch.object(os, "fsync", side_effect=tracked_fsync),
            mock.patch.object(os, "replace", side_effect=tracked_replace),
        ):
            document = usage_accounting.write_trace_usage(trace, destination)

        self.assertEqual(json.loads(destination.read_text()), document)
        self.assertTrue(destination.read_text().endswith("\n"))
        self.assertEqual(calls, ["fsync", "replace"])
        self.assertEqual(
            sorted(path.name for path in destination.parent.iterdir()),
            ["usage.json"],
        )


class UsageAggregationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.run = Path(self.temporary.name) / "run"
        self.run.mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def execution(
        self,
        problem: str,
        stage: str,
        collection: str,
        name: str,
    ) -> Path:
        path = self.run / "tasks" / problem / stage / collection / name
        path.mkdir(parents=True)
        return path

    def write_usage(
        self,
        execution: Path,
        delta: dict[str, int],
        *,
        previous: dict[str, int] | None = None,
    ) -> None:
        previous = (
            dict.fromkeys(TOKEN_FIELDS, 0)
            if previous is None
            else previous
        )
        cumulative = {
            name: previous[name] + delta[name]
            for name in TOKEN_FIELDS
        }
        document = {
            "schema_version": 2,
            "status": "COMPLETE",
            "source_trace_sha256": "0" * 64,
            "selected_event": {
                "relative_path": "rollout.jsonl",
                "line_number": 1,
            },
            "cumulative": cumulative,
            "previous_cumulative": previous,
            "invocation_delta": delta,
            "monetary_cost": usage_accounting.MONETARY_COST_UNAVAILABLE,
        }
        (execution / "usage.json").write_text(
            json.dumps(document, sort_keys=True) + "\n"
        )

    def test_aggregates_exact_stage_shapes_tokens_and_runtime(self) -> None:
        stage1 = self.execution(
            "p1", "01-k-proof", "invocations", "001-initial"
        )
        self.write_usage(
            stage1,
            counters(
                12,
                input_tokens=10,
                cached_input_tokens=4,
                output_tokens=2,
                reasoning_output_tokens=1,
            ),
        )
        (stage1 / "metrics.json").write_text('{"duration_s":7}\n')
        (stage1 / "runtime-metrics.json").write_text(
            '{"start_epoch":10,"end_epoch":17,"duration_s":7}\n'
        )

        stage2 = self.execution("p1", "02-k-audit", "executions", "001")
        (stage2 / "usage.json").write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "status": "MISSING",
                    "source_trace_sha256": "0" * 64,
                    "selected_event": None,
                    "cumulative": None,
                    "previous_cumulative": dict.fromkeys(TOKEN_FIELDS, 0),
                    "invocation_delta": None,
                    "monetary_cost": usage_accounting.MONETARY_COST_UNAVAILABLE,
                }
            )
            + "\n"
        )
        (stage2 / "metrics.json").write_text(
            '{"start_epoch":20,"end_epoch":25,"duration_s":5}\n'
        )

        stage3 = self.execution(
            "p1", "03-lemma-discovery", "invocations", "001-initial"
        )
        self.write_usage(
            stage3,
            counters(
                5,
                input_tokens=4,
                cached_input_tokens=2,
                output_tokens=1,
            ),
        )
        (stage3 / "metrics.json").write_text('{"duration_s":6}\n')

        stage5 = self.execution(
            "p2", "05-lean-proof", "invocations", "001-initial"
        )
        (stage5 / "usage.json").write_text("{not json}\n")
        (stage5 / "metrics.json").write_text('{"duration_s":10}\n')
        (stage5 / "legacy-metrics.json").write_text(
            '{"start_epoch":30,"end_epoch":40,"duration_s":10}\n'
        )

        stage6 = self.execution("p2", "06-lean-audit", "executions", "001")
        self.write_usage(
            stage6,
            counters(
                3,
                input_tokens=2,
                cached_input_tokens=1,
                output_tokens=1,
                reasoning_output_tokens=1,
            ),
        )
        (stage6 / "metrics.json").write_text('{"duration_s":2}\n')

        no_usage = self.execution("p3", "02-k-audit", "executions", "001")
        (no_usage / "metrics.json").write_text('{"duration_s":4}\n')

        ignored = self.execution(
            "p1", "04-klean-generation", "invocations", "001"
        )
        self.write_usage(ignored, counters(999))
        (ignored / "metrics.json").write_text('{"duration_s":999}\n')

        document = usage_accounting.aggregate_usage_documents(self.run)

        self.assertEqual(document["totals"]["total_tokens"], 20)
        self.assertEqual(document["totals"]["cached_input_tokens"], 7)
        self.assertEqual(
            document["stage_subtotals"]["01-k-proof"]["total_tokens"],
            12,
        )
        self.assertEqual(
            document["stage_subtotals"]["03-lemma-discovery"]["total_tokens"],
            5,
        )
        self.assertEqual(
            document["stage_subtotals"]["06-lean-audit"]["total_tokens"],
            3,
        )
        self.assertEqual(
            list(document["stage_subtotals"]),
            [
                "01-k-proof",
                "02-k-audit",
                "03-lemma-discovery",
                "05-lean-proof",
                "06-lean-audit",
            ],
        )
        self.assertEqual(
            document["task_subtotals"]["p1"]["total_tokens"],
            17,
        )
        self.assertEqual(
            document["task_subtotals"]["p2"]["total_tokens"],
            3,
        )
        self.assertEqual(document["runtime"]["agent_seconds"], 34)
        self.assertEqual(document["runtime"]["earliest_start_epoch"], 10)
        self.assertEqual(document["runtime"]["latest_end_epoch"], 40)
        self.assertEqual(document["runtime"]["wall_clock_span_seconds"], 30)
        self.assertEqual(
            document["runtime"]["stage_agent_seconds"]["02-k-audit"],
            9,
        )
        self.assertEqual(document["runtime"]["task_agent_seconds"]["p2"], 12)
        self.assertEqual(
            document["missing_observations"],
            [
                "tasks/p1/02-k-audit/executions/001/usage.json",
                "tasks/p3/02-k-audit/executions/001/usage.json",
            ],
        )
        self.assertEqual(
            [
                item["relative_path"]
                for item in document["malformed_observations"]
            ],
            ["tasks/p2/05-lean-proof/invocations/001-initial/usage.json"],
        )
        self.assertEqual(
            document["monetary_cost"],
            usage_accounting.MONETARY_COST_UNAVAILABLE,
        )

    def test_delta_categories_are_summed_without_recombination(self) -> None:
        first = self.execution(
            "p1", "01-k-proof", "invocations", "001-initial"
        )
        second = self.execution(
            "p1", "03-lemma-discovery", "invocations", "001-initial"
        )
        self.write_usage(
            first,
            counters(
                100,
                input_tokens=90,
                cached_input_tokens=80,
                output_tokens=10,
                reasoning_output_tokens=9,
            ),
        )
        self.write_usage(
            second,
            counters(
                7,
                input_tokens=3,
                cached_input_tokens=2,
                output_tokens=4,
                reasoning_output_tokens=1,
            ),
            previous=counters(
                100,
                input_tokens=90,
                cached_input_tokens=80,
                output_tokens=10,
                reasoning_output_tokens=9,
            ),
        )

        document = usage_accounting.aggregate_usage_documents(self.run)

        self.assertEqual(
            document["totals"],
            {
                "input_tokens": 93,
                "cached_input_tokens": 82,
                "output_tokens": 14,
                "reasoning_output_tokens": 10,
                "total_tokens": 107,
            },
        )

    def test_write_run_summary_publishes_usage_summary(self) -> None:
        execution = self.execution(
            "p1", "01-k-proof", "invocations", "001-initial"
        )
        self.write_usage(execution, counters(4))

        document = usage_accounting.write_run_summary(self.run)

        self.assertEqual(
            json.loads((self.run / "usage-summary.json").read_text()),
            document,
        )

    def test_rejects_broken_link_at_an_exact_stage_collection(self) -> None:
        stage = self.run / "tasks/p1/01-k-proof"
        stage.mkdir(parents=True)
        os.symlink(
            self.run / "missing-invocations",
            stage / "invocations",
        )

        with self.assertRaisesRegex(
            usage_accounting.UsageAccountingError,
            "must be a real directory",
        ):
            usage_accounting.aggregate_usage_documents(self.run)

    def test_rejects_linked_stage_before_following_its_collection(self) -> None:
        outside_stage = Path(self.temporary.name) / "outside-stage"
        execution = outside_stage / "invocations/001-initial"
        execution.mkdir(parents=True)
        self.write_usage(execution, counters(99))
        task = self.run / "tasks/p1"
        task.mkdir(parents=True)
        os.symlink(outside_stage, task / "01-k-proof")

        with self.assertRaisesRegex(
            usage_accounting.UsageAccountingError,
            "must be a real directory",
        ):
            usage_accounting.aggregate_usage_documents(self.run)

    def test_rejects_special_entries_at_the_task_boundary(self) -> None:
        for kind in ("fifo", "socket"):
            with self.subTest(kind=kind):
                with tempfile.TemporaryDirectory(dir=self.temporary.name) as case:
                    run = Path(case) / "run"
                    tasks = run / "tasks"
                    tasks.mkdir(parents=True)
                    special = tasks / "p1"
                    if kind == "fifo":
                        os.mkfifo(special)
                    else:
                        endpoint = socket.socket(socket.AF_UNIX)
                        try:
                            endpoint.bind(str(special))
                        finally:
                            endpoint.close()

                    with self.assertRaisesRegex(
                        usage_accounting.UsageAccountingError,
                        "linked or unsupported task",
                    ):
                        usage_accounting.aggregate_usage_documents(run)

    def test_rejects_special_entries_in_execution_collections(self) -> None:
        for kind in ("fifo", "socket"):
            with self.subTest(kind=kind):
                with tempfile.TemporaryDirectory(dir=self.temporary.name) as case:
                    run = Path(case) / "run"
                    collection = (
                        run
                        / "tasks/p1/01-k-proof/invocations"
                    )
                    collection.mkdir(parents=True)
                    special = collection / "001-initial"
                    if kind == "fifo":
                        os.mkfifo(special)
                    else:
                        endpoint = socket.socket(socket.AF_UNIX)
                        try:
                            endpoint.bind(str(special))
                        finally:
                            endpoint.close()

                    with self.assertRaisesRegex(
                        usage_accounting.UsageAccountingError,
                        "linked or unsupported execution",
                    ):
                        usage_accounting.aggregate_usage_documents(run)

    def test_rejects_special_exact_stage_and_collection_paths(self) -> None:
        cases = (
            ("stage", "tasks/p1/01-k-proof"),
            ("collection", "tasks/p1/01-k-proof/invocations"),
        )
        for name, relative in cases:
            with self.subTest(name=name):
                with tempfile.TemporaryDirectory(dir=self.temporary.name) as case:
                    run = Path(case) / "run"
                    special = run / relative
                    special.parent.mkdir(parents=True)
                    os.mkfifo(special)

                    with self.assertRaisesRegex(
                        usage_accounting.UsageAccountingError,
                        "must be a real directory",
                    ):
                        usage_accounting.aggregate_usage_documents(run)

    def test_complete_usage_schema_and_delta_consistency_are_required(self) -> None:
        execution = self.execution(
            "p1", "01-k-proof", "invocations", "001-initial"
        )
        (execution / "usage.json").write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "status": "COMPLETE",
                    "invocation_delta": counters(7),
                }
            )
            + "\n"
        )

        document = usage_accounting.aggregate_usage_documents(self.run)

        self.assertEqual(document["totals"], dict.fromkeys(TOKEN_FIELDS, 0))
        self.assertRegex(
            document["malformed_observations"][0]["error"],
            "source_trace_sha256",
        )

        self.write_usage(execution, counters(7))
        usage = json.loads((execution / "usage.json").read_text())
        usage["invocation_delta"]["total_tokens"] = 6
        (execution / "usage.json").write_text(json.dumps(usage) + "\n")

        document = usage_accounting.aggregate_usage_documents(self.run)

        self.assertRegex(
            document["malformed_observations"][0]["error"],
            "does not match",
        )

    def test_runtime_observations_distinguish_missing_from_malformed(self) -> None:
        empty_metrics = self.execution(
            "p1", "01-k-proof", "invocations", "001-initial"
        )
        self.write_usage(empty_metrics, counters(1))
        (empty_metrics / "metrics.json").write_text("{}\n")

        malformed_metrics = self.execution(
            "p2", "01-k-proof", "invocations", "001-initial"
        )
        self.write_usage(malformed_metrics, counters(1))
        (malformed_metrics / "metrics.json").write_text("{not json}\n")

        no_metrics = self.execution(
            "p3", "01-k-proof", "invocations", "001-initial"
        )
        self.write_usage(no_metrics, counters(1))

        document = usage_accounting.aggregate_usage_documents(self.run)

        self.assertEqual(
            document["missing_runtime_observations"],
            ["tasks/p3/01-k-proof/invocations/001-initial"],
        )
        self.assertEqual(
            {
                item["relative_path"]
                for item in document["malformed_runtime_observations"]
            },
            {
                "tasks/p1/01-k-proof/invocations/001-initial/metrics.json",
                "tasks/p2/01-k-proof/invocations/001-initial/metrics.json",
            },
        )


class UsageCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.repo = Path(__file__).resolve().parents[1]

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "tools.usage_accounting", *arguments],
            cwd=self.repo,
            check=False,
            capture_output=True,
            text=True,
        )

    def write_trace(self, total: int) -> Path:
        trace = self.root / "trace"
        trace.mkdir()
        event = {
            "type": "event_msg",
            "payload": {
                "type": "token_count",
                "info": {"total_token_usage": counters(total)},
            },
        }
        (trace / "rollout.jsonl").write_text(json.dumps(event) + "\n")
        return trace

    def test_write_uses_previous_document_and_prints_result(self) -> None:
        trace = self.write_trace(20)
        previous = self.root / "previous.json"
        previous.write_text(
            json.dumps({"cumulative": counters(12)}) + "\n"
        )
        output = self.root / "usage.json"

        result = self.run_cli(
            "write",
            "--trace",
            str(trace),
            "--output",
            str(output),
            "--previous",
            str(previous),
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), json.loads(output.read_text()))
        self.assertEqual(
            json.loads(result.stdout)["invocation_delta"]["total_tokens"],
            8,
        )

    def test_summarize_writes_run_summary(self) -> None:
        run = self.root / "run"
        run.mkdir()

        result = self.run_cli("summarize", "--run", str(run))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            json.loads((run / "usage-summary.json").read_text()),
        )

    def test_validation_failure_is_concise_and_exits_two(self) -> None:
        trace = self.root / "missing"

        result = self.run_cli(
            "write",
            "--trace",
            str(trace),
            "--output",
            str(self.root / "usage.json"),
        )

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertTrue(result.stderr.startswith("usage accounting error:"))
        self.assertEqual(len(result.stderr.splitlines()), 1)

    def test_argument_validation_is_concise_and_exits_two(self) -> None:
        result = self.run_cli("write", "--trace", str(self.root / "trace"))

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertTrue(result.stderr.startswith("usage accounting error:"))
        self.assertEqual(len(result.stderr.splitlines()), 1)
