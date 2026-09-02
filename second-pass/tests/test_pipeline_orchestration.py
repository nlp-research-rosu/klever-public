import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import run_pipeline


class PipelineOrchestrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name)
        run = self.repo / "runs/demo"
        (run / "tasks").mkdir(parents=True)
        (run / "run.json").write_text(
            json.dumps(
                {
                    "run_id": "demo",
                    "tasks": ["0-first", "1-second"],
                }
            )
            + "\n"
        )
        for problem in ("0-first", "1-second"):
            task = run / "tasks" / problem
            for stage in run_pipeline.STAGES:
                (task / stage).mkdir(parents=True)
            (task / "task.json").write_text("{}\n")
            (self.repo / "runner-state/demo" / problem).mkdir(
                parents=True
            )
        for script in run_pipeline.STAGE_SCRIPTS.values():
            path = self.repo / script
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("#!/usr/bin/env bash\nexit 0\n")

    def test_runs_all_six_stages_in_order_and_resumes_after_interruption(
        self,
    ) -> None:
        expected = [
            ("PENDING_K_PROOF", "01-k-proof"),
            ("PENDING_K_AUDIT", "02-k-audit"),
            ("PENDING_LEMMA_DISCOVERY", "03-lemma-discovery"),
            ("PENDING_KLEAN_GENERATION", "04-klean-generation"),
            ("PENDING_LEAN_PROOF", "05-lean-proof"),
            ("PENDING_LEAN_AUDIT", "06-lean-audit"),
        ]
        states = iter(
            [
                {"state": state, "next_stage": stage}
                for state, stage in expected
            ]
            + [{"state": "COMPLETE_LEGIT", "next_stage": None}]
        )
        calls = []
        with mock.patch.object(
            run_pipeline, "inspect_problem", side_effect=lambda *args: next(states)
        ):
            result = run_pipeline.run_problem(
                self.repo,
                "demo",
                "0-first",
                execute=lambda command: calls.append(command) or 0,
            )
        self.assertEqual(result["state"], "COMPLETE_LEGIT")
        self.assertEqual(
            [run_pipeline.stage_from_command(command) for command in calls],
            list(run_pipeline.STAGES),
        )

        calls.clear()
        with mock.patch.object(
            run_pipeline,
            "inspect_problem",
            return_value={"state": "COMPLETE_LEGIT", "next_stage": None},
        ):
            run_pipeline.run_problem(
                self.repo,
                "demo",
                "0-first",
                execute=lambda command: calls.append(command) or 0,
            )
        self.assertEqual(calls, [])

    def test_numeric_aliases_name_each_canonical_stage(self) -> None:
        self.assertEqual(
            [
                run_pipeline.stage_from_command(
                    run_pipeline.command_for_stage(
                        self.repo,
                        "demo",
                        "0-first",
                        str(index),
                    )
                )
                for index in range(1, 7)
            ],
            list(run_pipeline.STAGES),
        )

    def inspect_with_statuses(
        self,
        *,
        results: dict[str, str | None],
        selections: dict[str, str | None],
    ) -> dict:
        with (
            mock.patch.object(
                run_pipeline,
                "_result_status",
                side_effect=lambda _task, stage: results.get(stage),
            ),
            mock.patch.object(
                run_pipeline,
                "_selected_status",
                side_effect=lambda _task, stage: selections.get(stage),
            ),
        ):
            return run_pipeline.inspect_problem(
                self.repo, "demo", "0-first"
            )

    def test_inspection_reports_each_canonical_pending_transition(self) -> None:
        expected = [
            ("PENDING_K_PROOF", "01-k-proof"),
            ("PENDING_K_AUDIT", "02-k-audit"),
            ("PENDING_LEMMA_DISCOVERY", "03-lemma-discovery"),
            ("PENDING_KLEAN_GENERATION", "04-klean-generation"),
            ("PENDING_LEAN_PROOF", "05-lean-proof"),
            ("PENDING_LEAN_AUDIT", "06-lean-audit"),
        ]
        cases = (
            ({}, {}),
            ({"01-k-proof": "SUCCEEDED"}, {}),
            (
                {"01-k-proof": "SUCCEEDED"},
                {"02-k-audit": "PASS"},
            ),
            (
                {
                    "01-k-proof": "SUCCEEDED",
                    "03-lemma-discovery": "SUCCEEDED",
                },
                {"02-k-audit": "PASS"},
            ),
            (
                {
                    "01-k-proof": "SUCCEEDED",
                    "03-lemma-discovery": "SUCCEEDED",
                },
                {
                    "02-k-audit": "PASS",
                    "04-klean-generation": "PASS",
                },
            ),
            (
                {
                    "01-k-proof": "SUCCEEDED",
                    "03-lemma-discovery": "SUCCEEDED",
                    "05-lean-proof": "SUCCEEDED",
                },
                {
                    "02-k-audit": "PASS",
                    "04-klean-generation": "PASS",
                },
            ),
        )
        for (state, stage), (results, selections) in zip(
            expected, cases, strict=True
        ):
            with self.subTest(state=state):
                self.assertEqual(
                    self.inspect_with_statuses(
                        results=results,
                        selections=selections,
                    ),
                    {"state": state, "next_stage": stage},
                )

    def test_no_obligations_routes_from_stage4_directly_to_stage6(self) -> None:
        self.assertEqual(
            self.inspect_with_statuses(
                results={
                    "01-k-proof": "SUCCEEDED",
                    "03-lemma-discovery": "SUCCEEDED",
                },
                selections={
                    "02-k-audit": "PASS",
                    "04-klean-generation": "KLEAN_NO_OBLIGATIONS",
                },
            ),
            {"state": "PENDING_LEAN_AUDIT", "next_stage": "06-lean-audit"},
        )

    def test_failed_lemma_discovery_is_terminal_before_stage4(self) -> None:
        self.assertEqual(
            self.inspect_with_statuses(
                results={
                    "01-k-proof": "SUCCEEDED",
                    "03-lemma-discovery": "FAILED",
                },
                selections={"02-k-audit": "PASS"},
            ),
            {"state": "LEMMA_DISCOVERY_FAILED", "next_stage": None},
        )

    def test_stage6_pass_and_concerns_are_complete(self) -> None:
        for verdict in ("PASS", "CONCERNS"):
            with self.subTest(verdict=verdict):
                self.assertEqual(
                    self.inspect_with_statuses(
                        results={
                            "01-k-proof": "SUCCEEDED",
                            "03-lemma-discovery": "SUCCEEDED",
                        },
                        selections={
                            "02-k-audit": "PASS",
                            "04-klean-generation": (
                                "KLEAN_NO_OBLIGATIONS"
                            ),
                            "06-lean-audit": verdict,
                        },
                    ),
                    {
                        "state": "COMPLETE_LEGIT",
                        "next_stage": None,
                        "lean_audit_verdict": verdict,
                    },
                )

    def test_stage2_fail_is_terminal(self) -> None:
        self.assertEqual(
            self.inspect_with_statuses(
                results={"01-k-proof": "SUCCEEDED"},
                selections={"02-k-audit": "FAIL"},
            ),
            {"state": "K_AUDIT_FAIL", "next_stage": None},
        )

    def test_manual_preflight_repair_uses_stage4_alias(self) -> None:
        calls = []
        with mock.patch.object(
            run_pipeline,
            "inspect_problem",
            return_value={
                "state": "KLEAN_PREFLIGHT_ERROR",
                "next_stage": None,
            },
        ):
            return_code = run_pipeline.run_one_stage(
                self.repo,
                "demo",
                "0-first",
                "4",
                execute=lambda command: calls.append(command) or 0,
            )

        self.assertEqual(return_code, 0)
        self.assertEqual(
            [run_pipeline.stage_from_command(command) for command in calls],
            ["04-klean-generation"],
        )

    def test_incomplete_input_provenance_blocks_before_stage1_inspection(
        self,
    ) -> None:
        task = self.repo / "runs/demo/tasks/0-first"
        (task / "task.json").write_text(
            json.dumps(
                {
                    "input_provenance": "INCOMPLETE",
                    "pipeline_block": "INPUT_PROVENANCE_INCOMPLETE",
                }
            )
            + "\n"
        )

        self.assertEqual(
            run_pipeline.inspect_problem(self.repo, "demo", "0-first"),
            {"state": "BLOCKED_INPUT_PROVENANCE", "next_stage": None},
        )

    def test_unrecoverable_session_state_is_a_supported_stage3_blocker(
        self,
    ) -> None:
        task = self.repo / "runs/demo/tasks/0-first"
        (task / "task.json").write_text(
            json.dumps(
                {
                    "session_provenance": {
                        "status": "UNRECOVERABLE",
                        "reason": "SESSION_STATE_MISSING",
                    },
                    "pipeline_block": "SESSION_STATE_UNRECOVERABLE",
                }
            )
            + "\n"
        )

        self.assertEqual(
            run_pipeline.inspect_problem(self.repo, "demo", "0-first"),
            {"state": "BLOCKED_SESSION_STATE", "next_stage": None},
        )

    def test_unknown_or_inconsistent_pipeline_blocks_fail_closed(self) -> None:
        task_manifest = self.repo / "runs/demo/tasks/0-first/task.json"
        cases = (
            (
                {
                    "input_provenance": "INCOMPLETE",
                    "pipeline_block": "UNKNOWN",
                },
                "unknown task pipeline block",
            ),
            (
                {
                    "input_provenance": "COMPLETE",
                    "pipeline_block": "INPUT_PROVENANCE_INCOMPLETE",
                },
                "pipeline block lacks incomplete provenance",
            ),
        )
        for manifest, message in cases:
            with self.subTest(manifest=manifest):
                task_manifest.write_text(json.dumps(manifest) + "\n")
                with self.assertRaisesRegex(
                    run_pipeline.PipelineOrchestrationError, message
                ):
                    run_pipeline.inspect_problem(
                        self.repo, "demo", "0-first"
                    )

    def test_terminal_failures_and_manual_preflight_repair_do_not_advance(
        self,
    ) -> None:
        for state in (
            "K_PROOF_TIMEOUT",
            "K_PROOF_OOM",
            "K_AUDIT_FAIL",
            "KLEAN_PREFLIGHT_ERROR",
            "LEAN_PROOF_FAILED",
            "LEAN_AUDIT_FAIL",
        ):
            calls = []
            with mock.patch.object(
                run_pipeline,
                "inspect_problem",
                return_value={"state": state, "next_stage": None},
            ):
                result = run_pipeline.run_problem(
                    self.repo,
                    "demo",
                    "0-first",
                    execute=lambda command: calls.append(command) or 0,
                )
            self.assertEqual(result["state"], state)
            self.assertEqual(calls, [])

    def test_audit_error_retries_only_its_independent_audit(self) -> None:
        for state, stage in (
            ("K_AUDIT_ERROR_RETRY", "02-k-audit"),
            ("LEAN_AUDIT_ERROR_RETRY", "06-lean-audit"),
        ):
            states = iter(
                [
                    {"state": state, "next_stage": stage},
                    {"state": "COMPLETE_LEGIT", "next_stage": None},
                ]
            )
            calls = []
            with mock.patch.object(
                run_pipeline,
                "inspect_problem",
                side_effect=lambda *args: next(states),
            ):
                run_pipeline.run_problem(
                    self.repo,
                    "demo",
                    "0-first",
                    execute=lambda command: calls.append(command) or 0,
                )
            self.assertEqual(
                [run_pipeline.stage_from_command(command) for command in calls],
                [stage],
            )

    def test_dry_run_and_status_never_launch_a_model(self) -> None:
        pending = {
            "state": "PENDING_K_PROOF",
            "next_stage": "01-k-proof",
        }
        with mock.patch.object(
            run_pipeline, "inspect_problem", return_value=pending
        ), mock.patch("subprocess.run") as subprocess_run:
            dry = run_pipeline.dry_run(self.repo, "demo")
            status = run_pipeline.run_status(self.repo, "demo")
        subprocess_run.assert_not_called()
        self.assertEqual(len(dry), 2)
        self.assertEqual(len(status["tasks"]), 2)

    def test_parallel_batch_keeps_stable_problem_arguments(self) -> None:
        seen = []

        def fake_run_problem(repo, run_id, problem, *, execute):
            seen.append(problem)
            return {"state": "COMPLETE_LEGIT", "next_stage": None}

        with mock.patch.object(
            run_pipeline, "run_problem", side_effect=fake_run_problem
        ):
            result = run_pipeline.run_batch(
                self.repo, "demo", jobs=2, execute=lambda command: 0
            )
        self.assertEqual(sorted(seen), ["0-first", "1-second"])
        self.assertEqual(sorted(result), ["0-first", "1-second"])


if __name__ == "__main__":
    unittest.main()
