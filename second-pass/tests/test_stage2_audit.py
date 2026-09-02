import json
import uuid
from pathlib import Path

from tests.test_pipeline_layout import PipelineLayoutFixture
from tools import audit_contract, pipeline_contract, usage_accounting


class Stage2AuditFixture(PipelineLayoutFixture):
    def setUp(self) -> None:
        super().setUp()
        self.run_id = "stage2-run"
        pipeline_contract.create_run(
            self.repo,
            run_id=self.run_id,
            config="codex-gpt-audited-xhigh-kit-semantics",
            problem_ids=[self.PROBLEM],
        )
        self.task = self.repo / f"runs/{self.run_id}/tasks/{self.PROBLEM}"
        self.workspace = self.task / "01-k-proof/workspace"
        for name in (
            "solution.py",
            "solution.mpy",
            "verification.k",
            "spec.k",
            "prove.sh",
            "PROOF.md",
        ):
            (self.workspace / name).write_text(f"{name}\n")
        invocation = pipeline_contract.prepare_invocation(
            self.repo, self.run_id, self.PROBLEM, "01-k-proof"
        )
        (invocation.path / "codex-output.log").write_text("generation output\n")
        (invocation.path / "codex-last.txt").write_text("generation done\n")
        (invocation.path / "runtime-metrics.json").write_text("{}\n")
        (invocation.path / "usage.json").write_text("{}\n")
        (invocation.path / "prompt.txt").write_text("generation prompt\n")
        trace = invocation.path / "codex-trace/2026/07/23"
        trace.mkdir(parents=True)
        self.session_id = str(uuid.uuid4())
        trace.joinpath("rollout.jsonl").write_text(
            json.dumps(
                {
                    "type": "session_meta",
                    "payload": {"id": self.session_id},
                }
            )
            + "\n"
        )
        self.result = pipeline_contract.finalize_invocation(
            self.repo,
            self.run_id,
            self.PROBLEM,
            "01-k-proof",
            invocation.name,
            exit_code=0,
            duration_s=42,
            timeout_marker=False,
            oom_killed=False,
            image_id="sha256:generation",
        )

    def mark_input_provenance_incomplete(self) -> None:
        manifest_path = self.task / "task.json"
        manifest = json.loads(manifest_path.read_text())
        manifest.update(
            {
                "input_provenance": "INCOMPLETE",
                "pipeline_block": "INPUT_PROVENANCE_INCOMPLETE",
            }
        )
        manifest_path.write_text(json.dumps(manifest) + "\n")

    def complete_audit(
        self,
        execution: Path,
        *,
        audit_status: str = "COMPLETE",
        verdict: str | None = "PASS",
        legitimacy: str | None = "LEGIT",
    ) -> None:
        (execution / "audit-input.json").write_text("{}\n")
        (execution / "metrics.json").write_text("{}\n")
        (execution / "codex-output.log").write_text("audit output\n")
        (execution / "codex-last.txt").write_text("audit done\n")
        (execution / "codex-trace").mkdir()
        (execution / "codex-trace/rollout.jsonl").write_text(
            json.dumps(
                {
                    "type": "event_msg",
                    "payload": {
                        "type": "token_count",
                        "info": {
                            "total_token_usage": {
                                "input_tokens": 80,
                                "cached_input_tokens": 20,
                                "output_tokens": 20,
                                "reasoning_output_tokens": 5,
                                "total_tokens": 100,
                            }
                        },
                    },
                }
            )
            + "\n"
        )
        (execution / "evidence").mkdir(exist_ok=True)
        (execution / "evidence/check.txt").write_text("checked\n")
        (execution / "REVIEW.md").write_text("review\n")
        (execution / "verdict.json").write_text(
            json.dumps(
                {
                    "audit_status": audit_status,
                    "verdict": verdict,
                    "legitimacy": legitimacy,
                    "error": "infrastructure" if audit_status == "AUDIT_ERROR" else None,
                }
            )
            + "\n"
        )
        usage_accounting.write_trace_usage(
            execution / "codex-trace",
            execution / "usage.json",
        )


