import json
import subprocess
from pathlib import Path
from unittest import mock

from tests.test_stage2_audit import Stage2AuditFixture
from tools import (
    audit_contract,
    lemma_discovery_contract,
    pipeline_contract,
    stage3_runner,
)


class LemmaDiscoveryStageTests(Stage2AuditFixture):
    def setUp(self) -> None:
        super().setUp()
        (self.workspace / "verification.k").write_text(
            "module TEST-VERIFICATION\n"
            "  rule <k> X:Int => X ... </k> [simplification]\n"
            "endmodule\n"
        )
        stage1_result = self.task / "01-k-proof/result.json"
        result = json.loads(stage1_result.read_text())
        result["outputs"]["workspace_sha256"] = pipeline_contract.sha256_tree(
            self.workspace
        )
        stage1_result.write_text(json.dumps(result) + "\n")
        source_prompt = (
            Path(__file__).resolve().parent.parent
            / "prompts/lemma-discovery.md"
        )
        (self.repo / "prompts/lemma-discovery.md").write_bytes(
            source_prompt.read_bytes()
        )

    def select_legit_audit(self, verdict: str = "PASS") -> None:
        execution = audit_contract.prepare_stage2_execution(
            self.repo, self.run_id, self.PROBLEM
        )
        self.complete_audit(
            execution,
            verdict=verdict,
            legitimacy="LEGIT",
        )
        pipeline_contract.select_stage_output(
            self.repo,
            self.run_id,
            self.PROBLEM,
            "02-k-audit",
            execution.name,
        )

    def write_successful_model_output(
        self, invocation: Path, inventory_path: Path
    ) -> None:
        inventory = json.loads(inventory_path.read_text())
        discovery = self.task / "03-lemma-discovery/workspace"
        (discovery / "trust-boundary.json").write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "inventory_sha256": inventory["inventory_sha256"],
                    "rules": [
                        {
                            "source_rule_id": rule["source_rule_id"],
                            "classification": (
                                "DOMAIN_LEMMA"
                                if "simplification" in rule["attributes"]
                                else "OPERATIONAL_RULE"
                            ),
                            "rationale": "Required mathematical bridge.",
                        }
                        for rule in inventory["rules"]
                    ],
                }
            )
            + "\n"
        )
        (discovery / "DISCOVERY.md").write_text(
            "The domain-lemma set is nonempty.\n"
        )
        (invocation / "codex-output.log").write_text("discovery output\n")
        (invocation / "codex-last.txt").write_text(
            "RESULT: LEMMA_DISCOVERY_COMPLETE — classified the inventory\n"
        )
        trace = invocation / "codex-trace"
        trace.mkdir()
        trace.joinpath("rollout.jsonl").write_text(
            json.dumps(
                {
                    "type": "session_meta",
                    "payload": {"id": self.session_id},
                }
            )
            + "\n"
        )
        (invocation / "metrics.json").write_text(
            json.dumps(
                {
                    "model_exit_code": 0,
                    "harness_exit_code": 0,
                    "final_exit_code": 0,
                    "duration_s": 11,
                    "timeout_marker": False,
                    "oom_killed": False,
                }
            )
            + "\n"
        )

    def fake_docker(
        self, calls: list[tuple[list[str], dict[str, str] | None]]
    ):
        def fake_run(command, *args, env=None, **kwargs):
            calls.append((list(command), env))
            if len(command) > 1 and command[1] == "compose":
                self.write_successful_model_output(
                    Path(env["INVOCATION_DIR"]),
                    Path(env["RULE_INVENTORY_PATH"]),
                )
                return subprocess.CompletedProcess(command, 0)
            if len(command) > 1 and command[1] == "inspect":
                return subprocess.CompletedProcess(
                    command,
                    0,
                    stdout=json.dumps(
                        [
                            {
                                "State": {
                                    "ExitCode": 0,
                                    "OOMKilled": False,
                                },
                                "Image": "sha256:lemma-discovery",
                            }
                        ]
                    ),
                    stderr="",
                )
            return subprocess.CompletedProcess(command, 0)

        return fake_run

    def test_requires_selected_legit_stage2_result(self) -> None:
        with self.assertRaisesRegex(
            stage3_runner.Stage3RunnerError, "selected LEGIT"
        ):
            stage3_runner.inspect_stage3(
                self.repo, self.run_id, self.PROBLEM
            )

    def test_valid_config_resumes_stage1_session_without_audit_paths(
        self,
    ) -> None:
        self.select_legit_audit("CONCERNS")

        config = stage3_runner.inspect_stage3(
            self.repo, self.run_id, self.PROBLEM
        )

        self.assertEqual(config["session_id"], self.session_id)
        self.assertEqual(config["timeout_s"], 1200)
        self.assertEqual(
            config["k_reference"],
            str(self.task / "01-k-proof/workspace"),
        )
        self.assertNotIn("k_audit", config)
        self.assertNotIn("02-k-audit", json.dumps(config))

    def test_runner_mounts_only_read_only_canonical_inputs(self) -> None:
        self.select_legit_audit()
        calls: list[tuple[list[str], dict[str, str] | None]] = []

        original_hash = pipeline_contract.sha256_tree(self.workspace)
        with mock.patch.object(
            stage3_runner.subprocess,
            "run",
            side_effect=self.fake_docker(calls),
        ):
            result = stage3_runner.run_stage3(
                self.repo, self.run_id, self.PROBLEM, docker="docker"
            )

        self.assertEqual(result["status"], "SUCCEEDED")
        self.assertEqual(
            pipeline_contract.sha256_tree(self.workspace), original_hash
        )
        compose_call = next(
            (command, env)
            for command, env in calls
            if len(command) > 1 and command[1] == "compose"
        )
        command, environment = compose_call
        self.assertIn("docker/codex/docker-compose.yml", " ".join(command))
        self.assertIn(
            "docker/codex/docker-compose.lemma-discovery.yml",
            " ".join(command),
        )
        self.assertEqual(
            environment["K_REFERENCE_DIR"],
            str(self.task / "01-k-proof/workspace"),
        )
        self.assertEqual(
            environment["WORKSPACE_DIR"],
            str(self.task / "03-lemma-discovery/workspace"),
        )
        self.assertNotIn("K_AUDIT", environment)
        self.assertNotIn("02-k-audit", json.dumps(environment))
        base_compose = (
            Path(__file__).resolve().parent.parent
            / "docker/codex/docker-compose.yml"
        ).read_text()
        compose = (
            Path(__file__).resolve().parent.parent
            / "docker/codex/docker-compose.lemma-discovery.yml"
        ).read_text()
        self.assertIn(
            "${K_REFERENCE_DIR:-/tmp}:/reference/k-proof:ro", compose
        )
        self.assertIn(
            "${RULE_INVENTORY_PATH:-/tmp}:"
            "/reference/rule-inventory.json:ro",
            compose,
        )
        self.assertIn(
            "${WORKSPACE_DIR:-/tmp}:/workspace:rw", base_compose
        )
        self.assertNotIn("/reference/", base_compose)
        self.assertNotIn("K_REFERENCE_DIR", base_compose)
        self.assertNotIn("RULE_INVENTORY_PATH", base_compose)
        self.assertNotIn("LEMMA_DISCOVERY", base_compose)
        self.assertNotIn("02-k-audit", compose)
        protected = (
            self.task
            / "03-lemma-discovery/invocations"
            / result["invocation"]
            / "validated-trust-boundary.json"
        )
        self.assertEqual(
            result["trust_boundary_artifact"],
            "invocations/"
            + result["invocation"]
            + "/validated-trust-boundary.json",
        )
        self.assertEqual(
            result["trust_boundary_sha256"],
            pipeline_contract.sha256_file(protected),
        )
        self.assertEqual(
            result["outputs"]["evidence"][
                "validated-trust-boundary.json"
            ],
            result["trust_boundary_sha256"],
        )

    def test_auth_infrastructure_retry_preserves_failed_invocation(self) -> None:
        self.select_legit_audit()
        inventory_path, _ = stage3_runner._prepare_rule_inventory(
            self.task, self.workspace
        )
        first = pipeline_contract.prepare_invocation(
            self.repo, self.run_id, self.PROBLEM, "03-lemma-discovery"
        )
        (first.path / "codex-output.log").write_text(
            "HTTP 401 token_invalidated\nrefresh_token_invalidated\n"
        )
        pipeline_contract.finalize_invocation(
            self.repo,
            self.run_id,
            self.PROBLEM,
            "03-lemma-discovery",
            first.name,
            exit_code=70,
            duration_s=2,
            timeout_marker=False,
            oom_killed=False,
            image_id="sha256:lemma-discovery",
        )

        retry = stage3_runner._prepare_auth_infrastructure_retry(
            self.repo, self.run_id, self.PROBLEM
        )

        self.assertEqual(retry.name, "002-infrastructure-retry")
        self.assertEqual(retry.kind, "infrastructure-retry")
        retry_document = json.loads(
            (retry.path / "invocation.json").read_text()
        )
        self.assertEqual(retry_document["retry_of"], "001-initial")
        self.assertEqual(
            retry_document["infrastructure_error"]["kind"],
            "codex-auth-token-invalidated",
        )
        self.assertTrue((first.path / "invocation.json").is_file())
        self.assertTrue(inventory_path.is_file())

    def test_auth_infrastructure_retry_rejects_non_auth_failure(self) -> None:
        self.select_legit_audit()
        first = pipeline_contract.prepare_invocation(
            self.repo, self.run_id, self.PROBLEM, "03-lemma-discovery"
        )
        (first.path / "codex-output.log").write_text("ordinary model error\n")
        pipeline_contract.finalize_invocation(
            self.repo,
            self.run_id,
            self.PROBLEM,
            "03-lemma-discovery",
            first.name,
            exit_code=70,
            duration_s=2,
            timeout_marker=False,
            oom_killed=False,
            image_id="sha256:lemma-discovery",
        )

        with self.assertRaisesRegex(
            stage3_runner.Stage3RunnerError, "token invalidation"
        ):
            stage3_runner._prepare_auth_infrastructure_retry(
                self.repo, self.run_id, self.PROBLEM
            )

    def test_manifest_swap_after_validation_cannot_publish_success(
        self,
    ) -> None:
        self.select_legit_audit()
        calls: list[tuple[list[str], dict[str, str] | None]] = []
        real_validate = lemma_discovery_contract.validate_trust_boundary
        live = (
            self.task
            / "03-lemma-discovery/workspace/trust-boundary.json"
        )

        def validate_then_swap(workspace, manifest):
            validated = real_validate(workspace, manifest)
            live.write_text("{}\n")
            return validated

        with (
            mock.patch.object(
                stage3_runner.subprocess,
                "run",
                side_effect=self.fake_docker(calls),
            ),
            mock.patch.object(
                stage3_runner.lemma_discovery_contract,
                "validate_trust_boundary",
                side_effect=validate_then_swap,
            ),
        ):
            result = stage3_runner.run_stage3(
                self.repo, self.run_id, self.PROBLEM, docker="docker"
            )

        invocation = (
            self.task
            / "03-lemma-discovery/invocations"
            / result["invocation"]
        )
        persisted_invocation = json.loads(
            (invocation / "invocation.json").read_text()
        )
        persisted_result = json.loads(
            (
                self.task / "03-lemma-discovery/result.json"
            ).read_text()
        )
        self.assertNotEqual(result["status"], "SUCCEEDED")
        self.assertNotEqual(
            persisted_invocation["status"], "SUCCEEDED"
        )
        self.assertNotEqual(persisted_result["status"], "SUCCEEDED")
        protected = invocation / "validated-trust-boundary.json"
        real_validate(self.workspace, protected)
        self.assertEqual(live.read_text(), "{}\n")

    def test_stage1_mutation_after_model_cannot_leave_public_success(
        self,
    ) -> None:
        self.select_legit_audit()
        calls: list[tuple[list[str], dict[str, str] | None]] = []
        real_run_one = stage3_runner._run_one

        def run_then_mutate(*args, **kwargs):
            outcome = real_run_one(*args, **kwargs)
            (self.workspace / "verification.k").write_text(
                "module MUTATED endmodule\n"
            )
            return outcome

        with (
            mock.patch.object(
                stage3_runner.subprocess,
                "run",
                side_effect=self.fake_docker(calls),
            ),
            mock.patch.object(
                stage3_runner,
                "_run_one",
                side_effect=run_then_mutate,
            ),
            self.assertRaises(stage3_runner.Stage3RunnerError),
        ):
            stage3_runner.run_stage3(
                self.repo,
                self.run_id,
                self.PROBLEM,
                docker="docker",
            )

        invocation = (
            self.task
            / "03-lemma-discovery/invocations/001-initial/invocation.json"
        )
        persisted_invocation = json.loads(invocation.read_text())
        self.assertEqual(
            persisted_invocation["status"], "PREPARED"
        )
        self.assertFalse(
            (self.task / "03-lemma-discovery/result.json").exists()
        )

    def assert_late_finalization_mutation_is_not_published(
        self,
        mutate,
    ) -> None:
        self.select_legit_audit()
        calls: list[tuple[list[str], dict[str, str] | None]] = []
        real_output_hashes = pipeline_contract._invocation_output_hashes
        invocation = (
            self.task
            / "03-lemma-discovery/invocations/001-initial"
        )

        def hash_then_mutate(invocation_path, workspace):
            outputs = real_output_hashes(invocation_path, workspace)
            mutate(invocation)
            return outputs

        with (
            mock.patch.object(
                stage3_runner.subprocess,
                "run",
                side_effect=self.fake_docker(calls),
            ),
            mock.patch.object(
                stage3_runner.pipeline_contract,
                "_invocation_output_hashes",
                side_effect=hash_then_mutate,
            ),
            self.assertRaises(
                (
                    stage3_runner.Stage3RunnerError,
                    pipeline_contract.PipelineContractError,
                )
            ),
        ):
            stage3_runner.run_stage3(
                self.repo,
                self.run_id,
                self.PROBLEM,
                docker="docker",
            )

        persisted = json.loads(
            (invocation / "invocation.json").read_text()
        )
        self.assertEqual(persisted["status"], "PREPARED")
        self.assertFalse(
            (self.task / "03-lemma-discovery/result.json").exists()
        )

    def test_late_stage1_mutation_is_rejected_inside_finalization(
        self,
    ) -> None:
        def mutate(_invocation: Path) -> None:
            (self.workspace / "verification.k").write_text(
                "module LATE-MUTATION endmodule\n"
            )

        self.assert_late_finalization_mutation_is_not_published(mutate)

    def test_late_live_manifest_replacement_is_rejected_inside_finalization(
        self,
    ) -> None:
        def mutate(_invocation: Path) -> None:
            live = (
                self.task
                / "03-lemma-discovery/workspace/trust-boundary.json"
            )
            live.unlink()
            live.write_text("{}\n")

        self.assert_late_finalization_mutation_is_not_published(mutate)

    def test_late_protected_evidence_replacement_is_rejected_before_publication(
        self,
    ) -> None:
        def mutate(invocation: Path) -> None:
            protected = invocation / "validated-trust-boundary.json"
            protected.unlink()
            protected.write_text('{"tampered": true}\n')

        self.assert_late_finalization_mutation_is_not_published(mutate)

    def test_prompt_has_exact_discovery_contract(self) -> None:
        prompt = (
            Path(__file__).resolve().parent.parent
            / "prompts/lemma-discovery.md"
        ).read_text()
        for required in (
            "Do not edit or copy the Stage 1 artifacts.",
            "Classify every rule in /reference/rule-inventory.json exactly once.",
            "Allowed classifications: DEFINITION, OPERATIONAL_RULE,",
            "PROVED_DERIVED_LEMMA, and DOMAIN_LEMMA.",
            "Do not write a Lean theorem statement.",
            "Write /workspace/trust-boundary.json and /workspace/DISCOVERY.md.",
        ):
            self.assertIn(required, prompt)
        marker = "RESULT: LEMMA_DISCOVERY_COMPLETE — <brief summary>"
        self.assertEqual(prompt.count(marker), 1)

    def test_default_budget_does_not_allocate_a_timeout_continuation(
        self,
    ) -> None:
        self.select_legit_audit()
        calls = []

        def fake_run_one(
            repo,
            run_id,
            problem,
            invocation,
            run_manifest,
            state,
            k_reference,
            inventory_path,
            *,
            docker,
            kit_skills=None,
        ):
            calls.append(invocation)
            trace = invocation.path / "codex-trace"
            trace.mkdir()
            trace.joinpath("rollout.jsonl").write_text(
                json.dumps(
                    {
                        "type": "session_meta",
                        "payload": {"id": self.session_id},
                    }
                )
                + "\n"
            )
            return stage3_runner.InvocationOutcome(
                exit_code=143,
                duration_s=1199,
                timeout_marker=True,
                oom_killed=False,
                image_id="sha256:lemma-discovery",
            )

        with mock.patch.object(
            stage3_runner, "_run_one", side_effect=fake_run_one
        ):
            result = stage3_runner.run_stage3(
                self.repo, self.run_id, self.PROBLEM, docker="unused"
            )

        self.assertEqual(result["status"], "TIMEOUT")
        self.assertEqual(
            [invocation.name for invocation in calls], ["001-initial"]
        )

    def test_result_marker_must_be_exact_and_unique(self) -> None:
        final = self.task / "last.txt"
        for content in (
            "RESULT: LEMMA_DISCOVERY_COMPLETE - wrong dash\n",
            "RESULT: LEMMA_DISCOVERY_COMPLETE — okay\n"
            "RESULT: LEMMA_DISCOVERY_COMPLETE — duplicate\n",
        ):
            with self.subTest(content=content):
                final.write_text(content)
                with self.assertRaises(stage3_runner.Stage3RunnerError):
                    stage3_runner.parse_stage3_result(final)

        final.write_text(
            "RESULT: LEMMA_DISCOVERY_COMPLETE — classified all rules\n"
        )
        self.assertEqual(
            stage3_runner.parse_stage3_result(final),
            "classified all rules",
        )

if __name__ == "__main__":
    import unittest

    unittest.main()
