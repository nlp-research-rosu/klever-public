import fcntl
import json
import os
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest import mock

from tests.test_pipeline_layout import PipelineLayoutFixture
from tools import pipeline_contract, usage_accounting


class PipelineStateFixture(PipelineLayoutFixture):
    def setUp(self) -> None:
        super().setUp()
        self.run_id = "state-run"
        pipeline_contract.create_run(
            self.repo,
            run_id=self.run_id,
            config="codex-gpt-5.6-sol-xhigh-kit-semantics",
            problem_ids=[self.PROBLEM],
        )
        self.task = self.repo / f"runs/{self.run_id}/tasks/{self.PROBLEM}"
        self.state = self.repo / f"runner-state/{self.run_id}/{self.PROBLEM}"
        self.session_id = str(uuid.uuid4())

    def write_trace(
        self,
        invocation: Path,
        session_ids: list[str] | None = None,
        *,
        linked: bool = False,
        total_tokens: int | None = None,
    ) -> None:
        trace = invocation / "codex-trace/2026/07/23"
        trace.mkdir(parents=True)
        rollout = trace / "rollout.jsonl"
        lines = [
            json.dumps(
                {
                    "type": "session_meta",
                    "payload": {"id": value},
                }
            )
            for value in (session_ids if session_ids is not None else [self.session_id])
        ]
        if total_tokens is not None:
            lines.append(
                json.dumps(
                    {
                        "type": "event_msg",
                        "payload": {
                            "type": "token_count",
                            "info": {
                                "total_token_usage": {
                                    "input_tokens": total_tokens,
                                    "cached_input_tokens": 0,
                                    "output_tokens": 0,
                                    "reasoning_output_tokens": 0,
                                    "total_tokens": total_tokens,
                                }
                            },
                        },
                    }
                )
            )
        if linked:
            target = invocation / "outside.jsonl"
            target.write_text("\n".join(lines) + "\n")
            os.symlink(target, rollout)
        else:
            rollout.write_text("\n".join(lines) + "\n")


class SessionTraceTests(PipelineStateFixture):
    def test_extracts_exactly_one_session_uuid(self) -> None:
        invocation = self.task / "01-k-proof/invocations/trace"
        invocation.mkdir()
        self.write_trace(invocation)

        self.assertEqual(
            pipeline_contract.extract_session_uuid(invocation / "codex-trace"),
            self.session_id,
        )

    def test_rejects_missing_multiple_malformed_and_linked_session_traces(self) -> None:
        cases = (
            ("missing", [], False),
            ("multiple", [self.session_id, str(uuid.uuid4())], False),
            ("malformed", ["not-a-uuid"], False),
            ("linked", [self.session_id], True),
        )
        for name, session_ids, linked in cases:
            with self.subTest(name=name):
                invocation = self.task / f"01-k-proof/invocations/{name}"
                invocation.mkdir()
                self.write_trace(invocation, session_ids, linked=linked)
                with self.assertRaises(pipeline_contract.PipelineContractError):
                    pipeline_contract.extract_session_uuid(
                        invocation / "codex-trace"
                    )

    def test_validates_subagent_trace_tree_rooted_at_expected_session(self) -> None:
        invocation = self.task / "01-k-proof/invocations/subagent-tree"
        trace = invocation / "codex-trace"
        trace.mkdir(parents=True)
        child_id = str(uuid.uuid4())
        trace.joinpath("root.jsonl").write_text(
            json.dumps(
                {
                    "type": "session_meta",
                    "payload": {"id": self.session_id},
                }
            )
            + "\n"
        )
        trace.joinpath("child.jsonl").write_text(
            json.dumps(
                {
                    "type": "session_meta",
                    "payload": {
                        "id": child_id,
                        "parent_thread_id": self.session_id,
                        "source": {
                            "subagent": {
                                "thread_spawn": {
                                    "parent_thread_id": self.session_id,
                                    "depth": 1,
                                }
                            }
                        },
                    },
                }
            )
            + "\n"
        )

        self.assertEqual(
            pipeline_contract.validate_session_trace_tree(
                trace, self.session_id
            ),
            self.session_id,
        )

    def test_rejects_unrooted_or_falsely_linked_subagent_trace(self) -> None:
        cases = (
            ("unrooted", None, None),
            ("mismatched-source-parent", self.session_id, str(uuid.uuid4())),
        )
        for name, parent_id, source_parent_id in cases:
            with self.subTest(name=name):
                invocation = self.task / f"01-k-proof/invocations/{name}"
                trace = invocation / "codex-trace"
                trace.mkdir(parents=True)
                child_id = str(uuid.uuid4())
                events = [
                    {
                        "type": "session_meta",
                        "payload": {"id": self.session_id},
                    },
                    {
                        "type": "session_meta",
                        "payload": {
                            "id": child_id,
                            "parent_thread_id": parent_id,
                            "source": {
                                "subagent": {
                                    "thread_spawn": {
                                        "parent_thread_id": source_parent_id,
                                        "depth": 1,
                                    }
                                }
                            },
                        },
                    },
                ]
                trace.joinpath("rollout.jsonl").write_text(
                    "\n".join(json.dumps(event) for event in events) + "\n"
                )
                with self.assertRaises(
                    pipeline_contract.PipelineContractError
                ):
                    pipeline_contract.validate_session_trace_tree(
                        trace, self.session_id
                    )