class Stage2ResolutionTests(Stage2AuditFixture):
    def test_resolves_frozen_workspace_and_selected_generation_evidence(self) -> None:
        resolution = audit_contract.resolve_stage2_audit(
            self.repo, self.run_id, self.PROBLEM
        )
        invocation = (
            self.task
            / f"01-k-proof/invocations/{self.result['invocation']}"
        )
        self.assertEqual(Path(resolution["candidate"]), self.workspace.resolve())
        self.assertEqual(resolution["generation_config"], "codex-gpt-audited-xhigh-kit-semantics")
        self.assertEqual(resolution["condition"], "kit-semantics")
        self.assertEqual(resolution["semantics_mode"], "SUPPLIED_SEMANTICS")
        self.assertEqual(
            Path(resolution["generation_evidence"]["metrics"]),
            (invocation / "metrics.json").resolve(),
        )
        self.assertEqual(resolution["record_layout"], "pipeline-v3")
        self.assertEqual(
            Path(resolution["generation_root"]), invocation.resolve()
        )
        self.assertEqual(
            Path(resolution["run_manifest"]),
            (self.task.parent.parent / "run.json").resolve(),
        )
        self.assertEqual(
            Path(resolution["task_manifest"]),
            (self.task / "task.json").resolve(),
        )
        self.assertEqual(
            Path(resolution["stage1_result"]),
            (self.task / "01-k-proof/result.json").resolve(),
        )
        for name in (
            "run_manifest_sha256",
            "task_manifest_sha256",
            "stage1_result_sha256",
            "stage1_invocation_sha256",
            "generation_runtime_metrics_sha256",
            "generation_usage_sha256",
            "generation_prompt_sha256",
        ):
            self.assertRegex(resolution["hashes"][name], r"^[0-9a-f]{64}$")
        self.assertEqual(
            resolution["hashes"]["candidate_tree_sha256"],
            audit_contract.sha256_tree(self.workspace),
        )
        self.assertTrue(resolution["integrity"]["candidate_prompt_matches_trusted"])
        self.assertTrue(
            resolution["integrity"]["candidate_reference_semantics_matches_trusted"]
        )
        self.assertTrue(
            resolution["integrity"][
                "manifest_reference_semantics_hash_matches_trusted"
            ]
        )
        self.assertEqual(
            resolution["hashes"][
                "trusted_reference_semantics_manifest_sha256"
            ],
            pipeline_contract.sha256_tree(self.repo / "data/reference/src"),
        )

    def test_incomplete_stage1_candidate_is_refused(self) -> None:
        (self.workspace / "PROOF.md").unlink()
        with self.assertRaisesRegex(audit_contract.AuditContractError, "PROOF.md"):
            audit_contract.resolve_stage2_audit(
                self.repo, self.run_id, self.PROBLEM
            )

    def test_missing_generation_record_is_an_infrastructure_preflight_error(
        self,
    ) -> None:
        invocation = (
            self.task
            / f"01-k-proof/invocations/{self.result['invocation']}"
        )
        (invocation / "usage.json").unlink()

        with self.assertRaisesRegex(
            audit_contract.AuditContractError,
            "selected Stage 1 usage.json",
        ):
            audit_contract.resolve_stage2_audit(
                self.repo, self.run_id, self.PROBLEM
            )

    def test_legacy_import_without_proof_document_remains_auditable(self) -> None:
        (self.workspace / "PROOF.md").unlink()
        invocation_root = (
            self.task
            / f"01-k-proof/invocations/{self.result['invocation']}"
        )
        (invocation_root / "runtime-metrics.json").unlink()
        run_path = self.repo / f"runs/{self.run_id}/run.json"
        run = json.loads(run_path.read_text())
        run["legacy_import"] = True
        run_path.write_text(json.dumps(run) + "\n")

        task_path = self.task / "task.json"
        task = json.loads(task_path.read_text())
        task["input_provenance"] = "COMPLETE"
        task_path.write_text(json.dumps(task) + "\n")

        invocation_path = (
            self.task
            / f"01-k-proof/invocations/{self.result['invocation']}/invocation.json"
        )
        invocation = json.loads(invocation_path.read_text())
        invocation["legacy_import"] = True
        invocation_path.write_text(json.dumps(invocation) + "\n")

        result_path = self.task / "01-k-proof/result.json"
        result = json.loads(result_path.read_text())
        result["legacy_import"] = True
        result["outputs"]["workspace_sha256"] = pipeline_contract.sha256_tree(
            self.workspace
        )
        result_path.write_text(json.dumps(result) + "\n")
        (self.task / "migration.json").write_text(
            json.dumps(
                {
                    "legacy_import": True,
                    "status": "SUCCEEDED",
                    "input_provenance": "COMPLETE",
                    "invocation": self.result["invocation"],
                }
            )
            + "\n"
        )

        resolution = audit_contract.resolve_stage2_audit(
            self.repo, self.run_id, self.PROBLEM
        )

        self.assertEqual(Path(resolution["candidate"]), self.workspace.resolve())
        self.assertEqual(resolution["record_layout"], "legacy-selected-stage1")
        self.assertNotIn(
            "generation_runtime_metrics_sha256", resolution["hashes"]
        )
        self.assertTrue(
            resolution["integrity"][
                "manifest_reference_semantics_hash_matches_trusted"
            ]
        )

    def test_fresh_no_kit_candidate_without_proof_document_is_auditable(
        self,
    ) -> None:
        (self.workspace / "PROOF.md").unlink()
        run_path = self.repo / f"runs/{self.run_id}/run.json"
        run = json.loads(run_path.read_text())
        run["config"] = "codex-gpt-audited-xhigh-semantics"
        run["condition"] = {
            "name": "semantics",
            "kit": False,
            "semantics": True,
        }
        run_path.write_text(json.dumps(run) + "\n")
        task_path = self.task / "task.json"
        task = json.loads(task_path.read_text())
        task["condition"] = run["condition"]
        task_path.write_text(json.dumps(task) + "\n")
        result_path = self.task / "01-k-proof/result.json"
        result = json.loads(result_path.read_text())
        result["outputs"]["workspace_sha256"] = pipeline_contract.sha256_tree(
            self.workspace
        )
        result_path.write_text(json.dumps(result) + "\n")

        resolution = audit_contract.resolve_stage2_audit(
            self.repo, self.run_id, self.PROBLEM
        )

        self.assertEqual(Path(resolution["candidate"]), self.workspace.resolve())

    def test_non_success_stage1_result_is_refused(self) -> None:
        result = self.task / "01-k-proof/result.json"
        document = json.loads(result.read_text())
        document["status"] = "TIMEOUT"
        result.write_text(json.dumps(document) + "\n")
        with self.assertRaisesRegex(audit_contract.AuditContractError, "SUCCEEDED"):
            audit_contract.resolve_stage2_audit(
                self.repo, self.run_id, self.PROBLEM
            )

    def test_incomplete_input_provenance_blocks_stage2_entrypoints(self) -> None:
        self.mark_input_provenance_incomplete()

        for entrypoint in (
            audit_contract.resolve_stage2_audit,
            audit_contract.stage2_eligibility,
        ):
            with self.subTest(entrypoint=entrypoint.__name__):
                with self.assertRaisesRegex(
                    audit_contract.AuditContractError,
                    "INPUT_PROVENANCE_INCOMPLETE",
                ):
                    entrypoint(self.repo, self.run_id, self.PROBLEM)


