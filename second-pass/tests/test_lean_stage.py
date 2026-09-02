import hashlib
import json
import os
import subprocess
import uuid
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from tests.test_stage2_audit import Stage2AuditFixture
from tools import klean_export, pipeline_contract, stage5_runner


class LeanStageTests(Stage2AuditFixture):
    def setUp(self) -> None:
        super().setUp()
        source_prompt = (
            Path(__file__).resolve().parent.parent
            / "prompts/klean-prove.md"
        )
        (self.repo / "prompts/klean-prove.md").write_bytes(
            source_prompt.read_bytes()
        )
        invocation = pipeline_contract.prepare_invocation(
            self.repo,
            self.run_id,
            self.PROBLEM,
            "03-lemma-discovery",
        )
        protected = invocation.path / "validated-trust-boundary.json"
        protected.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "inventory_sha256": "a" * 64,
                    "rules": [],
                }
            )
            + "\n"
        )
        (invocation.path / "codex-output.log").write_text("discovery\n")
        (invocation.path / "codex-last.txt").write_text(
            "RESULT: LEMMA_DISCOVERY_COMPLETE — test\n"
        )
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
        protected_hash = pipeline_contract.sha256_file(protected)
        pipeline_contract.finalize_invocation(
            self.repo,
            self.run_id,
            self.PROBLEM,
            "03-lemma-discovery",
            invocation.name,
            exit_code=0,
            duration_s=11,
            timeout_marker=False,
            oom_killed=False,
            image_id="sha256:lemma-discovery",
            result_metadata={
                "trust_boundary_sha256": protected_hash,
                "trust_boundary_artifact": (
                    f"invocations/{invocation.name}/"
                    "validated-trust-boundary.json"
                ),
            },
            expected_evidence={
                "validated-trust-boundary.json": protected_hash,
            },
        )
        self.discovery_manifest = protected

        generation = self.task / "04-klean-generation/generations/001"
        generated = generation / "generated/Klean8SumProduct"
        generated.mkdir(parents=True)
        (generation / "generated/Klean8SumProduct.lean").write_text(
            "import Klean8SumProduct.Lemmas\n"
        )
        (generated / "Lemmas.lean").write_text(
            "def targetStatement (helper : Int → Int) : Prop :=\n"
            "  ∀ (I : Int), helper I = I\n"
        )
        (generation / "generated/lean-toolchain").write_text(
            "leanprover/lean4:v4.22.0\n"
        )
        (generation / "generated/lakefile.toml").write_text(
            'name = "klean-8-sum-product"\n'
        )
        binding = {
            "kore_symbol": "helper",
            "name": "helper",
            "type": "Int → Int",
            "source_rule_ids": ["rule-" + "a" * 64],
        }
        binding["binding_sha256"] = hashlib.sha256(
            json.dumps(
                binding, sort_keys=True, separators=(",", ":")
            ).encode()
        ).hexdigest()
        target = {
            "declaration": "Klean8SumProduct.Lemmas.targetStatement",
            "file": "Klean8SumProduct/Lemmas.lean",
            "statement": "Klean8SumProduct.Lemmas.targetStatement helper",
            "statement_sha256": "unused",
            "parameters": [binding],
        }
        stage1_hash = klean_export.tree_digest(self.workspace)
        generated_hash = klean_export.tree_digest(
            generation / "generated"
        )
        (generation / "input-manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": 3,
                    "problem": self.PROBLEM,
                    "frozen_input_sha256": stage1_hash,
                    "stage1_workspace_sha256": stage1_hash,
                    "stage3_discovery_manifest_sha256": protected_hash,
                }
            )
            + "\n"
        )
        (generation / "generator-manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": 3,
                    "generated_tree_sha256": generated_hash,
                    "obligation_count": 1,
                    "provenance": {
                        "stage1_workspace_sha256": stage1_hash,
                        "stage3_discovery_manifest_sha256": protected_hash,
                    },
                    "target": target,
                    "toolchain": {
                        "lean_toolchain": "leanprover/lean4:v4.22.0",
                    },
                }
            )
            + "\n"
        )
        inventory = generation / "trust-inventory.json"
        inventory.write_text('{"allowlist": []}\n')
        (generation / "export-result.json").write_text(
            json.dumps(
                {
                    "schema_version": 3,
                    "status": "OK",
                    "problem": self.PROBLEM,
                    "frozen_input_sha256": stage1_hash,
                    "stage3_discovery_manifest_sha256": protected_hash,
                    "generated_tree_sha256": generated_hash,
                    "trust_inventory_sha256": hashlib.sha256(
                        inventory.read_bytes()
                    ).hexdigest(),
                    "obligation_count": 1,
                }
            )
            + "\n"
        )
        (generation / "export.log").write_text("export\n")
        (generation / "preflight.log").write_text("pass\n")
        (generation / "preflight.json").write_text(
            json.dumps(
                {
                    "schema_version": 3,
                    "status": "PASS",
                    "stage1_workspace_sha256": stage1_hash,
                    "stage3_discovery_manifest_sha256": protected_hash,
                    "generated_tree_sha256": generated_hash,
                    "obligation_count": 1,
                }
            )
            + "\n"
        )
        self.selection = pipeline_contract.select_stage_output(
            self.repo,
            self.run_id,
            self.PROBLEM,
            "04-klean-generation",
            "001",
            expected_candidate_sha256=pipeline_contract.sha256_tree(
                generation
            ),
        )
        self.generation = generation

    @staticmethod
    def successful_outcome(duration_s: int = 9) -> SimpleNamespace:
        return SimpleNamespace(
            exit_code=0,
            duration_s=duration_s,
            timeout_marker=False,
            oom_killed=False,
            image_id="sha256:" + "1" * 64,
        )

    def successful_mechanical_check(
        self, _image_id, generation, candidate, *, docker
    ) -> dict[str, object]:
        return {
            "status": "PASS",
            "target": json.loads(
                (generation / "generator-manifest.json").read_text()
            )["target"],
            "generation_sha256": klean_export.tree_digest(generation),
            "candidate_sha256": klean_export.tree_digest(candidate),
            "used_axioms": [],
            "diagnostics": [],
        }

    def write_matching_trace(self, invocation: Path) -> None:
        self.write_trace_for_session(invocation, self.session_id)
        (invocation / "codex-last.txt").write_text(
            "RESULT: LEAN_PROOF_COMPLETE — completed the fixed proof\n"
        )

    def write_trace_for_session(
        self, invocation: Path, session_id: str
    ) -> None:
        trace = invocation / "codex-trace"
        trace.mkdir()
        trace.joinpath("rollout.jsonl").write_text(
            json.dumps(
                {
                    "type": "session_meta",
                    "payload": {"id": session_id},
                }
            )
            + "\n"
        )

    @staticmethod
    def rewrite_json(path: Path, **updates) -> None:
        document = json.loads(path.read_text())
        document.update(updates)
        path.write_text(json.dumps(document) + "\n")

    def test_replaced_session_state_cannot_supplant_stage1_uuid(
        self,
    ) -> None:
        replacement = str(uuid.uuid4())
        state = (
            self.repo
            / f"runner-state/{self.run_id}/{self.PROBLEM}/session.json"
        )
        self.rewrite_json(state, session_id=replacement)

        def fake_run(*args, **kwargs):
            invocation = args[3]
            self.write_trace_for_session(invocation.path, replacement)
            return self.successful_outcome()

        with (
            mock.patch.object(stage5_runner, "_run_one", fake_run),
            self.assertRaisesRegex(
                stage5_runner.Stage5RunnerError,
                "canonical|Stage 1",
            ),
        ):
            stage5_runner.run_stage5(
                self.repo, self.run_id, self.PROBLEM, docker="unused"
            )

        self.assertEqual(
            list(
                (
                    self.task / "05-lean-proof/invocations"
                ).iterdir()
            ),
            [],
        )
        self.assertFalse(
            (self.task / "05-lean-proof/result.json").exists()
        )

    def test_late_stage3_invocation_uuid_substitution_cannot_publish(
        self,
    ) -> None:
        stage3 = json.loads(
            (
                self.task / "03-lemma-discovery/result.json"
            ).read_text()
        )
        stage3_invocation = (
            self.task
            / "03-lemma-discovery/invocations"
            / stage3["invocation"]
            / "invocation.json"
        )

        def fake_run(*args, **kwargs):
            invocation = args[3]
            self.write_matching_trace(invocation.path)
            self.rewrite_json(
                stage3_invocation, session_id=str(uuid.uuid4())
            )
            return self.successful_outcome()

        with (
            mock.patch.object(stage5_runner, "_run_one", fake_run),
            self.assertRaisesRegex(
                stage5_runner.Stage5RunnerError,
                "canonical|Stage 3",
            ),
        ):
            stage5_runner.run_stage5(
                self.repo, self.run_id, self.PROBLEM, docker="unused"
            )

        invocation = (
            self.task
            / "05-lean-proof/invocations/001-initial/invocation.json"
        )
        self.assertEqual(
            json.loads(invocation.read_text())["status"], "PREPARED"
        )
        self.assertFalse(
            (self.task / "05-lean-proof/result.json").exists()
        )

    def test_valid_lean_completion_marker_is_parsed(self) -> None:
        final = self.repo / "valid-lean-final.txt"
        final.write_text(
            "Proof completed.\n"
            "RESULT: LEAN_PROOF_COMPLETE — discharged the obligation\n"
        )

        self.assertEqual(
            stage5_runner.parse_stage5_result(final),
            "discharged the obligation",
        )

    def test_missing_lean_completion_marker_is_rejected(self) -> None:
        final = self.repo / "missing-lean-final.txt"
        final.write_text("Proof completed without a result marker.\n")

        with self.assertRaisesRegex(
            stage5_runner.Stage5RunnerError, "exactly one RESULT"
        ):
            stage5_runner.parse_stage5_result(final)

    def test_duplicate_lean_completion_marker_is_rejected(self) -> None:
        final = self.repo / "duplicate-lean-final.txt"
        final.write_text(
            "RESULT: LEAN_PROOF_COMPLETE — first\n"
            "RESULT: LEAN_PROOF_COMPLETE — second\n"
        )

        with self.assertRaisesRegex(
            stage5_runner.Stage5RunnerError, "exactly one RESULT"
        ):
            stage5_runner.parse_stage5_result(final)

    def test_malformed_lean_completion_marker_is_rejected(self) -> None:
        final = self.repo / "malformed-lean-final.txt"
        final.write_text(
            "RESULT: LEAN_PROOF_COMPLETE - wrong dash\n"
        )

        with self.assertRaisesRegex(
            stage5_runner.Stage5RunnerError, "malformed"
        ):
            stage5_runner.parse_stage5_result(final)

    def test_clean_exit_without_completion_marker_is_failed(self) -> None:
        def fake_run(*args, **kwargs):
            invocation = args[3]
            self.write_trace_for_session(
                invocation.path, self.session_id
            )
            return self.successful_outcome()

        with mock.patch.object(stage5_runner, "_run_one", fake_run):
            result = stage5_runner.run_stage5(
                self.repo, self.run_id, self.PROBLEM, docker="unused"
            )

        self.assertEqual(result["status"], "FAILED")
        invocation = (
            self.task
            / "05-lean-proof/invocations/001-initial/invocation.json"
        )
        self.assertEqual(
            json.loads(invocation.read_text())["status"], "FAILED"
        )

    def test_completion_marker_cannot_publish_without_mechanical_pass(
        self,
    ) -> None:
        def fake_run(*args, **kwargs):
            invocation = args[3]
            proof = self.task / "05-lean-proof/workspace/Proof.lean"
            proof.write_text(proof.read_text().replace("sorry", "constructor"))
            self.write_matching_trace(invocation.path)
            return self.successful_outcome()

        with (
            mock.patch.object(stage5_runner, "_run_one", fake_run),
            mock.patch.object(
                stage5_runner,
                "_run_mechanical_check",
                return_value={
                    "status": "FAIL",
                    "error": "lake build failed with unsolved goals",
                },
            ),
        ):
            result = stage5_runner.run_stage5(
                self.repo, self.run_id, self.PROBLEM, docker="unused"
            )

        self.assertEqual(result["status"], "FAILED")
        invocation = (
            self.task
            / "05-lean-proof/invocations/001-initial/lean-validation.json"
        )
        self.assertEqual(json.loads(invocation.read_text())["status"], "FAIL")

    def test_late_completion_marker_mutation_cannot_publish(self) -> None:
        original_output_hashes = (
            pipeline_contract._invocation_output_hashes
        )

        def fake_run(*args, **kwargs):
            invocation = args[3]
            self.write_matching_trace(invocation.path)
            return self.successful_outcome()

        def mutate_after_output_hash(*args, **kwargs):
            outputs = original_output_hashes(*args, **kwargs)
            invocation = args[0]
            (invocation / "codex-last.txt").write_text(
                "RESULT: LEAN_PROOF_COMPLETE - malformed late marker\n"
            )
            return outputs

        with (
            mock.patch.object(stage5_runner, "_run_one", fake_run),
            mock.patch.object(
                stage5_runner,
                "_run_mechanical_check",
                self.successful_mechanical_check,
            ),
            mock.patch.object(
                pipeline_contract,
                "_invocation_output_hashes",
                mutate_after_output_hash,
            ),
            self.assertRaisesRegex(
                stage5_runner.Stage5RunnerError,
                "malformed|completion evidence",
            ),
        ):
            stage5_runner.run_stage5(
                self.repo, self.run_id, self.PROBLEM, docker="unused"
            )

        invocation = (
            self.task
            / "05-lean-proof/invocations/001-initial/invocation.json"
        )
        self.assertEqual(
            json.loads(invocation.read_text())["status"], "PREPARED"
        )
        self.assertFalse(
            (self.task / "05-lean-proof/result.json").exists()
        )

    def test_late_completion_marker_symlink_cannot_publish(self) -> None:
        original_output_hashes = (
            pipeline_contract._invocation_output_hashes
        )

        def fake_run(*args, **kwargs):
            invocation = args[3]
            self.write_matching_trace(invocation.path)
            return self.successful_outcome()

        def link_after_output_hash(*args, **kwargs):
            outputs = original_output_hashes(*args, **kwargs)
            invocation = args[0]
            final = invocation / "codex-last.txt"
            replacement = self.repo / "linked-lean-final.txt"
            replacement.write_bytes(final.read_bytes())
            final.unlink()
            os.symlink(replacement, final)
            return outputs

        with (
            mock.patch.object(stage5_runner, "_run_one", fake_run),
            mock.patch.object(
                stage5_runner,
                "_run_mechanical_check",
                self.successful_mechanical_check,
            ),
            mock.patch.object(
                pipeline_contract,
                "_invocation_output_hashes",
                link_after_output_hash,
            ),
            self.assertRaisesRegex(
                stage5_runner.Stage5RunnerError,
                "real regular file|completion evidence",
            ),
        ):
            stage5_runner.run_stage5(
                self.repo, self.run_id, self.PROBLEM, docker="unused"
            )

        invocation = (
            self.task
            / "05-lean-proof/invocations/001-initial/invocation.json"
        )
        self.assertEqual(
            json.loads(invocation.read_text())["status"], "PREPARED"
        )
        self.assertFalse(
            (self.task / "05-lean-proof/result.json").exists()
        )

    def test_inspection_resolves_stage5_session_budget_and_inputs(
        self,
    ) -> None:
        config = stage5_runner.inspect_stage5(
            self.repo, self.run_id, self.PROBLEM
        )

        self.assertEqual(config["session_id"], self.session_id)
        self.assertEqual(config["initial_timeout_s"], 3600)
        self.assertEqual(config["total_timeout_s"], 7200)
        self.assertEqual(
            config["stage3_discovery"], str(self.discovery_manifest)
        )
        self.assertEqual(
            config["stage4_generation"], str(self.generation)
        )
        self.assertEqual(
            config["workspace"],
            str(self.task / "05-lean-proof/workspace"),
        )
        self.assertNotIn("02-k-audit", json.dumps(config))

    def test_separate_stage_resumes_original_session_and_builds_exact_template(
        self,
    ) -> None:
        original_hash = pipeline_contract.sha256_tree(self.workspace)
        seen = []

        def fake_run(
            repo,
            run_id,
            problem,
            invocation,
            run_manifest,
            state,
            k_reference,
            discovery,
            generation,
            *,
            docker,
        ):
            seen.append(invocation)
            proof = self.task / "05-lean-proof/workspace/Proof.lean"
            proof.write_text(
                proof.read_text()
                .replace("axiom helper : Int → Int", "def helper : Int → Int := id")
                .replace("sorry", "trivial")
            )
            self.write_matching_trace(invocation.path)
            return self.successful_outcome()

        with (
            mock.patch.object(stage5_runner, "_run_one", fake_run),
            mock.patch.object(
                stage5_runner,
                "_run_mechanical_check",
                self.successful_mechanical_check,
            ),
        ):
            result = stage5_runner.run_stage5(
                self.repo, self.run_id, self.PROBLEM, docker="unused"
            )

        self.assertEqual(result["status"], "SUCCEEDED")
        self.assertEqual(seen[0].kind, "stage-resume")
        self.assertEqual(seen[0].session_id, self.session_id)
        proof = self.task / "05-lean-proof/workspace/Proof.lean"
        self.assertIn("theorem final", proof.read_text())
        self.assertIn("def helper : Int → Int := id", proof.read_text())
        self.assertIn("KORE symbol: helper", proof.read_text())
        self.assertIn(
            "Klean8SumProduct.Lemmas.targetStatement helper",
            proof.read_text(),
        )
        self.assertNotIn("sorry", proof.read_text())
        self.assertIn(
            "@[default_target]",
            (
                self.task / "05-lean-proof/workspace/lakefile.lean"
            ).read_text(),
        )
        self.assertEqual(
            pipeline_contract.sha256_tree(self.workspace), original_hash
        )

    def test_stage5_accepts_authenticated_subagent_trace_descendant(self) -> None:
        def fake_run(*args, **kwargs):
            invocation = args[3]
            proof = self.task / "05-lean-proof/workspace/Proof.lean"
            proof.write_text(proof.read_text().replace("sorry", "trivial"))
            self.write_matching_trace(invocation.path)
            child_id = str(uuid.uuid4())
            child = invocation.path / "codex-trace/subagent.jsonl"
            child.write_text(
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
            return self.successful_outcome()

        with (
            mock.patch.object(stage5_runner, "_run_one", fake_run),
            mock.patch.object(
                stage5_runner,
                "_run_mechanical_check",
                self.successful_mechanical_check,
            ),
        ):
            result = stage5_runner.run_stage5(
                self.repo, self.run_id, self.PROBLEM, docker="unused"
            )

        self.assertEqual(result["status"], "SUCCEEDED")

    def test_lean_timeout_uses_full_stage5_continuation_budget(self) -> None:
        calls = []

        def fake_run(
            repo,
            run_id,
            problem,
            invocation,
            run_manifest,
            state,
            k_reference,
            discovery,
            generation,
            *,
            docker,
        ):
            calls.append(invocation)
            self.write_matching_trace(invocation.path)
            if len(calls) == 1:
                return SimpleNamespace(
                    exit_code=143,
                    duration_s=3600,
                    timeout_marker=True,
                    oom_killed=False,
                    image_id="sha256:" + "1" * 64,
                )
            return self.successful_outcome(4)

        with (
            mock.patch.object(stage5_runner, "_run_one", fake_run),
            mock.patch.object(
                stage5_runner,
                "_run_mechanical_check",
                self.successful_mechanical_check,
            ),
        ):
            result = stage5_runner.run_stage5(
                self.repo, self.run_id, self.PROBLEM, docker="unused"
            )

        self.assertEqual(result["status"], "SUCCEEDED")
        self.assertEqual(
            [invocation.name for invocation in calls],
            ["001-initial", "002-timeout-resume"],
        )
        self.assertEqual(
            [invocation.allocation_s for invocation in calls], [3600, 3600]
        )
        self.assertTrue(
            all(item.session_id == self.session_id for item in calls)
        )

    def test_runner_mounts_only_stage1_stage3_stage4_as_read_only_inputs(
        self,
    ) -> None:
        calls: list[tuple[list[str], dict[str, str] | None]] = []

        def fake_subprocess(command, *args, env=None, **kwargs):
            calls.append((list(command), env))
            if len(command) > 1 and command[1] == "compose":
                invocation = Path(env["INVOCATION_DIR"])
                (invocation / "metrics.json").write_text(
                    json.dumps(
                        {
                            "model_exit_code": 0,
                            "harness_exit_code": 0,
                            "final_exit_code": 0,
                            "duration_s": 9,
                            "timeout_marker": False,
                            "oom_killed": False,
                        }
                    )
                    + "\n"
                )
                self.write_matching_trace(invocation)
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
                                "Image": "sha256:" + "1" * 64,
                            }
                        ]
                    ),
                    stderr="",
                )
            return subprocess.CompletedProcess(command, 0)

        with mock.patch.object(
            stage5_runner.subprocess,
            "run",
            side_effect=fake_subprocess,
        ), mock.patch.object(
            stage5_runner,
            "_run_mechanical_check",
            self.successful_mechanical_check,
        ):
            result = stage5_runner.run_stage5(
                self.repo, self.run_id, self.PROBLEM, docker="docker"
            )

        self.assertEqual(result["status"], "SUCCEEDED")
        command, environment = next(
            (command, environment)
            for command, environment in calls
            if len(command) > 1 and command[1] == "compose"
        )
        self.assertIn(
            "docker/codex/docker-compose.klean.yml", " ".join(command)
        )
        self.assertEqual(
            environment["WORKSPACE_DIR"],
            str(self.task / "05-lean-proof/workspace"),
        )
        self.assertEqual(
            environment["K_REFERENCE_DIR"],
            str(self.task / "01-k-proof/workspace"),
        )
        self.assertEqual(
            environment["STAGE3_DISCOVERY_PATH"],
            str(self.discovery_manifest),
        )
        self.assertEqual(
            environment["GENERATED_DIR"],
            str(self.generation / "generated"),
        )
        self.assertNotIn("K_AUDIT", environment)
        self.assertNotIn("02-k-audit", json.dumps(environment))
        base = (
            Path(__file__).resolve().parent.parent
            / "docker/codex/docker-compose.yml"
        ).read_text()
        compose = (
            Path(__file__).resolve().parent.parent
            / "docker/codex/docker-compose.klean.yml"
        ).read_text()
        self.assertIn(
            "${WORKSPACE_DIR:-/tmp}:/workspace:rw", base
        )
        for mount in (
            "${K_REFERENCE_DIR:-/tmp}:/reference/k-proof:ro",
            "${STAGE3_DISCOVERY_PATH:-/tmp}:"
            "/reference/trust-boundary.json:ro",
            "${GENERATED_DIR:-/tmp}:/workspace/Base:ro",
            "${LEAN_LAKEFILE_PATH:-/tmp}:"
            "/workspace/lakefile.lean:ro",
            "${LEAN_TOOLCHAIN_PATH:-/tmp}:"
            "/workspace/lean-toolchain:ro",
        ):
            self.assertIn(mount, compose)
        self.assertNotIn(":rw", compose)
        self.assertNotIn("02-k-audit", compose)
        self.assertNotIn("preflight", compose)

    def test_stage3_mutation_after_model_cannot_publish_stage5_success(
        self,
    ) -> None:
        def mutate_after_model(*args, **kwargs):
            invocation = args[3]
            self.write_matching_trace(invocation.path)
            self.discovery_manifest.write_text("{}\n")
            return self.successful_outcome()

        with (
            mock.patch.object(
                stage5_runner, "_run_one", mutate_after_model
            ),
            self.assertRaisesRegex(
                stage5_runner.Stage5RunnerError, "Stage 3"
            ),
        ):
            stage5_runner.run_stage5(
                self.repo, self.run_id, self.PROBLEM, docker="unused"
            )

        invocation = (
            self.task
            / "05-lean-proof/invocations/001-initial/invocation.json"
        )
        self.assertEqual(
            json.loads(invocation.read_text())["status"], "PREPARED"
        )
        self.assertFalse(
            (self.task / "05-lean-proof/result.json").exists()
        )

    def test_stage4_mutation_after_model_cannot_publish_stage5_success(
        self,
    ) -> None:
        def mutate_after_model(*args, **kwargs):
            invocation = args[3]
            self.write_matching_trace(invocation.path)
            (self.generation / "generated/Injected.lean").write_text(
                "theorem injected : True := by sorry\n"
            )
            return self.successful_outcome()

        with (
            mock.patch.object(
                stage5_runner, "_run_one", mutate_after_model
            ),
            self.assertRaisesRegex(
                stage5_runner.Stage5RunnerError, "Stage 4"
            ),
        ):
            stage5_runner.run_stage5(
                self.repo, self.run_id, self.PROBLEM, docker="unused"
            )

        self.assertFalse(
            (self.task / "05-lean-proof/result.json").exists()
        )

    def test_no_obligations_skips_stage5_without_invocation(self) -> None:
        preflight_path = self.generation / "preflight.json"
        preflight = json.loads(preflight_path.read_text())
        preflight.update(
            {"status": "KLEAN_NO_OBLIGATIONS", "obligation_count": 0}
        )
        preflight_path.write_text(json.dumps(preflight) + "\n")
        manifest_path = self.generation / "generator-manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["obligation_count"] = 0
        manifest_path.write_text(json.dumps(manifest) + "\n")
        export_path = self.generation / "export-result.json"
        export = json.loads(export_path.read_text())
        export.update(
            {"status": "KLEAN_NO_OBLIGATIONS", "obligation_count": 0}
        )
        export_path.write_text(json.dumps(export) + "\n")
        selection_path = self.task / "04-klean-generation/selected.json"
        selection = json.loads(selection_path.read_text())
        selection.update(
            {
                "status": "KLEAN_NO_OBLIGATIONS",
                "artifact_sha256": pipeline_contract.sha256_tree(
                    self.generation
                ),
            }
        )
        selection_path.write_text(json.dumps(selection) + "\n")

        with mock.patch.object(stage5_runner, "_run_one") as run_one:
            result = stage5_runner.run_stage5(
                self.repo, self.run_id, self.PROBLEM, docker="unused"
            )

        self.assertEqual(result["status"], "KLEAN_NO_OBLIGATIONS")
        self.assertTrue(result["skipped"])
        run_one.assert_not_called()
        self.assertEqual(
            list(
                (
                    self.task / "05-lean-proof/invocations"
                ).iterdir()
            ),
            [],
        )
        self.assertEqual(
            list((self.task / "05-lean-proof/workspace").iterdir()),
            [],
        )
        self.assertFalse(
            (self.task / "05-lean-proof/result.json").exists()
        )

    def test_incomplete_input_provenance_blocks_stage5_launch(self) -> None:
        self.mark_input_provenance_incomplete()

        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError,
            "INPUT_PROVENANCE_INCOMPLETE",
        ):
            stage5_runner.run_stage5(
                self.repo, self.run_id, self.PROBLEM, docker="unused"
            )

    def test_quoted_klean_identifier_is_safe_and_binding_is_enforced(
        self,
    ) -> None:
        self.assertTrue(stage5_runner._safe_lean_identifier("«_+Int_»"))
        self.assertFalse(
            stage5_runner._safe_lean_identifier("«bad»\naxiom x")
        )
        manifest = json.loads(
            (self.generation / "generator-manifest.json").read_text()
        )
        manifest["target"]["parameters"][0]["kore_symbol"] = "changed"
        with self.assertRaisesRegex(
            stage5_runner.Stage5RunnerError, "binding changed"
        ):
            stage5_runner._initialize_workspace(
                self.task / "05-lean-proof/other-workspace",
                manifest,
                self.PROBLEM,
            )

    def test_resume_rejects_linked_immutable_workspace_files(self) -> None:
        workspace = self.task / "05-lean-proof/workspace"
        manifest = json.loads(
            (self.generation / "generator-manifest.json").read_text()
        )
        stage5_runner._initialize_workspace(
            workspace, manifest, self.PROBLEM
        )
        lakefile = workspace / "lakefile.lean"
        replacement = self.repo / "linked-lakefile.lean"
        replacement.write_bytes(lakefile.read_bytes())
        lakefile.unlink()
        os.symlink(replacement, lakefile)

        with self.assertRaisesRegex(
            (
                pipeline_contract.PipelineContractError,
                stage5_runner.Stage5RunnerError,
            ),
            "regular|linked",
        ):
            stage5_runner._initialize_workspace(
                workspace, manifest, self.PROBLEM
            )

    def test_stage5_prompt_forbids_audit_access_and_trust_escapes(
        self,
    ) -> None:
        prompt = (
            Path(__file__).resolve().parent.parent
            / "prompts/klean-prove.md"
        ).read_text()
        self.assertIn("Do not read audit output", prompt)
        self.assertIn("fixed theorem statement", " ".join(prompt.split()))
        self.assertIn(
            "RESULT: LEAN_PROOF_COMPLETE — <brief summary>", prompt
        )
        for forbidden in ("axiom", "sorry", "admit", "unsafe", "opaque"):
            self.assertIn(forbidden, prompt)

    def test_agent_image_contains_the_pinned_lean_and_klean_toolchain(
        self,
    ) -> None:
        dockerfile = (
            Path(__file__).resolve().parent.parent
            / "docker/codex/Dockerfile"
        ).read_text()
        self.assertIn(
            "K_COMMIT=ff15baac9e66426612ec45ff912af7f14965b64a",
            dockerfile,
        )
        self.assertIn(
            "LEAN_TOOLCHAIN=leanprover/lean4:v4.22.0", dockerfile
        )
        self.assertIn(
            "/opt/runtimeverification-k/pyk/.venv/bin", dockerfile
        )
        self.assertIn("tools/klean.py", dockerfile)


if __name__ == "__main__":
    import unittest

    unittest.main()