class InvocationStateTests(PipelineStateFixture):
    BWRAP_NAMESPACE_ERROR = (
        "bwrap: No permissions to create a new namespace, likely because "
        "the kernel does not allow non-privileged user namespaces."
    )

    def prepare(self, stage: str = "01-k-proof") -> pipeline_contract.Invocation:
        return pipeline_contract.prepare_invocation(
            self.repo, self.run_id, self.PROBLEM, stage
        )

    def finalize(
        self,
        invocation: pipeline_contract.Invocation,
        *,
        exit_code: int,
        duration_s: int = 7,
        timeout_marker: bool = False,
        oom_killed: bool = False,
    ) -> dict[str, object]:
        if (
            invocation.kind == "initial"
            and not (invocation.path / "codex-trace").exists()
        ):
            self.write_trace(invocation.path)
        return pipeline_contract.finalize_invocation(
            self.repo,
            self.run_id,
            self.PROBLEM,
            invocation.stage,
            invocation.name,
            exit_code=exit_code,
            duration_s=duration_s,
            timeout_marker=timeout_marker,
            oom_killed=oom_killed,
            image_id="sha256:test-image",
        )

    def test_prepares_initial_and_finalizes_exit_zero(self) -> None:
        invocation = self.prepare()
        self.assertEqual(invocation.name, "001-initial")
        self.assertEqual(invocation.kind, "initial")
        self.assertEqual(invocation.allocation_s, 3600)

        result = self.finalize(invocation, exit_code=0)

        self.assertEqual(result["status"], "SUCCEEDED")
        self.assertEqual(result["session_id"], self.session_id)
        self.assertEqual(result["cumulative_duration_s"], 7)
        persisted = json.loads((self.state / "session.json").read_text())
        self.assertEqual(persisted["session_id"], self.session_id)
        self.assertEqual(persisted["codex_home_relative"], "codex-home")
        self.assertTrue((self.task / "01-k-proof/result.json").is_file())

    def test_finalization_publishes_prevalidated_result_metadata_once(
        self,
    ) -> None:
        invocation = self.prepare()
        metadata = {
            "review_context": {
                "rule_count": 1,
            },
        }
        self.write_trace(invocation.path)

        result = pipeline_contract.finalize_invocation(
            self.repo,
            self.run_id,
            self.PROBLEM,
            invocation.stage,
            invocation.name,
            exit_code=0,
            duration_s=7,
            timeout_marker=False,
            oom_killed=False,
            image_id="sha256:test-image",
            result_metadata=metadata,
        )

        persisted_invocation = json.loads(
            (invocation.path / "invocation.json").read_text()
        )
        persisted_result = json.loads(
            (
                self.task
                / invocation.stage
                / "result.json"
            ).read_text()
        )
        for document in (result, persisted_result, persisted_invocation):
            self.assertEqual(
                {
                    key: document[key]
                    for key in metadata
                },
                metadata,
            )

    def test_trust_boundary_metadata_requires_expected_evidence(
        self,
    ) -> None:
        stage1 = self.prepare()
        self.write_trace(stage1.path)
        self.finalize(stage1, exit_code=0)
        invocation = self.prepare("03-lemma-discovery")
        self.write_trace(invocation.path)
        evidence = invocation.path / "validated-trust-boundary.json"
        evidence.write_text('{"validated": true}\n')
        digest = pipeline_contract.sha256_file(evidence)

        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError,
            "trust-boundary metadata",
        ):
            pipeline_contract.finalize_invocation(
                self.repo,
                self.run_id,
                self.PROBLEM,
                invocation.stage,
                invocation.name,
                exit_code=0,
                duration_s=7,
                timeout_marker=False,
                oom_killed=False,
                image_id="sha256:test-image",
                result_metadata={
                    "trust_boundary_sha256": digest,
                    "trust_boundary_artifact": (
                        "invocations/001-initial/"
                        "validated-trust-boundary.json"
                    ),
                },
            )

        persisted = json.loads(
            (invocation.path / "invocation.json").read_text()
        )
        self.assertEqual(persisted["status"], "PREPARED")
        self.assertFalse(
            (self.task / "03-lemma-discovery/result.json").exists()
        )

    def test_prepublication_guard_failure_writes_no_terminal_record(
        self,
    ) -> None:
        stage1 = self.prepare()
        self.write_trace(stage1.path)
        self.finalize(stage1, exit_code=0)
        invocation = self.prepare("03-lemma-discovery")
        self.write_trace(invocation.path)

        def reject_publication() -> None:
            raise pipeline_contract.PipelineContractError(
                "late integrity failure"
            )

        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError,
            "late integrity failure",
        ):
            pipeline_contract.finalize_invocation(
                self.repo,
                self.run_id,
                self.PROBLEM,
                invocation.stage,
                invocation.name,
                exit_code=0,
                duration_s=7,
                timeout_marker=False,
                oom_killed=False,
                image_id="sha256:test-image",
                prepublication_guard=reject_publication,
            )

        persisted = json.loads(
            (invocation.path / "invocation.json").read_text()
        )
        self.assertEqual(persisted["status"], "PREPARED")
        self.assertFalse(
            (self.task / "03-lemma-discovery/result.json").exists()
        )
        self.assertFalse((invocation.path / "metrics.json").exists())

    def test_expected_evidence_mismatch_writes_no_terminal_record(
        self,
    ) -> None:
        stage1 = self.prepare()
        self.write_trace(stage1.path)
        self.finalize(stage1, exit_code=0)
        invocation = self.prepare("03-lemma-discovery")
        self.write_trace(invocation.path)
        evidence = invocation.path / "validated-trust-boundary.json"
        evidence.write_text('{"validated": true}\n')

        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError,
            "expected invocation evidence",
        ):
            pipeline_contract.finalize_invocation(
                self.repo,
                self.run_id,
                self.PROBLEM,
                invocation.stage,
                invocation.name,
                exit_code=0,
                duration_s=7,
                timeout_marker=False,
                oom_killed=False,
                image_id="sha256:test-image",
                expected_evidence={
                    "validated-trust-boundary.json": "0" * 64,
                },
            )

        persisted = json.loads(
            (invocation.path / "invocation.json").read_text()
        )
        self.assertEqual(persisted["status"], "PREPARED")
        self.assertFalse(
            (self.task / "03-lemma-discovery/result.json").exists()
        )
        self.assertFalse((invocation.path / "metrics.json").exists())

    def test_expected_evidence_is_consistent_across_terminal_records(
        self,
    ) -> None:
        stage1 = self.prepare()
        self.write_trace(stage1.path)
        self.finalize(stage1, exit_code=0)
        invocation = self.prepare("03-lemma-discovery")
        self.write_trace(invocation.path)
        evidence = invocation.path / "validated-trust-boundary.json"
        evidence.write_text('{"validated": true}\n')
        digest = pipeline_contract.sha256_file(evidence)
        metadata = {
            "trust_boundary_sha256": digest,
            "trust_boundary_artifact": (
                "invocations/001-initial/validated-trust-boundary.json"
            ),
        }

        result = pipeline_contract.finalize_invocation(
            self.repo,
            self.run_id,
            self.PROBLEM,
            invocation.stage,
            invocation.name,
            exit_code=0,
            duration_s=7,
            timeout_marker=False,
            oom_killed=False,
            image_id="sha256:test-image",
            result_metadata=metadata,
            expected_evidence={
                "validated-trust-boundary.json": digest,
            },
        )

        persisted_invocation = json.loads(
            (invocation.path / "invocation.json").read_text()
        )
        persisted_result = json.loads(
            (
                self.task
                / invocation.stage
                / "result.json"
            ).read_text()
        )
        for document in (result, persisted_result, persisted_invocation):
            self.assertEqual(document["trust_boundary_sha256"], digest)
            self.assertEqual(
                document["outputs"]["evidence"][
                    "validated-trust-boundary.json"
                ],
                digest,
            )

    def test_finalize_preserves_raw_metrics_and_writes_usage(self) -> None:
        invocation = self.prepare()
        raw_metrics = {
            "start_epoch": 10,
            "end_epoch": 17,
            "duration_s": 7,
            "mem_peak_bytes": 1234,
        }
        (invocation.path / "metrics.json").write_text(
            json.dumps(raw_metrics) + "\n"
        )
        self.write_trace(invocation.path, total_tokens=120)

        result = self.finalize(invocation, exit_code=0, duration_s=7)

        self.assertEqual(
            json.loads(
                (invocation.path / "runtime-metrics.json").read_text()
            ),
            raw_metrics,
        )
        usage = json.loads((invocation.path / "usage.json").read_text())
        self.assertEqual(usage["invocation_delta"]["total_tokens"], 120)
        self.assertIn("runtime-metrics.json", result["outputs"]["evidence"])
        self.assertIn("usage.json", result["outputs"]["evidence"])

    def test_later_model_stages_subtract_prior_same_session_cumulative(
        self,
    ) -> None:
        stage1 = self.prepare()
        self.write_trace(stage1.path, total_tokens=120)
        self.finalize(stage1, exit_code=0)

        stage3 = self.prepare("03-lemma-discovery")
        self.write_trace(stage3.path, total_tokens=150)
        self.finalize(stage3, exit_code=0)

        lemma_usage = json.loads((stage3.path / "usage.json").read_text())
        self.assertEqual(
            lemma_usage["previous_cumulative"]["total_tokens"], 120
        )
        self.assertEqual(lemma_usage["invocation_delta"]["total_tokens"], 30)

        stage5 = self.prepare("05-lean-proof")
        self.write_trace(stage5.path, total_tokens=170)
        self.finalize(stage5, exit_code=0)

        lean_usage = json.loads((stage5.path / "usage.json").read_text())
        self.assertEqual(
            lean_usage["previous_cumulative"]["total_tokens"], 150
        )
        self.assertEqual(lean_usage["invocation_delta"]["total_tokens"], 20)
        summary = json.loads(
            (self.task.parent.parent / "usage-summary.json").read_text()
        )
        self.assertEqual(summary["totals"]["total_tokens"], 170)

    def test_resumed_stage_rejects_trace_from_a_different_session(
        self,
    ) -> None:
        stage1 = self.prepare()
        self.finalize(stage1, exit_code=0)
        for stage in ("03-lemma-discovery", "05-lean-proof"):
            with self.subTest(stage=stage):
                invocation = self.prepare(stage)
                self.write_trace(invocation.path, [str(uuid.uuid4())])

                with self.assertRaisesRegex(
                    pipeline_contract.PipelineContractError,
                    "trace session does not match",
                ):
                    self.finalize(invocation, exit_code=0)

    def test_stage3_success_requires_same_session_trace(self) -> None:
        stage1 = self.prepare()
        self.finalize(stage1, exit_code=0)
        lemma = self.prepare("03-lemma-discovery")

        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError,
            "successful stage-resume requires a session trace",
        ):
            self.finalize(lemma, exit_code=0)

    def test_stage5_success_requires_same_session_trace(self) -> None:
        stage1 = self.prepare()
        self.finalize(stage1, exit_code=0)
        lean = self.prepare("05-lean-proof")

        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError,
            "successful stage-resume requires a session trace",
        ):
            self.finalize(lean, exit_code=0)

    def test_stage5_timeout_continuation_requires_matching_trace(
        self,
    ) -> None:
        stage1 = self.prepare()
        self.finalize(stage1, exit_code=0)
        lean_initial = self.prepare("05-lean-proof")
        self.write_trace(lean_initial.path)
        self.finalize(
            lean_initial,
            exit_code=143,
            timeout_marker=True,
            duration_s=3600,
        )
        lean_resumed = self.prepare("05-lean-proof")

        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError,
            "successful stage-resume requires a session trace",
        ):
            self.finalize(lean_resumed, exit_code=0)

        self.write_trace(lean_resumed.path, [str(uuid.uuid4())])
        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError,
            "trace session does not match",
        ):
            self.finalize(lean_resumed, exit_code=0)

    def test_usage_subtraction_follows_cumulative_counts_not_stage_order(
        self,
    ) -> None:
        stage1 = self.prepare()
        self.write_trace(stage1.path, total_tokens=120)
        self.finalize(stage1, exit_code=0)

        lean_initial = self.prepare("05-lean-proof")
        self.write_trace(lean_initial.path, total_tokens=150)
        self.finalize(
            lean_initial,
            exit_code=143,
            timeout_marker=True,
            duration_s=3600,
        )

        lemma = self.prepare("03-lemma-discovery")
        self.write_trace(lemma.path, total_tokens=170)
        self.finalize(lemma, exit_code=0)

        lean_resumed = self.prepare("05-lean-proof")
        self.write_trace(lean_resumed.path, total_tokens=190)
        self.finalize(lean_resumed, exit_code=0)

        usage = json.loads((lean_resumed.path / "usage.json").read_text())
        self.assertEqual(usage["previous_cumulative"]["total_tokens"], 170)
        self.assertEqual(usage["invocation_delta"]["total_tokens"], 20)
        summary = json.loads(
            (self.task.parent.parent / "usage-summary.json").read_text()
        )
        self.assertEqual(summary["totals"]["total_tokens"], 190)

    def test_finalize_rejects_preexisting_runtime_metrics(self) -> None:
        invocation = self.prepare()
        (invocation.path / "metrics.json").write_text('{"duration_s": 7}\n')
        (invocation.path / "runtime-metrics.json").write_text(
            '{"duration_s": 99}\n'
        )

        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError,
            "runtime metrics already exist",
        ):
            self.finalize(invocation, exit_code=0)

    def test_trace_failure_does_not_strand_raw_runtime_metrics(self) -> None:
        invocation = self.prepare()
        (invocation.path / "metrics.json").write_text('{"duration_s": 7}\n')
        trace = invocation.path / "codex-trace"
        trace.mkdir()
        rollout = trace / "rollout.jsonl"
        rollout.write_text("not JSON\n")

        with self.assertRaises(pipeline_contract.PipelineContractError):
            self.finalize(invocation, exit_code=0)
        self.assertFalse((invocation.path / "runtime-metrics.json").exists())

        rollout.write_text(
            json.dumps(
                {
                    "type": "session_meta",
                    "payload": {"id": self.session_id},
                }
            )
            + "\n"
        )
        result = self.finalize(invocation, exit_code=0)
        self.assertEqual(result["status"], "SUCCEEDED")
        self.assertTrue((invocation.path / "runtime-metrics.json").is_file())

    def test_hash_failure_restores_raw_metrics_for_retry(self) -> None:
        invocation = self.prepare()
        raw_metrics = '{"duration_s": 7, "start_epoch": 10}\n'
        (invocation.path / "metrics.json").write_text(raw_metrics)
        self.write_trace(invocation.path, total_tokens=120)
        linked_workspace_entry = (
            self.task / "01-k-proof/workspace/linked-prompt.py"
        )
        os.symlink(
            self.task / "01-k-proof/workspace/prompt.py",
            linked_workspace_entry,
        )

        with self.assertRaises(pipeline_contract.PipelineContractError):
            self.finalize(invocation, exit_code=0)
        self.assertEqual(
            (invocation.path / "metrics.json").read_text(),
            raw_metrics,
        )
        self.assertFalse((invocation.path / "runtime-metrics.json").exists())
        self.assertEqual(
            json.loads((invocation.path / "invocation.json").read_text())[
                "status"
            ],
            "PREPARED",
        )

        linked_workspace_entry.unlink()
        result = self.finalize(invocation, exit_code=0)
        self.assertEqual(result["status"], "SUCCEEDED")
        self.assertTrue((invocation.path / "runtime-metrics.json").is_file())

    def test_post_link_failure_removes_runtime_metrics_for_retry(self) -> None:
        invocation = self.prepare()
        raw_metrics = '{"duration_s": 7, "start_epoch": 10}\n'
        (invocation.path / "metrics.json").write_text(raw_metrics)
        self.write_trace(invocation.path, total_tokens=120)
        real_link = os.link

        def publish_then_fail(source: Path, destination: Path) -> None:
            real_link(source, destination)
            source.unlink()
            raise OSError("injected post-link failure")

        with mock.patch.object(
            pipeline_contract.os,
            "link",
            publish_then_fail,
        ):
            with self.assertRaisesRegex(
                pipeline_contract.PipelineContractError,
                "cannot preserve runtime metrics",
            ):
                self.finalize(invocation, exit_code=0)

        self.assertEqual(
            (invocation.path / "metrics.json").read_text(),
            raw_metrics,
        )
        self.assertFalse((invocation.path / "runtime-metrics.json").exists())
        self.assertEqual(
            json.loads((invocation.path / "invocation.json").read_text())[
                "status"
            ],
            "PREPARED",
        )

        result = self.finalize(invocation, exit_code=0)
        self.assertEqual(result["status"], "SUCCEEDED")

    def test_finalize_serializes_summary_after_publication(self) -> None:
        invocation = self.prepare()
        self.write_trace(invocation.path, total_tokens=120)
        run = self.task.parent.parent
        summary_lock = run / ".usage-summary.lock"
        summary_lock.touch()
        real_write_summary = usage_accounting.write_run_summary
        observed = []

        def inspect_publication_and_lock(run_path: Path) -> dict[str, object]:
            manifest = json.loads(
                (invocation.path / "invocation.json").read_text()
            )
            self.assertEqual(manifest["status"], "SUCCEEDED")
            self.assertTrue(
                (self.task / "01-k-proof/result.json").is_file()
            )
            descriptor = os.open(summary_lock, os.O_RDWR)
            try:
                with self.assertRaises(BlockingIOError):
                    fcntl.flock(
                        descriptor,
                        fcntl.LOCK_EX | fcntl.LOCK_NB,
                    )
            finally:
                os.close(descriptor)
            observed.append(True)
            return real_write_summary(run_path)

        with mock.patch.object(
            usage_accounting,
            "write_run_summary",
            inspect_publication_and_lock,
        ):
            self.finalize(invocation, exit_code=0)

        self.assertEqual(observed, [True])

    def test_only_wrapper_marker_classifies_timeout(self) -> None:
        marker = self.prepare()
        marker_result = self.finalize(
            marker, exit_code=143, timeout_marker=True
        )
        self.assertEqual(marker_result["status"], "TIMEOUT")

        other_problem = "9-rolling-max"
        self.make_problem(other_problem)
        pipeline_contract.create_run(
            self.repo,
            run_id="exit-124-run",
            config="codex-gpt-5.6-sol-xhigh-bare",
            problem_ids=[other_problem],
        )
        invocation = pipeline_contract.prepare_invocation(
            self.repo, "exit-124-run", other_problem, "01-k-proof"
        )
        trace = invocation.path / "codex-trace/2026/07/23"
        trace.mkdir(parents=True)
        trace.joinpath("rollout.jsonl").write_text(
            json.dumps(
                {
                    "type": "session_meta",
                    "payload": {"id": str(uuid.uuid4())},
                }
            )
            + "\n"
        )
        result = pipeline_contract.finalize_invocation(
            self.repo,
            "exit-124-run",
            other_problem,
            "01-k-proof",
            invocation.name,
            exit_code=124,
            duration_s=2,
            timeout_marker=False,
            oom_killed=False,
            image_id="image",
        )
        self.assertEqual(result["status"], "FAILED")

    def test_timeout_resumes_once_with_same_session_and_independent_stage_budget(
        self,
    ) -> None:
        initial = self.prepare()
        self.finalize(initial, exit_code=143, timeout_marker=True, duration_s=3600)

        resumed = self.prepare()
        self.assertEqual(resumed.name, "002-timeout-resume")
        self.assertEqual(resumed.kind, "timeout-resume")
        self.assertEqual(resumed.session_id, self.session_id)
        self.assertEqual(resumed.allocation_s, 3600)
        result = self.finalize(
            resumed, exit_code=143, timeout_marker=True, duration_s=3600
        )
        self.assertEqual(result["status"], "TIMEOUT")
        self.assertEqual(result["cumulative_duration_s"], 7200)
        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError, "invocation budget"
        ):
            self.prepare()

        lemma = self.prepare("03-lemma-discovery")
        self.assertEqual(lemma.name, "001-initial")
        self.assertEqual(lemma.kind, "stage-resume")
        self.assertEqual(lemma.session_id, self.session_id)
        self.assertEqual(lemma.allocation_s, 1200)

        lean = self.prepare("05-lean-proof")
        self.assertEqual(lean.name, "001-initial")
        self.assertEqual(lean.kind, "stage-resume")
        self.assertEqual(lean.session_id, self.session_id)
        self.assertEqual(lean.allocation_s, 3600)

    def test_oom_resume_supports_initial_and_post_timeout_oom(self) -> None:
        initial = self.prepare()
        self.finalize(initial, exit_code=137, oom_killed=True)

        resumed = pipeline_contract.prepare_oom_resume(
            self.repo, self.run_id, self.PROBLEM
        )
        self.assertEqual(resumed.name, "002-oom-resume")
        self.assertEqual(resumed.kind, "oom-resume")
        self.assertEqual(resumed.session_id, self.session_id)
        self.assertEqual(resumed.allocation_s, 3600)
        resumed_document = json.loads(
            (resumed.path / "invocation.json").read_text()
        )
        self.assertEqual(resumed_document["retry_of"], "001-initial")
        self.assertEqual(
            resumed_document["memory_limit_bytes"], 16 * 1024**3
        )

        other_problem = "9-rolling-max"
        other_run = "post-timeout-oom"
        self.make_problem(other_problem)
        pipeline_contract.create_run(
            self.repo,
            run_id=other_run,
            config="codex-gpt-5.6-sol-xhigh-kit-semantics",
            problem_ids=[other_problem],
        )
        first = pipeline_contract.prepare_invocation(
            self.repo, other_run, other_problem, "01-k-proof"
        )
        self.write_trace(first.path)
        pipeline_contract.finalize_invocation(
            self.repo,
            other_run,
            other_problem,
            "01-k-proof",
            first.name,
            exit_code=143,
            duration_s=3600,
            timeout_marker=True,
            oom_killed=False,
            image_id="sha256:test-image",
        )
        second = pipeline_contract.prepare_invocation(
            self.repo, other_run, other_problem, "01-k-proof"
        )
        pipeline_contract.finalize_invocation(
            self.repo,
            other_run,
            other_problem,
            "01-k-proof",
            second.name,
            exit_code=137,
            duration_s=100,
            timeout_marker=False,
            oom_killed=True,
            image_id="sha256:test-image",
        )

        third = pipeline_contract.prepare_oom_resume(
            self.repo, other_run, other_problem
        )
        self.assertEqual(third.name, "003-oom-resume")
        self.assertEqual(third.kind, "oom-resume")
        self.assertEqual(third.session_id, self.session_id)

    def test_terminal_resume_supports_failure_and_exhausted_timeout(self) -> None:
        initial = self.prepare()
        self.finalize(initial, exit_code=1)

        resumed = pipeline_contract.prepare_terminal_resume(
            self.repo, self.run_id, self.PROBLEM
        )
        self.assertEqual(resumed.name, "002-failure-resume")
        self.assertEqual(resumed.kind, "terminal-resume")
        self.assertEqual(resumed.session_id, self.session_id)
        document = json.loads((resumed.path / "invocation.json").read_text())
        self.assertEqual(document["continuation_reason"], "transient-model-failure")
        self.assertEqual(document["memory_limit_bytes"], 8 * 1024**3)

        other_problem = "9-rolling-max"
        other_run = "exhausted-timeout-resume"
        self.make_problem(other_problem)
        pipeline_contract.create_run(
            self.repo,
            run_id=other_run,
            config="codex-gpt-5.6-sol-xhigh-kit-semantics",
            problem_ids=[other_problem],
        )
        first = pipeline_contract.prepare_invocation(
            self.repo, other_run, other_problem, "01-k-proof"
        )
        self.write_trace(first.path)
        pipeline_contract.finalize_invocation(
            self.repo,
            other_run,
            other_problem,
            "01-k-proof",
            first.name,
            exit_code=143,
            duration_s=3600,
            timeout_marker=True,
            oom_killed=False,
            image_id="sha256:test-image",
        )
        second = pipeline_contract.prepare_invocation(
            self.repo, other_run, other_problem, "01-k-proof"
        )
        pipeline_contract.finalize_invocation(
            self.repo,
            other_run,
            other_problem,
            "01-k-proof",
            second.name,
            exit_code=143,
            duration_s=3600,
            timeout_marker=True,
            oom_killed=False,
            image_id="sha256:test-image",
        )

        third = pipeline_contract.prepare_terminal_resume(
            self.repo, other_run, other_problem
        )
        self.assertEqual(third.name, "003-timeout-extension")
        third_document = json.loads(
            (third.path / "invocation.json").read_text()
        )
        self.assertEqual(
            third_document["continuation_reason"], "exhausted-timeout"
        )

    def test_equal_initial_and_total_budget_has_no_timeout_continuation(
        self,
    ) -> None:
        stage1 = self.prepare()
        self.finalize(stage1, exit_code=0)
        lemma = self.prepare("03-lemma-discovery")
        self.write_trace(lemma.path)
        self.finalize(
            lemma,
            exit_code=143,
            timeout_marker=True,
            duration_s=1200,
        )

        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError, "invocation budget"
        ):
            self.prepare("03-lemma-discovery")

    def _finalize_infrastructure_blocked_second(
        self, *, mutate_workspace: bool = False, include_signature: bool = True
    ) -> tuple[pipeline_contract.Invocation, str]:
        initial = self.prepare()
        self.finalize(
            initial, exit_code=143, timeout_marker=True, duration_s=3600
        )
        second = self.prepare()
        message = (
            self.BWRAP_NAMESPACE_ERROR
            if include_signature
            else "ordinary model output without infrastructure failure"
        )
        (second.path / "codex-output.log").write_text(message + "\n")
        if mutate_workspace:
            (
                self.task / "01-k-proof/workspace/partial-artifact.txt"
            ).write_text("changed\n")
        before = pipeline_contract.sha256_file(
            second.path / "invocation.json"
        )
        self.finalize(second, exit_code=0, duration_s=60)
        return second, before

    def test_prepares_one_immutable_infrastructure_retry(self) -> None:
        second, _before_finalize = self._finalize_infrastructure_blocked_second()
        second_manifest_hash = pipeline_contract.sha256_file(
            second.path / "invocation.json"
        )

        retry = pipeline_contract.prepare_infrastructure_retry(
            self.repo, self.run_id, self.PROBLEM, "01-k-proof"
        )

        self.assertEqual(retry.name, "003-infrastructure-retry")
        self.assertEqual(retry.kind, "infrastructure-retry")
        self.assertEqual(retry.session_id, self.session_id)
        self.assertEqual(retry.allocation_s, 3600)
        document = json.loads((retry.path / "invocation.json").read_text())
        self.assertEqual(document["retry_of"], "002-timeout-resume")
        self.assertEqual(
            document["inputs"]["workspace_sha256"],
            pipeline_contract.sha256_tree(
                self.task / "01-k-proof/workspace"
            ),
        )
        self.assertEqual(
            pipeline_contract.sha256_file(second.path / "invocation.json"),
            second_manifest_hash,
        )
        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError,
            "PREPARED|finalized",
        ):
            pipeline_contract.prepare_infrastructure_retry(
                self.repo, self.run_id, self.PROBLEM, "01-k-proof"
            )
        failed = self.finalize(
            retry, exit_code=70, duration_s=0
        )
        self.assertEqual(failed["status"], "FAILED")

        repaired = pipeline_contract.prepare_infrastructure_retry(
            self.repo, self.run_id, self.PROBLEM, "01-k-proof"
        )
        self.assertEqual(repaired.name, "004-infrastructure-retry")
        self.assertEqual(repaired.kind, "infrastructure-retry")
        repaired_document = json.loads(
            (repaired.path / "invocation.json").read_text()
        )
        self.assertEqual(
            repaired_document["retry_of"],
            "003-infrastructure-retry",
        )
        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError, "exhausted|PREPARED"
        ):
            pipeline_contract.prepare_infrastructure_retry(
                self.repo, self.run_id, self.PROBLEM, "01-k-proof"
            )

    def test_infrastructure_retry_rejects_changed_workspace(self) -> None:
        self._finalize_infrastructure_blocked_second(mutate_workspace=True)
        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError, "workspace"
        ):
            pipeline_contract.prepare_infrastructure_retry(
                self.repo, self.run_id, self.PROBLEM, "01-k-proof"
            )

    def test_infrastructure_retry_requires_namespace_denial_evidence(self) -> None:
        self._finalize_infrastructure_blocked_second(
            include_signature=False
        )
        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError, "namespace-denial"
        ):
            pipeline_contract.prepare_infrastructure_retry(
                self.repo, self.run_id, self.PROBLEM, "01-k-proof"
            )

    def test_resume_refuses_missing_session_or_replaced_codex_home(self) -> None:
        initial = self.prepare()
        self.finalize(initial, exit_code=143, timeout_marker=True)
        session = self.state / "session.json"
        session.unlink()
        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError, "session"
        ):
            self.prepare()

        # Recreate the task state and then replace the persistent home inode.
        pipeline_contract.write_session_state(
            self.state, self.session_id, "01-k-proof/001-initial"
        )
        home = self.state / "codex-home"
        home.rmdir()
        home.mkdir()
        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError, "CODEX_HOME"
        ):
            self.prepare()

    def test_oom_comes_only_from_explicit_container_state(self) -> None:
        first = self.prepare()
        result = self.finalize(first, exit_code=137, oom_killed=False)
        self.assertEqual(result["status"], "FAILED")

        other_problem = "10-make-palindrome"
        self.make_problem(other_problem)
        pipeline_contract.create_run(
            self.repo,
            run_id="oom-run",
            config="codex-gpt-5.6-sol-xhigh-bare",
            problem_ids=[other_problem],
        )
        invocation = pipeline_contract.prepare_invocation(
            self.repo, "oom-run", other_problem, "01-k-proof"
        )
        trace = invocation.path / "codex-trace"
        trace.mkdir()
        trace.joinpath("rollout.jsonl").write_text(
            json.dumps(
                {
                    "type": "session_meta",
                    "payload": {"id": str(uuid.uuid4())},
                }
            )
            + "\n"
        )
        result = pipeline_contract.finalize_invocation(
            self.repo,
            "oom-run",
            other_problem,
            "01-k-proof",
            invocation.name,
            exit_code=1,
            duration_s=1,
            timeout_marker=False,
            oom_killed=True,
            image_id="image",
        )
        self.assertEqual(result["status"], "OOM")

    def test_initial_failure_without_session_trace_is_terminal_not_prepared(
        self,
    ) -> None:
        invocation = self.prepare()
        result = pipeline_contract.finalize_invocation(
            self.repo,
            self.run_id,
            self.PROBLEM,
            invocation.stage,
            invocation.name,
            exit_code=70,
            duration_s=0,
            timeout_marker=False,
            oom_killed=False,
            image_id="UNAVAILABLE",
        )
        self.assertEqual(result["status"], "FAILED")
        self.assertIsNone(result["session_id"])
        self.assertFalse(result["resumable"])
        persisted = json.loads(
            (invocation.path / "invocation.json").read_text()
        )
        self.assertEqual(persisted["status"], "FAILED")
        self.assertFalse((self.state / "session.json").exists())

    def test_ledger_is_append_only(self) -> None:
        first = self.prepare()
        self.finalize(first, exit_code=143, timeout_marker=True)
        second = self.prepare()
        self.finalize(second, exit_code=0)

        records = [
            json.loads(line)
            for line in (self.state / "stage-ledger.jsonl").read_text().splitlines()
        ]
        self.assertEqual(
            [record["event"] for record in records],
            [
                "invocation_prepared",
                "invocation_finalized",
                "invocation_prepared",
                "invocation_finalized",
            ],
        )
        self.assertEqual([record["sequence"] for record in records], [1, 2, 3, 4])