class Stage2ExecutionTests(Stage2AuditFixture):
    def test_pipeline_launcher_records_usage_around_selection(self) -> None:
        launcher = (
            Path(__file__).resolve().parent.parent
            / "docker/audit/run_task.sh"
        ).read_text()
        write_usage = (
            'usage_accounting.py" write '
            '--trace "$OUTPUT/codex-trace" '
            '--output "$OUTPUT/usage.json"'
        )
        summarize = (
            'flock "$REPO/runs/$CONFIG/.usage-summary.lock" '
            'python3 "$REPO/tools/usage_accounting.py" summarize '
            '--run "$REPO/runs/$CONFIG"'
        )

        self.assertIn(write_usage, launcher)
        self.assertIn(summarize, launcher)
        self.assertIn("MODEL_TRACE_AVAILABLE", launcher)
        self.assertIn('-d "$OUTPUT/codex-trace"', launcher)
        self.assertLess(launcher.index(write_usage), launcher.index("select_stage_output"))
        self.assertGreater(launcher.index(summarize), launcher.index("select_stage_output"))

    def test_first_execution_is_exact_001_and_pass_is_stage3_eligible(self) -> None:
        execution = audit_contract.prepare_stage2_execution(
            self.repo, self.run_id, self.PROBLEM
        )
        self.assertEqual(execution.name, "001")
        self.assertEqual(
            execution.parent,
            self.task / "02-k-audit/executions",
        )
        self.complete_audit(execution)
        (execution / "usage.json").unlink()
        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError, "usage.json"
        ):
            pipeline_contract.select_stage_output(
                self.repo, self.run_id, self.PROBLEM, "02-k-audit", "001"
            )
        usage_accounting.write_trace_usage(
            execution / "codex-trace",
            execution / "usage.json",
        )
        selected = pipeline_contract.select_stage_output(
            self.repo, self.run_id, self.PROBLEM, "02-k-audit", "001"
        )
        self.assertEqual(selected["relative_path"], "executions/001")
        eligibility = audit_contract.stage2_eligibility(
            self.repo, self.run_id, self.PROBLEM
        )
        self.assertTrue(eligibility["eligible"])
        self.assertEqual(eligibility["verdict"], "PASS")
        self.assertEqual(eligibility["legitimacy"], "LEGIT")
        self.assertEqual(
            eligibility["selected_relative_path"], "executions/001"
        )
        self.assertEqual(
            eligibility["selected_artifact_sha256"],
            selected["artifact_sha256"],
        )

    def test_concerns_is_eligible_and_fail_is_terminal_ineligible(self) -> None:
        cases = (
            ("CONCERNS", "LEGIT", True),
            ("FAIL", "NOT_LEGIT", False),
        )
        for index, (verdict, legitimacy, eligible) in enumerate(cases):
            if index:
                other = "19-sort-numbers"
                self.make_problem(other)
                pipeline_contract.create_run(
                    self.repo,
                    run_id="stage2-fail",
                    config="codex-gpt-audited-xhigh-kit-semantics",
                    problem_ids=[other],
                )
                task = self.repo / f"runs/stage2-fail/tasks/{other}"
                workspace = task / "01-k-proof/workspace"
                for name in (
                    "solution.py",
                    "solution.mpy",
                    "verification.k",
                    "spec.k",
                    "prove.sh",
                    "PROOF.md",
                ):
                    (workspace / name).write_text(name + "\n")
                invocation = pipeline_contract.prepare_invocation(
                    self.repo, "stage2-fail", other, "01-k-proof"
                )
                (invocation.path / "codex-output.log").write_text("out\n")
                (invocation.path / "codex-last.txt").write_text("last\n")
                (invocation.path / "runtime-metrics.json").write_text("{}\n")
                (invocation.path / "usage.json").write_text("{}\n")
                (invocation.path / "prompt.txt").write_text("prompt\n")
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
                pipeline_contract.finalize_invocation(
                    self.repo,
                    "stage2-fail",
                    other,
                    "01-k-proof",
                    invocation.name,
                    exit_code=0,
                    duration_s=1,
                    timeout_marker=False,
                    oom_killed=False,
                    image_id="image",
                )
                run_id, problem = "stage2-fail", other
            else:
                run_id, problem = self.run_id, self.PROBLEM
            execution = audit_contract.prepare_stage2_execution(
                self.repo, run_id, problem
            )
            self.complete_audit(
                execution, verdict=verdict, legitimacy=legitimacy
            )
            pipeline_contract.select_stage_output(
                self.repo, run_id, problem, "02-k-audit", "001"
            )
            result = audit_contract.stage2_eligibility(
                self.repo, run_id, problem
            )
            self.assertEqual(result["eligible"], eligible)
            with self.assertRaisesRegex(
                audit_contract.AuditContractError, "terminal"
            ):
                audit_contract.prepare_stage2_execution(
                    self.repo, run_id, problem
                )

    def test_audit_error_permits_002_but_complete_verdict_is_terminal(self) -> None:
        first = audit_contract.prepare_stage2_execution(
            self.repo, self.run_id, self.PROBLEM
        )
        self.complete_audit(
            first,
            audit_status="AUDIT_ERROR",
            verdict=None,
            legitimacy=None,
        )
        (first / "usage.json").unlink()
        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError, "usage.json"
        ):
            pipeline_contract.select_stage_output(
                self.repo,
                self.run_id,
                self.PROBLEM,
                "02-k-audit",
                "001",
            )
        usage_accounting.write_trace_usage(
            first / "codex-trace",
            first / "usage.json",
        )
        pipeline_contract.select_stage_output(
            self.repo, self.run_id, self.PROBLEM, "02-k-audit", "001"
        )

        second = audit_contract.prepare_stage2_execution(
            self.repo, self.run_id, self.PROBLEM
        )
        self.assertEqual(second.name, "002")
        self.complete_audit(second, verdict="PASS", legitimacy="LEGIT")
        pipeline_contract.select_stage_output(
            self.repo, self.run_id, self.PROBLEM, "02-k-audit", "002"
        )
        with self.assertRaisesRegex(
            audit_contract.AuditContractError, "terminal"
        ):
            audit_contract.prepare_stage2_execution(
                self.repo, self.run_id, self.PROBLEM
            )

    def test_explicit_replacement_preserves_terminal_selected_audit(self) -> None:
        first = audit_contract.prepare_stage2_execution(
            self.repo, self.run_id, self.PROBLEM
        )
        self.complete_audit(first, verdict="FAIL", legitimacy="NOT_LEGIT")
        original = pipeline_contract.select_stage_output(
            self.repo, self.run_id, self.PROBLEM, "02-k-audit", "001"
        )

        second = audit_contract.prepare_stage2_execution(
            self.repo,
            self.run_id,
            self.PROBLEM,
            replace_selected=True,
        )

        self.assertEqual(second.name, "002")
        self.assertEqual(
            json.loads(
                (
                    self.repo
                    / "runs"
                    / self.run_id
                    / "tasks"
                    / self.PROBLEM
                    / "02-k-audit"
                    / "selected.json"
                ).read_text()
            ),
            original,
        )
        self.complete_audit(second, verdict="PASS", legitimacy="LEGIT")
        replacement = pipeline_contract.select_stage_output(
            self.repo,
            self.run_id,
            self.PROBLEM,
            "02-k-audit",
            "002",
            replace_selected=True,
        )
        self.assertEqual(replacement["relative_path"], "executions/002")
        self.assertEqual(replacement["replaces"], "executions/001")
        self.assertTrue(first.is_dir())
        self.assertEqual(
            json.loads((first / "verdict.json").read_text())["verdict"],
            "FAIL",
        )

    def test_minimal_infrastructure_error_is_selectable_and_retryable(self) -> None:
        first = audit_contract.prepare_stage2_execution(
            self.repo, self.run_id, self.PROBLEM
        )
        (first / "audit-input.json").write_text("{}\n")
        (first / "verdict.json").write_text(
            json.dumps(
                {
                    "audit_status": "AUDIT_ERROR",
                    "verdict": None,
                    "legitimacy": None,
                    "error": "docker setup failed",
                }
            )
            + "\n"
        )
        selected = pipeline_contract.select_stage_output(
            self.repo, self.run_id, self.PROBLEM, "02-k-audit", first.name
        )
        self.assertEqual(selected["status"], "AUDIT_ERROR")
        self.assertEqual(
            audit_contract.prepare_stage2_execution(
                self.repo, self.run_id, self.PROBLEM
            ).name,
            "002",
        )

    def test_stage2_eligibility_rejects_mutated_selected_audit(self) -> None:
        execution = audit_contract.prepare_stage2_execution(
            self.repo, self.run_id, self.PROBLEM
        )
        self.complete_audit(execution)
        pipeline_contract.select_stage_output(
            self.repo, self.run_id, self.PROBLEM, "02-k-audit", execution.name
        )
        (execution / "REVIEW.md").write_text("mutated\n")
        with self.assertRaisesRegex(
            audit_contract.AuditContractError, "changed after selection"
        ):
            audit_contract.stage2_eligibility(
                self.repo, self.run_id, self.PROBLEM
            )

    def test_selection_refuses_incomplete_audit_artifacts(self) -> None:
        execution = audit_contract.prepare_stage2_execution(
            self.repo, self.run_id, self.PROBLEM
        )
        (execution / "verdict.json").write_text(
            json.dumps(
                {
                    "audit_status": "COMPLETE",
                    "verdict": "PASS",
                    "legitimacy": "LEGIT",
                }
            )
            + "\n"
        )
        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError, "audit-input.json"
        ):
            pipeline_contract.select_stage_output(
                self.repo, self.run_id, self.PROBLEM, "02-k-audit", "001"
            )
