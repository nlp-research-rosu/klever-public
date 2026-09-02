import errno
import hashlib
import json
import os
import shutil
from pathlib import Path
from unittest import mock

from tests.test_stage2_audit import Stage2AuditFixture
from tools import audit_contract, pipeline_contract, stage4_runner
from tools.k_rule_inventory import inventory_verification


class KleanLauncherTests(Stage2AuditFixture):
    def setUp(self) -> None:
        super().setUp()
        (self.workspace / "verification.k").write_text(
            "module TEST-VERIFICATION\n"
            "  imports TEST-SYNTAX\n"
            "  rule X +Int 0 => X [simplification]\n"
            "endmodule\n"
        )
        (self.workspace / "syntax.k").write_text(
            "module TEST-SYNTAX\nendmodule\n"
        )
        stage1_result = self.task / "01-k-proof/result.json"
        stage1 = json.loads(stage1_result.read_text())
        stage1["outputs"]["workspace_sha256"] = (
            pipeline_contract.sha256_tree(self.workspace)
        )
        stage1_result.write_text(json.dumps(stage1) + "\n")
        execution = audit_contract.prepare_stage2_execution(
            self.repo, self.run_id, self.PROBLEM
        )
        self.complete_audit(execution)
        pipeline_contract.select_stage_output(
            self.repo, self.run_id, self.PROBLEM, "02-k-audit", "001"
        )
        inventory = inventory_verification(self.workspace)
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
                    "inventory_sha256": inventory["inventory_sha256"],
                    "rules": [
                        {
                            "source_rule_id": rule["source_rule_id"],
                            "classification": "DOMAIN_LEMMA",
                            "rationale": "Required test domain lemma.",
                        }
                        for rule in inventory["rules"]
                    ],
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
        self.stage3_result = pipeline_contract.finalize_invocation(
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
                "validated-trust-boundary.json": protected_hash
            },
        )
        self.protected_manifest = protected
        self.fake_root = self.repo / "fake-klean"
        self.fake_root.mkdir()
        self.calls = self.fake_root / "calls.jsonl"
        self.scenarios = self.fake_root / "scenarios.json"
        self.fake_docker = self.repo / "fake-docker-klean"
        self.fake_docker.write_text(
            """#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path
import sys

def tree_digest(root):
    digest = hashlib.sha256()
    entries = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            relative = path.relative_to(root).as_posix()
            if child.is_dir(follow_symlinks=False):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif child.is_file(follow_symlinks=False):
                entries.append((relative, "file", path))
            else:
                raise RuntimeError(f"unsafe tree entry: {path}")
    for relative, kind, path in sorted(entries):
        digest.update(relative.encode() + b"\\0" + kind.encode() + b"\\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()

root = Path(os.environ["FAKE_KLEAN_ROOT"])
args = sys.argv[1:]
with (root / "calls.jsonl").open("a") as stream:
    stream.write(json.dumps(args) + "\\n")
if args[:2] == ["image", "inspect"]:
    print("sha256:fake-klean-image")
    raise SystemExit(0)
scenarios = json.loads((root / "scenarios.json").read_text())
scenario = scenarios.pop(0)
(root / "scenarios.json").write_text(json.dumps(scenarios))
mount = next(value for value in args if "target=/output" in value)
output_root = Path(mount.split("source=", 1)[1].split(",target=", 1)[0])
frozen_mount = next(value for value in args if "target=/frozen-k" in value)
frozen = Path(frozen_mount.split("source=", 1)[1].split(",target=", 1)[0])
discovery_mount = next(
    value for value in args if "target=/discovery-manifest.json" in value
)
discovery = Path(
    discovery_mount.split("source=", 1)[1].split(",target=", 1)[0]
)
problem = next(
    value.split("=", 1)[1]
    for value in args
    if value.startswith("PROBLEM_ID=")
)
destination = output_root / "generation"
destination.mkdir()
destination.joinpath("export.log").write_text("export\\n")
status = scenario["status"]
successful = status in {"PASS", "KLEAN_NO_OBLIGATIONS"}
if successful:
    destination.joinpath("generated").mkdir()
    destination.joinpath("generated/Main.lean").write_text(
        "theorem target : True := by trivial\\n"
    )
    generated_sha256 = tree_digest(destination / "generated")
    stage1_sha256 = tree_digest(frozen)
    stage3_sha256 = hashlib.sha256(discovery.read_bytes()).hexdigest()
    trust_inventory = destination / "trust-inventory.json"
    trust_inventory.write_text("{}\\n")
    destination.joinpath("input-manifest.json").write_text(json.dumps({
        "schema_version": 3,
        "problem": problem,
        "frozen_input_sha256": stage1_sha256,
        "stage1_workspace_sha256": stage1_sha256,
        "stage3_discovery_manifest_sha256": stage3_sha256,
    }) + "\\n")
    destination.joinpath("generator-manifest.json").write_text(json.dumps({
        "schema_version": 3,
        "generated_tree_sha256": generated_sha256,
        "obligation_count": 1,
        "provenance": {
            "stage1_workspace_sha256": stage1_sha256,
            "stage3_discovery_manifest_sha256": stage3_sha256,
        },
    }) + "\\n")
    destination.joinpath("export-result.json").write_text(json.dumps({
        "schema_version": 3,
        "status": "OK" if status == "PASS" else "KLEAN_NO_OBLIGATIONS",
        "problem": problem,
        "frozen_input_sha256": stage1_sha256,
        "stage3_discovery_manifest_sha256": stage3_sha256,
        "generated_tree_sha256": generated_sha256,
        "trust_inventory_sha256": hashlib.sha256(
            trust_inventory.read_bytes()
        ).hexdigest(),
        "obligation_count": 1,
    }) + "\\n")
    destination.joinpath("preflight.log").write_text("pass\\n")
preflight = {"status": status}
if not scenario.get("status_only", False):
    preflight.update({
        "schema_version": 3,
        "stage1_workspace_sha256": scenario.get(
            "stage1_workspace_sha256", tree_digest(frozen)
        ),
        "stage3_discovery_manifest_sha256": scenario.get(
            "stage3_discovery_manifest_sha256",
            hashlib.sha256(discovery.read_bytes()).hexdigest(),
        ),
    })
    if successful:
        preflight["generated_tree_sha256"] = tree_digest(
            destination / "generated"
        )
        preflight["obligation_count"] = 1
destination.joinpath("preflight.json").write_text(
    json.dumps(preflight) + "\\n"
)
raise SystemExit(
    scenario.get("exit_code", 0 if successful else 1)
)
"""
        )
        self.fake_docker.chmod(0o755)

    def run_stage(self, *scenarios):
        self.scenarios.write_text(json.dumps(scenarios))
        old = os.environ.get("FAKE_KLEAN_ROOT")
        os.environ["FAKE_KLEAN_ROOT"] = str(self.fake_root)
        try:
            return stage4_runner.run_stage4(
                self.repo,
                self.run_id,
                self.PROBLEM,
                docker=str(self.fake_docker),
            )
        finally:
            if old is None:
                os.environ.pop("FAKE_KLEAN_ROOT", None)
            else:
                os.environ["FAKE_KLEAN_ROOT"] = old

    def test_print_config_is_non_mutating(self) -> None:
        document = stage4_runner.inspect_stage4(
            self.repo, self.run_id, self.PROBLEM
        )
        self.assertTrue(document["eligible"])
        self.assertEqual(document["next_generation"], "001")
        generations = self.task / "04-klean-generation/generations"
        self.assertEqual(list(generations.iterdir()), [])

    def test_incomplete_input_provenance_blocks_inspection_and_allocation(
        self,
    ) -> None:
        self.mark_input_provenance_incomplete()

        for entrypoint in (
            stage4_runner.inspect_stage4,
            stage4_runner._next_generation,
        ):
            with self.subTest(entrypoint=entrypoint.__name__):
                with self.assertRaisesRegex(
                    (
                        pipeline_contract.PipelineContractError,
                        stage4_runner.Stage4RunnerError,
                    ),
                    "INPUT_PROVENANCE_INCOMPLETE",
                ):
                    entrypoint(self.repo, self.run_id, self.PROBLEM)

    def test_pass_selects_001_without_auth_or_session_mounts(self) -> None:
        selected = self.run_stage({"status": "PASS"})
        self.assertEqual(selected["relative_path"], "generations/001")
        command = self.calls.read_text()
        self.assertIn("readonly", command)
        self.assertNotIn("auth.json", command)
        self.assertNotIn("codex-home", command)
        self.assertNotIn("runner-state", command)
        self.assertNotIn("target=/generations", command)
        self.assertNotIn("target=/stage2-selection.json", command)
        self.assertNotIn("target=/stage2-verdict.json", command)
        self.assertIn(
            "target=/discovery-manifest.json,readonly", command
        )
        self.assertIn("validated-trust-boundary.json", command)

    def test_publication_does_not_rename_across_filesystems(self) -> None:
        original_rename = Path.rename

        def reject_cross_device(source: Path, target: Path) -> Path:
            if source.name == "generation" and source.parent.name == "output":
                raise OSError(errno.EXDEV, "Invalid cross-device link")
            return original_rename(source, target)

        with mock.patch.object(Path, "rename", reject_cross_device):
            selected = self.run_stage({"status": "PASS"})

        self.assertEqual(selected["relative_path"], "generations/001")

    def test_failed_generation_is_preserved_and_manual_retry_uses_002(self) -> None:
        failed = self.run_stage({"status": "KLEAN_PREFLIGHT_ERROR"})
        self.assertEqual(failed["relative_path"], "generations/001")
        self.assertTrue(
            (self.task / "04-klean-generation/generations/001/export.log").is_file()
        )
        passed = self.run_stage({"status": "PASS"})
        self.assertEqual(passed["relative_path"], "generations/002")
        self.assertTrue(
            (self.task / "04-klean-generation/generations/001").is_dir()
        )

    def test_fail_verdict_never_launches_generator(self) -> None:
        verdict = self.task / "02-k-audit/executions/001/verdict.json"
        verdict.write_text(
            json.dumps(
                {
                    "audit_status": "COMPLETE",
                    "verdict": "FAIL",
                    "legitimacy": "NOT_LEGIT",
                    "error": None,
                }
            )
            + "\n"
        )
        # Selection hashes make mutation visible; make a separate ineligible
        # eligibility assertion directly on the trusted verdict state.
        with self.assertRaises(stage4_runner.Stage4RunnerError):
            stage4_runner._next_generation(
                self.repo, self.run_id, self.PROBLEM
            )

    def test_changed_protected_stage3_manifest_never_launches_generator(
        self,
    ) -> None:
        self.protected_manifest.write_text("{}\n")
        with self.assertRaisesRegex(
            stage4_runner.Stage4RunnerError, "protected Stage 3"
        ):
            stage4_runner._next_generation(
                self.repo, self.run_id, self.PROBLEM
            )
        self.assertFalse(self.calls.exists())

    def test_accepts_protected_stage3_infrastructure_retry(self) -> None:
        stage3 = self.task / "03-lemma-discovery"
        original = stage3 / "invocations/001-initial"
        retry = stage3 / "invocations/002-infrastructure-retry"
        original.rename(retry)
        artifact = (
            "invocations/002-infrastructure-retry/"
            "validated-trust-boundary.json"
        )
        invocation = json.loads((retry / "invocation.json").read_text())
        invocation["name"] = "002-infrastructure-retry"
        invocation["kind"] = "infrastructure-retry"
        invocation["trust_boundary_artifact"] = artifact
        (retry / "invocation.json").write_text(json.dumps(invocation) + "\n")
        result = json.loads((stage3 / "result.json").read_text())
        result["invocation"] = "002-infrastructure-retry"
        result["trust_boundary_artifact"] = artifact
        (stage3 / "result.json").write_text(json.dumps(result) + "\n")

        protected = stage4_runner._protected_stage3_discovery(self.task)

        self.assertEqual(protected.path, retry / "validated-trust-boundary.json")

    def test_inconsistent_failed_process_never_selects_pass(self) -> None:
        with self.assertRaisesRegex(
            stage4_runner.Stage4RunnerError, "container failed"
        ):
            self.run_stage({"status": "PASS", "exit_code": 1})
        self.assertFalse(
            (self.task / "04-klean-generation/selected.json").exists()
        )
        self.assertTrue(
            (
                self.task
                / "04-klean-generation/generations/001/preflight.json"
            ).is_file()
        )

    def test_status_only_pass_preflight_is_rejected_without_selection(
        self,
    ) -> None:
        with self.assertRaisesRegex(
            stage4_runner.Stage4RunnerError, "schema"
        ):
            self.run_stage({"status": "PASS", "status_only": True})
        self.assertFalse(
            (self.task / "04-klean-generation/selected.json").exists()
        )

    def test_terminal_preflight_requires_exact_protected_input_hashes(
        self,
    ) -> None:
        with self.assertRaisesRegex(
            stage4_runner.Stage4RunnerError, "Stage 1"
        ):
            self.run_stage(
                {
                    "status": "KLEAN_PREFLIGHT_ERROR",
                    "stage1_workspace_sha256": "0" * 64,
                }
            )
        self.assertFalse(
            (self.task / "04-klean-generation/selected.json").exists()
        )

    def assert_final_candidate_mutation_is_not_selected(
        self, mutate
    ) -> None:
        real_discovery = stage4_runner._protected_stage3_discovery
        calls = 0

        def mutate_during_final_check(task):
            nonlocal calls
            calls += 1
            result = real_discovery(task)
            if calls == 4:
                generation = (
                    self.task
                    / "04-klean-generation/generations/001"
                )
                mutate(generation)
            return result

        with mock.patch.object(
            stage4_runner,
            "_protected_stage3_discovery",
            side_effect=mutate_during_final_check,
        ):
            with self.assertRaisesRegex(
                (
                    stage4_runner.Stage4RunnerError,
                    pipeline_contract.PipelineContractError,
                ),
                "candidate|generated|sidecar|preflight",
            ):
                self.run_stage({"status": "PASS"})
        self.assertEqual(calls, 4)
        self.assertFalse(
            (self.task / "04-klean-generation/selected.json").exists()
        )

    def test_generated_mutation_during_final_check_is_not_selected(
        self,
    ) -> None:
        self.assert_final_candidate_mutation_is_not_selected(
            lambda generation: generation.joinpath(
                "generated/Injected.lean"
            ).write_text("theorem injected : True := by sorry\n")
        )

    def test_trust_inventory_mutation_during_final_check_is_not_selected(
        self,
    ) -> None:
        def replace_bound_inventory(generation: Path) -> None:
            inventory = generation / "trust-inventory.json"
            inventory.write_text('{"tampered": true}\n')
            export_path = generation / "export-result.json"
            export_result = json.loads(export_path.read_text())
            export_result["trust_inventory_sha256"] = hashlib.sha256(
                inventory.read_bytes()
            ).hexdigest()
            export_path.write_text(json.dumps(export_result) + "\n")

        self.assert_final_candidate_mutation_is_not_selected(
            replace_bound_inventory
        )

    def test_preflight_mutation_during_final_check_is_not_selected(
        self,
    ) -> None:
        def corrupt_preflight(generation: Path) -> None:
            path = generation / "preflight.json"
            document = json.loads(path.read_text())
            document["generated_tree_sha256"] = "0" * 64
            path.write_text(json.dumps(document) + "\n")

        self.assert_final_candidate_mutation_is_not_selected(
            corrupt_preflight
        )

    def test_shell_launchers_use_stage4_and_only_stage1_stage3_inputs(
        self,
    ) -> None:
        root = Path(__file__).resolve().parent.parent
        generate = (root / "docker/klean/generate_task.sh").read_text()
        check = (root / "docker/klean/check_task.sh").read_text()
        entrypoint = (root / "docker/klean/entrypoint.sh").read_text()
        self.assertIn("tools/stage4_runner.py", generate)
        self.assertIn("04-klean-generation", check)
        self.assertIn("--discovery-manifest", check)
        self.assertIn("/discovery-manifest.json", entrypoint)
        self.assertIn("--discovery-manifest", entrypoint)
        for text in (check, entrypoint):
            self.assertNotIn("stage2-selection", text)
            self.assertNotIn("stage2-verdict", text)


if __name__ == "__main__":
    import unittest

    unittest.main()