class SelectionStateTests(PipelineStateFixture):
    def make_execution(
        self,
        stage: str,
        name: str,
        document_name: str,
        document: dict[str, object],
    ) -> Path:
        container = (
            "generations" if stage == "04-klean-generation" else "executions"
        )
        candidate = self.task / stage / container / name
        candidate.mkdir()
        (candidate / "artifact.txt").write_text(name + "\n")
        (candidate / document_name).write_text(json.dumps(document) + "\n")
        if stage == "04-klean-generation":
            (candidate / "export.log").write_text("exported\n")
            if document.get("status") == "PASS":
                for required in (
                    "input-manifest.json",
                    "generator-manifest.json",
                    "trust-inventory.json",
                    "export-result.json",
                    "preflight.log",
                ):
                    (candidate / required).write_text("{}\n")
                (candidate / "generated").mkdir()
                (candidate / "generated/Main.lean").write_text(
                    "theorem target : True := by trivial\n"
                )
        if stage in {"02-k-audit", "06-lean-audit"}:
            for required in (
                "audit-input.json",
                "metrics.json",
                "codex-output.log",
                "codex-last.txt",
                "REVIEW.md",
            ):
                (candidate / required).write_text(required + "\n")
            (candidate / "codex-trace").mkdir()
            (candidate / "codex-trace/rollout.jsonl").write_text(
                json.dumps(
                    {
                        "type": "event_msg",
                        "payload": {
                            "type": "token_count",
                            "info": {
                                "total_token_usage": {
                                    "input_tokens": 40,
                                    "cached_input_tokens": 0,
                                    "output_tokens": 10,
                                    "reasoning_output_tokens": 0,
                                    "total_tokens": 50,
                                }
                            },
                        },
                    }
                )
                + "\n"
            )
            if document.get("audit_status") == "COMPLETE":
                usage_accounting.write_trace_usage(
                    candidate / "codex-trace",
                    candidate / "usage.json",
                )
            (candidate / "evidence").mkdir()
            (candidate / "evidence/check.txt").write_text("checked\n")
            if (
                stage == "06-lean-audit"
                and document.get("audit_status") == "COMPLETE"
            ):
                (candidate / "mechanical-check.json").write_text(
                    json.dumps({"status": "PASS"}) + "\n"
                )
        return candidate

    def test_selects_complete_audit_by_relative_path_and_hash(self) -> None:
        candidate = self.make_execution(
            "02-k-audit",
            "001",
            "verdict.json",
            {"audit_status": "COMPLETE", "verdict": "PASS", "legitimacy": "LEGIT"},
        )
        selected = pipeline_contract.select_stage_output(
            self.repo,
            self.run_id,
            self.PROBLEM,
            "02-k-audit",
            "001",
        )
        self.assertEqual(selected["relative_path"], "executions/001")
        self.assertEqual(
            selected["artifact_sha256"], pipeline_contract.sha256_tree(candidate)
        )
        self.assertFalse((self.task / "02-k-audit/selected.json").is_symlink())

    def test_selects_complete_audit_at_explicit_task_and_state_paths(
        self,
    ) -> None:
        candidate = self.make_execution(
            "02-k-audit",
            "001",
            "verdict.json",
            {
                "audit_status": "COMPLETE",
                "verdict": "CONCERNS",
                "legitimacy": "LEGIT",
            },
        )

        selected = pipeline_contract.select_stage_output_at(
            self.task,
            self.state,
            "02-k-audit",
            "001",
        )

        self.assertEqual(selected["status"], "CONCERNS")
        self.assertEqual(
            selected["artifact_sha256"],
            pipeline_contract.sha256_tree(candidate),
        )

    def test_selection_rejects_candidate_changed_from_expected_hash(
        self,
    ) -> None:
        candidate = self.make_execution(
            "02-k-audit",
            "001",
            "verdict.json",
            {
                "audit_status": "COMPLETE",
                "verdict": "PASS",
                "legitimacy": "LEGIT",
            },
        )
        expected = pipeline_contract.sha256_tree(candidate)
        (candidate / "artifact.txt").write_text("changed\n")

        try:
            with self.assertRaisesRegex(
                pipeline_contract.PipelineContractError,
                "candidate changed",
            ):
                pipeline_contract.select_stage_output(
                    self.repo,
                    self.run_id,
                    self.PROBLEM,
                    "02-k-audit",
                    "001",
                    expected_candidate_sha256=expected,
                )
        except TypeError as error:
            self.fail(f"selection lacks expected-hash guard: {error}")
        self.assertFalse(
            (self.task / "02-k-audit/selected.json").exists()
        )

    def test_audit_replacement_requires_previous_audit_error(self) -> None:
        self.make_execution(
            "02-k-audit",
            "001",
            "verdict.json",
            {"audit_status": "COMPLETE", "verdict": "PASS", "legitimacy": "LEGIT"},
        )
        self.make_execution(
            "02-k-audit",
            "002",
            "verdict.json",
            {"audit_status": "COMPLETE", "verdict": "PASS", "legitimacy": "LEGIT"},
        )
        pipeline_contract.select_stage_output(
            self.repo, self.run_id, self.PROBLEM, "02-k-audit", "001"
        )
        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError, "terminal"
        ):
            pipeline_contract.select_stage_output(
                self.repo, self.run_id, self.PROBLEM, "02-k-audit", "002"
            )

    def test_audit_error_and_preflight_error_can_be_replaced_once_repaired(
        self,
    ) -> None:
        pretrace_error = self.make_execution(
            "06-lean-audit",
            "001",
            "verdict.json",
            {"audit_status": "AUDIT_ERROR", "verdict": None, "legitimacy": None},
        )
        (pretrace_error / "codex-trace/rollout.jsonl").unlink()
        self.make_execution(
            "06-lean-audit",
            "002",
            "verdict.json",
            {"audit_status": "COMPLETE", "verdict": "CONCERNS", "legitimacy": "LEGIT"},
        )
        pipeline_contract.select_stage_output(
            self.repo, self.run_id, self.PROBLEM, "06-lean-audit", "001"
        )
        selected = pipeline_contract.select_stage_output(
            self.repo, self.run_id, self.PROBLEM, "06-lean-audit", "002"
        )
        self.assertEqual(selected["relative_path"], "executions/002")

        self.make_execution(
            "04-klean-generation",
            "001",
            "preflight.json",
            {"status": "KLEAN_PREFLIGHT_ERROR"},
        )
        self.make_execution(
            "04-klean-generation",
            "002",
            "preflight.json",
            {"status": "PASS"},
        )
        pipeline_contract.select_stage_output(
            self.repo,
            self.run_id,
            self.PROBLEM,
            "04-klean-generation",
            "001",
        )
        selected = pipeline_contract.select_stage_output(
            self.repo,
            self.run_id,
            self.PROBLEM,
            "04-klean-generation",
            "002",
        )
        self.assertEqual(selected["relative_path"], "generations/002")

    def test_terminal_stage4_replacement_requires_explicit_authorization(
        self,
    ) -> None:
        self.make_execution(
            "04-klean-generation",
            "001",
            "preflight.json",
            {"status": "PASS"},
        )
        self.make_execution(
            "04-klean-generation",
            "002",
            "preflight.json",
            {"status": "PASS"},
        )
        pipeline_contract.select_stage_output(
            self.repo,
            self.run_id,
            self.PROBLEM,
            "04-klean-generation",
            "001",
        )
        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError, "terminal"
        ):
            pipeline_contract.select_stage_output(
                self.repo,
                self.run_id,
                self.PROBLEM,
                "04-klean-generation",
                "002",
            )

        selected = pipeline_contract.select_stage_output(
            self.repo,
            self.run_id,
            self.PROBLEM,
            "04-klean-generation",
            "002",
            replace_selected=True,
        )

        self.assertEqual(selected["relative_path"], "generations/002")
        self.assertEqual(selected["replaces"], "generations/001")


if __name__ == "__main__":
    unittest.main()
