import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from tools import audit_contract


REPO = Path(__file__).resolve().parent.parent


class AuditFixture(unittest.TestCase):
    PROBLEM = "8-sum-product"

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)

    def make_candidate(
        self,
        *,
        directory_config: str,
        manifest_config: str,
        condition: str,
        supplied_semantics: bool,
    ) -> tuple[Path, Path]:
        repo = Path(self.temporary_directory.name) / directory_config
        task = repo / "runs" / directory_config / self.PROBLEM
        question = repo / "data/questions" / self.PROBLEM
        semantics = repo / "data/reference/src"
        kit = repo / "data/skills/using-kit"
        tools = repo / "tools"
        trace = task / "codex-trace"
        question.mkdir(parents=True)
        semantics.mkdir(parents=True)
        kit.mkdir(parents=True)
        tools.mkdir(parents=True)
        trace.mkdir(parents=True)

        (question / "prompt.py").write_text("def add(a, b):\n    pass\n")
        (question / "canonical.py").write_text("def add(a, b):\n    return a + b\n")
        (tools / "py2mpy.py").write_text("# trusted translator\n")
        (semantics / "semantics.k").write_text("module SEMANTICS endmodule\n")
        (semantics / "generated").mkdir()
        (kit / "SKILL.md").write_text("---\nname: using-kit\n---\n")

        shutil.copy2(question / "prompt.py", task / "prompt.py")
        shutil.copy2(tools / "py2mpy.py", task / "py2mpy.py")
        if supplied_semantics:
            shutil.copytree(semantics, task / "reference-semantics")

        manifest = {
            "schema_version": 1,
            "config": manifest_config,
            "problem_id": self.PROBLEM,
            "condition": {
                "name": condition,
                "kit": condition in {"kit", "kit-semantics"},
                "semantics": supplied_semantics,
            },
            "inputs": {
                "problem_prompt_sha256": self.sha256_file(question / "prompt.py"),
                "translator_sha256": self.sha256_file(tools / "py2mpy.py"),
            },
        }
        (task / "run-input.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        )
        (task / "metrics.json").write_text("{}\n")
        (task / "codex-output.log").write_text("generation output\n")
        (task / "codex-last.txt").write_text("generation summary\n")
        (trace / "rollout.jsonl").write_text("{}\n")
        return repo, task

    @staticmethod
    def sha256_file(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()


class AuditResolutionTests(AuditFixture):
    def test_condition_comes_from_manifest_not_fix_suffix(self) -> None:
        repo, task = self.make_candidate(
            directory_config="codex-gpt-5.6-sol-xhigh-kit-semantics-fix-kit",
            manifest_config="codex-gpt-5.6-sol-xhigh-kit-semantics",
            condition="kit-semantics",
            supplied_semantics=True,
        )

        resolved = audit_contract.resolve_audit(
            repo,
            "codex-gpt-5.6-sol-xhigh-kit-semantics-fix-kit",
            self.PROBLEM,
        )

        self.assertEqual(resolved["condition"], "kit-semantics")
        self.assertTrue(resolved["mount_reference_semantics"])
        self.assertEqual(Path(resolved["candidate"]), task.resolve())
        self.assertEqual(
            resolved["manifest_config"],
            "codex-gpt-5.6-sol-xhigh-kit-semantics",
        )

    def test_generated_semantics_conditions_have_no_reference_mount(self) -> None:
        for condition in ("bare", "kit"):
            with self.subTest(condition=condition):
                repo, _ = self.make_candidate(
                    directory_config=f"future-{condition}-fix",
                    manifest_config=f"future-{condition}",
                    condition=condition,
                    supplied_semantics=False,
                )
                resolved = audit_contract.resolve_audit(
                    repo, f"future-{condition}-fix", self.PROBLEM
                )
                self.assertEqual(resolved["condition"], condition)
                self.assertFalse(resolved["mount_reference_semantics"])
                self.assertIsNone(resolved["reference_semantics"])

    def test_supplied_semantics_conditions_mount_trusted_tree(self) -> None:
        for condition in ("semantics", "kit-semantics"):
            with self.subTest(condition=condition):
                repo, _ = self.make_candidate(
                    directory_config=f"future-{condition}-fix",
                    manifest_config=f"future-{condition}",
                    condition=condition,
                    supplied_semantics=True,
                )
                resolved = audit_contract.resolve_audit(
                    repo, f"future-{condition}-fix", self.PROBLEM
                )
                self.assertTrue(resolved["mount_reference_semantics"])
                self.assertEqual(
                    Path(resolved["reference_semantics"]),
                    (repo / "data/reference/src").resolve(),
                )

    def test_unsafe_config_and_problem_components_are_rejected(self) -> None:
        repo, _ = self.make_candidate(
            directory_config="safe-config",
            manifest_config="safe-config",
            condition="bare",
            supplied_semantics=False,
        )
        unsafe = ("", ".", "..", ".hidden", "../escape", "a/b", "a\\b", "/tmp/x", "bad\nname")
        for value in unsafe:
            with self.subTest(config=value):
                with self.assertRaises(audit_contract.AuditContractError):
                    audit_contract.resolve_audit(repo, value, self.PROBLEM)
            with self.subTest(problem=value):
                with self.assertRaises(audit_contract.AuditContractError):
                    audit_contract.resolve_audit(repo, "safe-config", value)

    def test_symlinked_config_and_task_directories_are_rejected(self) -> None:
        repo, task = self.make_candidate(
            directory_config="real-config",
            manifest_config="real-config",
            condition="bare",
            supplied_semantics=False,
        )
        os.symlink(task.parent, repo / "runs/config-link")
        with self.assertRaisesRegex(
            audit_contract.AuditContractError, "generation config"
        ):
            audit_contract.resolve_audit(repo, "config-link", self.PROBLEM)

        linked_problem = "linked-problem"
        os.symlink(task, task.parent / linked_problem)
        with self.assertRaisesRegex(
            audit_contract.AuditContractError, "candidate task"
        ):
            audit_contract.resolve_audit(repo, "real-config", linked_problem)

    def test_runs_archive_is_not_an_active_generation_config(self) -> None:
        repo, _ = self.make_candidate(
            directory_config="archive",
            manifest_config="old-kit",
            condition="kit",
            supplied_semantics=False,
        )
        with self.assertRaisesRegex(audit_contract.AuditContractError, "runs/archive"):
            audit_contract.resolve_audit(repo, "archive", self.PROBLEM)

    def test_malformed_and_nonregular_manifests_are_rejected(self) -> None:
        mutations = (
            lambda path: path.write_text("{not-json\n"),
            lambda path: (path.unlink(), path.mkdir()),
            lambda path: (
                path.unlink(),
                path.symlink_to(path.parent / "metrics.json"),
            ),
        )
        for index, mutate in enumerate(mutations):
            with self.subTest(case=index):
                repo, task = self.make_candidate(
                    directory_config=f"config-{index}",
                    manifest_config=f"config-{index}",
                    condition="bare",
                    supplied_semantics=False,
                )
                mutate(task / "run-input.json")
                with self.assertRaisesRegex(
                    audit_contract.AuditContractError, "run-input.json"
                ):
                    audit_contract.resolve_audit(
                        repo, f"config-{index}", self.PROBLEM
                    )

    def test_manifest_problem_id_must_match_task_directory(self) -> None:
        repo, task = self.make_candidate(
            directory_config="mismatch",
            manifest_config="mismatch",
            condition="bare",
            supplied_semantics=False,
        )
        manifest_path = task / "run-input.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["problem_id"] = "different-problem"
        manifest_path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(audit_contract.AuditContractError, "problem_id"):
            audit_contract.resolve_audit(repo, "mismatch", self.PROBLEM)

    def test_manifest_condition_must_be_supported_and_well_formed(self) -> None:
        for index, condition_value in enumerate(
            ("future-condition", None, {"wrong": "bare"})
        ):
            with self.subTest(condition=condition_value):
                repo, task = self.make_candidate(
                    directory_config=f"bad-condition-{index}",
                    manifest_config="bad-condition",
                    condition="bare",
                    supplied_semantics=False,
                )
                manifest_path = task / "run-input.json"
                manifest = json.loads(manifest_path.read_text())
                manifest["condition"] = condition_value
                manifest_path.write_text(json.dumps(manifest))
                with self.assertRaisesRegex(
                    audit_contract.AuditContractError, "condition"
                ):
                    audit_contract.resolve_audit(
                        repo, task.parent.name, self.PROBLEM
                    )

    def test_manifest_condition_name_must_be_a_string(self) -> None:
        for index, condition_name in enumerate(([], {"nested": "bare"})):
            with self.subTest(condition_name=condition_name):
                repo, task = self.make_candidate(
                    directory_config=f"nested-condition-name-{index}",
                    manifest_config="nested-condition-name",
                    condition="bare",
                    supplied_semantics=False,
                )
                manifest_path = task / "run-input.json"
                manifest = json.loads(manifest_path.read_text())
                manifest["condition"]["name"] = condition_name
                manifest_path.write_text(json.dumps(manifest))

                with self.assertRaisesRegex(
                    audit_contract.AuditContractError,
                    "manifest condition name must be a string",
                ):
                    audit_contract.resolve_audit(
                        repo, task.parent.name, self.PROBLEM
                    )

    def test_all_generation_evidence_is_required(self) -> None:
        for evidence in (
            "metrics.json",
            "codex-output.log",
            "codex-last.txt",
            "codex-trace",
        ):
            with self.subTest(evidence=evidence):
                repo, task = self.make_candidate(
                    directory_config=f"missing-{evidence}",
                    manifest_config="missing-evidence",
                    condition="bare",
                    supplied_semantics=False,
                )
                path = task / evidence
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                with self.assertRaisesRegex(
                    audit_contract.AuditContractError, evidence
                ):
                    audit_contract.resolve_audit(
                        repo, task.parent.name, self.PROBLEM
                    )

    def test_candidate_integrity_mismatches_are_recorded_not_rejected(self) -> None:
        repo, task = self.make_candidate(
            directory_config="tampered-supplied",
            manifest_config="original-supplied",
            condition="semantics",
            supplied_semantics=True,
        )
        (task / "prompt.py").write_text("# changed prompt\n")
        (task / "py2mpy.py").unlink()
        (task / "py2mpy.py").symlink_to(repo / "tools/py2mpy.py")
        (task / "reference-semantics/unexpected-empty").mkdir()
        manifest_path = task / "run-input.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["inputs"]["problem_prompt_sha256"] = "0" * 64
        manifest["inputs"]["translator_sha256"] = "1" * 64
        manifest["inputs"]["reference_semantics_sha256"] = "2" * 64
        manifest_path.write_text(json.dumps(manifest))

        resolved = audit_contract.resolve_audit(
            repo, "tampered-supplied", self.PROBLEM
        )

        integrity = resolved["integrity"]
        self.assertFalse(integrity["candidate_prompt_matches_trusted"])
        self.assertFalse(integrity["candidate_translator_matches_trusted"])
        self.assertFalse(integrity["candidate_reference_semantics_matches_trusted"])
        self.assertFalse(integrity["manifest_prompt_hash_matches_trusted"])
        self.assertFalse(integrity["manifest_translator_hash_matches_trusted"])
        self.assertFalse(integrity["manifest_reference_semantics_hash_matches_trusted"])

    def test_tree_hash_records_empty_directories_and_entry_types(self) -> None:
        repo, task = self.make_candidate(
            directory_config="tree-types",
            manifest_config="tree-types",
            condition="kit-semantics",
            supplied_semantics=True,
        )
        first = audit_contract.resolve_audit(repo, "tree-types", self.PROBLEM)
        self.assertTrue(
            first["integrity"]["candidate_reference_semantics_matches_trusted"]
        )
        trusted_hash = first["hashes"]["trusted_reference_semantics_sha256"]
        self.assertEqual(len(trusted_hash), 64)

        candidate_file = task / "reference-semantics/semantics.k"
        candidate_file.unlink()
        candidate_file.symlink_to(repo / "data/reference/src/semantics.k")
        second = audit_contract.resolve_audit(repo, "tree-types", self.PROBLEM)
        self.assertNotEqual(
            second["hashes"]["candidate_reference_semantics_sha256"], trusted_hash
        )
        self.assertFalse(
            second["integrity"]["candidate_reference_semantics_matches_trusted"]
        )

    def test_tree_hash_streams_regular_file_contents(self) -> None:
        root = Path(self.temporary_directory.name) / "streamed-tree"
        root.mkdir()
        (root / "large-evidence.bin").write_bytes(b"audit-evidence" * 100_000)
        expected = audit_contract.sha256_tree(root)

        with mock.patch.object(
            Path,
            "read_bytes",
            side_effect=AssertionError("tree hashing must not call Path.read_bytes"),
        ):
            actual = audit_contract.sha256_tree(root)

        self.assertEqual(actual, expected)

    def test_resolve_cli_emits_json_contract(self) -> None:
        repo, task = self.make_candidate(
            directory_config="cli-config",
            manifest_config="original-cli-config",
            condition="bare",
            supplied_semantics=False,
        )
        result = subprocess.run(
            (
                sys.executable,
                str(REPO / "tools/audit_contract.py"),
                "resolve",
                "--repo",
                str(repo),
                "--config",
                "cli-config",
                "--problem",
                self.PROBLEM,
            ),
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["candidate"], str(task.resolve()))
        self.assertEqual(payload["condition"], "bare")


class VerdictNormalizationTests(unittest.TestCase):
    def test_pass_and_concerns_are_legit(self) -> None:
        for verdict in ("PASS", "CONCERNS"):
            with self.subTest(verdict=verdict):
                review = f"VERDICT: {verdict}\nLEGITIMACY: LEGIT\n"
                result = audit_contract.normalize_verdict(review, 0, 0, False)
                self.assertEqual(result["audit_status"], "COMPLETE")
                self.assertEqual(result["verdict"], verdict)
                self.assertEqual(result["legitimacy"], "LEGIT")
                self.assertIsNone(result["error"])

    def test_fail_is_not_legit(self) -> None:
        result = audit_contract.normalize_verdict(
            "VERDICT: FAIL\nLEGITIMACY: NOT_LEGIT\n", 0, 0, False
        )
        self.assertEqual(result["audit_status"], "COMPLETE")
        self.assertEqual(result["verdict"], "FAIL")
        self.assertEqual(result["legitimacy"], "NOT_LEGIT")

    def test_final_two_nonempty_lines_are_parsed(self) -> None:
        result = audit_contract.normalize_verdict(
            "Detailed review.\n\nVERDICT: PASS\nLEGITIMACY: LEGIT\n\n",
            0,
            0,
            False,
        )
        self.assertEqual(result["audit_status"], "COMPLETE")
        self.assertEqual(result["verdict"], "PASS")

    def test_timeout_is_audit_error_even_with_markers(self) -> None:
        result = audit_contract.normalize_verdict(
            "VERDICT: PASS\nLEGITIMACY: LEGIT\n", 124, 0, True
        )
        self.assertEqual(result["audit_status"], "AUDIT_ERROR")
        self.assertIsNone(result["verdict"])
        self.assertIsNone(result["legitimacy"])
        self.assertIn("timed out", result["error"])

    def test_nonzero_model_exit_is_an_audit_error(self) -> None:
        result = audit_contract.normalize_verdict(
            "VERDICT: FAIL\nLEGITIMACY: NOT_LEGIT\n", 17, 0, False
        )
        self.assertEqual(result["audit_status"], "AUDIT_ERROR")
        self.assertIsNone(result["verdict"])
        self.assertIn("17", result["error"])

    def test_nonzero_harness_exit_is_an_audit_error(self) -> None:
        result = audit_contract.normalize_verdict(
            "VERDICT: PASS\nLEGITIMACY: LEGIT\n", 0, 70, False
        )
        self.assertEqual(result["audit_status"], "AUDIT_ERROR")
        self.assertIsNone(result["verdict"])
        self.assertIn("harness", result["error"])
        self.assertIn("70", result["error"])

    def test_duplicate_missing_and_nonfinal_markers_are_rejected(self) -> None:
        reviews = {
            "duplicate": (
                "VERDICT: PASS\nLEGITIMACY: LEGIT\n"
                "VERDICT: PASS\nLEGITIMACY: LEGIT\n"
            ),
            "missing": "Detailed review only.\n",
            "missing_legitimacy": "VERDICT: PASS\n",
            "nonfinal": "VERDICT: PASS\nLEGITIMACY: LEGIT\ntrailing prose\n",
        }
        for label, review in reviews.items():
            with self.subTest(case=label):
                result = audit_contract.normalize_verdict(review, 0, 0, False)
                self.assertEqual(result["audit_status"], "AUDIT_ERROR")
                self.assertIsNone(result["verdict"])
                self.assertIsNotNone(result["error"])

    def test_inconsistent_marker_pairs_are_rejected(self) -> None:
        for pair in (
            ("PASS", "NOT_LEGIT"),
            ("CONCERNS", "NOT_LEGIT"),
            ("FAIL", "LEGIT"),
        ):
            with self.subTest(pair=pair):
                review = f"VERDICT: {pair[0]}\nLEGITIMACY: {pair[1]}\n"
                result = audit_contract.normalize_verdict(review, 0, 0, False)
                self.assertEqual(result["audit_status"], "AUDIT_ERROR")
                self.assertIsNone(result["verdict"])
                self.assertIn("inconsistent", result["error"])


class VerdictCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.review = self.root / "REVIEW.md"
        self.metrics = self.root / "metrics.json"
        self.output = self.root / "verdict.json"

    def run_cli(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            (
                sys.executable,
                str(REPO / "tools/audit_contract.py"),
                "verdict",
                "--review",
                str(self.review),
                "--metrics",
                str(self.metrics),
                "--output",
                str(self.output),
            ),
            check=False,
            capture_output=True,
            text=True,
        )

    def test_verdict_cli_atomically_replaces_output(self) -> None:
        self.review.write_text("VERDICT: CONCERNS\nLEGITIMACY: LEGIT\n")
        self.metrics.write_text(
            json.dumps(
                {
                    "model_exit_code": 0,
                    "harness_exit_code": 0,
                    "timed_out": False,
                }
            )
        )
        self.output.write_text("stale output\n")

        result = self.run_cli()

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(self.output.read_text())
        self.assertEqual(payload["audit_status"], "COMPLETE")
        self.assertEqual(payload["verdict"], "CONCERNS")
        self.assertEqual(
            [path.name for path in self.root.iterdir() if path.name.startswith(".verdict")],
            [],
        )

    def test_missing_review_writes_audit_error(self) -> None:
        self.metrics.write_text(
            json.dumps(
                {
                    "model_exit_code": 0,
                    "harness_exit_code": 0,
                    "timed_out": False,
                }
            )
        )

        result = self.run_cli()

        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(self.output.read_text())
        self.assertEqual(payload["audit_status"], "AUDIT_ERROR")
        self.assertIsNone(payload["verdict"])
        self.assertIn("REVIEW.md", payload["error"])

    def test_malformed_metrics_writes_audit_error(self) -> None:
        self.review.write_text("VERDICT: PASS\nLEGITIMACY: LEGIT\n")
        self.metrics.write_text("not json\n")

        result = self.run_cli()

        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(self.output.read_text())
        self.assertEqual(payload["audit_status"], "AUDIT_ERROR")
        self.assertIn("metrics", payload["error"])

    def test_nonzero_harness_status_is_an_audit_error(self) -> None:
        self.review.write_text("VERDICT: PASS\nLEGITIMACY: LEGIT\n")
        self.metrics.write_text(
            json.dumps(
                {
                    "model_exit_code": 0,
                    "harness_exit_code": 70,
                    "timed_out": False,
                }
            )
        )

        result = self.run_cli()

        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(self.output.read_text())
        self.assertEqual(payload["audit_status"], "AUDIT_ERROR")
        self.assertIsNone(payload["verdict"])
        self.assertIn("harness", payload["error"])
        self.assertIn("70", payload["error"])

    def test_missing_harness_status_is_an_audit_error(self) -> None:
        self.review.write_text("VERDICT: PASS\nLEGITIMACY: LEGIT\n")
        self.metrics.write_text(
            json.dumps({"model_exit_code": 0, "timed_out": False})
        )

        result = self.run_cli()

        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(self.output.read_text())
        self.assertEqual(payload["audit_status"], "AUDIT_ERROR")
        self.assertIn("harness_exit_code", payload["error"])


class AuditPromptContractTests(unittest.TestCase):
    def test_audit_prompt_has_independent_dynamic_and_static_gates(self) -> None:
        text = (REPO / "prompts/audit.md").read_text()
        for phrase in (
            "UNTRUSTED EVIDENCE",
            "/audit-input.json",
            "/audit-campaign-lock.json",
            "/generation-evidence/invocation.json",
            "legacy-selected-stage1",
            "infrastructure breach",
            "AUDIT_ERROR",
            "clean proof reconstruction",
            "candidate-versus-canonical",
            "rule-by-rule",
            "non-vacuity",
            "proven versus assumed",
            "constructor-level comparison",
            "bounded unrollings do not prove",
            "VERDICT: <PASS|CONCERNS|FAIL>",
            "LEGITIMACY: <LEGIT|NOT_LEGIT>",
        ):
            self.assertIn(phrase, text)

    def test_generated_semantics_route_forbids_reference_semantics(self) -> None:
        text = (REPO / "prompts/audit.md").read_text()
        self.assertIn("GENERATED_SEMANTICS", text)
        self.assertIn("`/reference/reference-semantics` must not exist", text)


class AuditEntrypointFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.home = self.root / "home"
        self.supervisor_parent = self.home / "audit-supervisor"
        self.auth = self.root / "auth.json"
        self.kit = self.root / "kit-skills"
        self.prompt = self.root / "audit-prompt.md"
        self.output = self.root / "audit-output"
        self.work = self.root / "audit-work"
        self.cgroup = self.root / "cgroup"
        self.bin = self.root / "bin"
        self.codex_args = self.root / "codex-args"
        self.codex_stdin = self.root / "codex-stdin"
        self.profile_listing = self.root / "profile-listing"
        self.sentinel = self.root / "sentinel"
        for directory in (
            self.home,
            self.supervisor_parent,
            self.kit / "using-kit",
            self.output,
            self.work,
            self.cgroup,
            self.bin,
        ):
            directory.mkdir(parents=True, exist_ok=True)
        self.auth.write_text('{"tokens": {}}\n')
        (self.kit / "using-kit/SKILL.md").write_text(
            "---\nname: using-kit\n---\n"
        )
        self.prompt.write_text(
            "Problem: __PROBLEM_ID__\n"
            "Condition: __CONDITION__\n"
            "Mode: __SEMANTICS_MODE__\n"
        )
        (self.cgroup / "memory.peak").write_text("4567\n")
        self.sentinel.write_text("sentinel must remain unchanged\n")
        self.write_executable(
            self.bin / "timeout",
            """#!/usr/bin/env bash
set -uo pipefail
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --signal=*|--kill-after=*) shift ;;
    *) break ;;
  esac
done
if [[ "$#" -lt 2 ]]; then
  exit 98
fi
shift
"$@"
command_rc=$?
if [[ -n "${FAKE_TIMEOUT_FORCE_RC:-}" ]]; then
  exit "$FAKE_TIMEOUT_FORCE_RC"
fi
exit "$command_rc"
""",
        )
        self.write_executable(
            self.bin / "codex",
            """#!/usr/bin/env bash
set -uo pipefail
printf '%s\\0' "$@" > "$FAKE_CODEX_ARGS"
cat > "$FAKE_CODEX_STDIN"
find "$CODEX_HOME" -mindepth 1 -printf '%P\\n' \
  | LC_ALL=C sort > "$FAKE_PROFILE_LISTING"

last_message=''
while [[ "$#" -gt 0 ]]; do
  if [[ "$1" == '--output-last-message' ]]; then
    last_message="$2"
    shift 2
  else
    shift
  fi
done

case "${FAKE_DESTINATION_ACTION:-}" in
  prompt_symlink)
    ln -s -- "$FAKE_SENTINEL" "$AUDIT_OUTPUT_DIR/prompt.txt"
    ;;
  log_directory)
    mkdir -- "$AUDIT_OUTPUT_DIR/codex-output.log"
    ;;
esac

if [[ "${FAKE_WRITE_LAST:-1}" == '1' ]]; then
  if [[ "${FAKE_LAST_SYMLINK:-0}" == '1' ]]; then
    ln -s -- "$FAKE_SENTINEL" "$last_message"
  else
    printf 'reviewer last message\\n' > "$last_message"
  fi
fi

if [[ "${FAKE_WRITE_TRACE:-1}" == '1' ]]; then
  mkdir -p "$CODEX_HOME/sessions/2026/07/21"
  if [[ "${FAKE_TRACE_SYMLINK:-0}" == '1' ]]; then
    ln -s -- "$FAKE_SENTINEL" \
      "$CODEX_HOME/sessions/2026/07/21/rollout.jsonl"
  else
    printf '{"turn": 1}\\n' \
      > "$CODEX_HOME/sessions/2026/07/21/rollout.jsonl"
  fi
fi

printf 'Detailed fake review.\\n\\nVERDICT: PASS\\nLEGITIMACY: LEGIT\\n' \
  > "$AUDIT_OUTPUT_DIR/REVIEW.md"
mkdir -p "$AUDIT_OUTPUT_DIR/evidence"
printf 'fake evidence\\n' > "$AUDIT_OUTPUT_DIR/evidence/command.log"

if [[ "${FAKE_BACKGROUND_RACE:-0}" == '1' ]]; then
  (
    trap '' TERM
    sleep 0.2
    printf 'background process won the race\\n' \
      > "$AUDIT_OUTPUT_DIR/prompt.txt"
  ) &
fi

printf 'fake codex stdout\\n'
exit "${FAKE_CODEX_RC:-0}"
""",
        )

    @staticmethod
    def write_executable(path: Path, text: str) -> None:
        path.write_text(text)
        path.chmod(0o755)

    def run_entrypoint(
        self, **overrides: str
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment.update(
            {
                "HOME": str(self.home),
                "PATH": f"{self.bin}:{environment['PATH']}",
                "AUDIT_AUTH_FILE": str(self.auth),
                "AUDIT_KIT_SKILLS_DIR": str(self.kit),
                "AUDIT_PROMPT_FILE": str(self.prompt),
                "AUDIT_OUTPUT_DIR": str(self.output),
                "AUDIT_WORK_DIR": str(self.work),
                "AUDIT_SUPERVISOR_PARENT": str(self.supervisor_parent),
                "AUDIT_CGROUP_ROOT": str(self.cgroup),
                "AUDIT_PROBLEM_ID": "8-sum-product",
                "AUDIT_CONDITION": "kit",
                "AUDIT_SEMANTICS_MODE": "GENERATED_SEMANTICS",
                "FAKE_CODEX_ARGS": str(self.codex_args),
                "FAKE_CODEX_STDIN": str(self.codex_stdin),
                "FAKE_PROFILE_LISTING": str(self.profile_listing),
                "FAKE_SENTINEL": str(self.sentinel),
                "FROZEN_TOOLCHAIN_CHECK": "/bin/true",
            }
        )
        environment.update(overrides)
        return subprocess.run(
            (str(REPO / "docker/audit/entrypoint.sh"),),
            cwd=self.output,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )

    def metrics(self) -> dict[str, object]:
        path = self.output / "metrics.json"
        self.assertTrue(path.is_file(), "entrypoint did not publish metrics.json")
        return json.loads(path.read_text())


class AuditEntrypointContractTests(AuditEntrypointFixture):
    def test_entrypoint_fixes_reviewer_and_preserves_evidence(self) -> None:
        text = (REPO / "docker/audit/entrypoint.sh").read_text()
        self.assertIn('MODEL="gpt-5.6-sol"', text)
        self.assertIn('EFFORT="xhigh"', text)
        self.assertIn('TIMEOUT_S="3600"', text)
        self.assertIn("timeout --signal=TERM --kill-after=60", text)
        self.assertIn('AUTH_FILE="${AUDIT_AUTH_FILE:-/auth/auth.json}"', text)
        self.assertIn(
            'KIT_SKILLS_DIR="${AUDIT_KIT_SKILLS_DIR:-/kit-skills}"', text
        )
        self.assertIn('OUTPUT_DIR="${AUDIT_OUTPUT_DIR:-/audit-output}"', text)
        self.assertIn('WORK_DIR="${AUDIT_WORK_DIR:-/tmp/audit-work}"', text)
        self.assertIn("codex -a never exec", text)
        self.assertIn("--sandbox workspace-write", text)
        self.assertIn("--ignore-user-config", text)
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", text)

    def test_normal_run_publishes_exact_evidence(self) -> None:
        result = self.run_entrypoint()

        self.assertEqual(result.returncode, 0, result.stderr)
        expected_prompt = (
            "Problem: 8-sum-product\n"
            "Condition: kit\n"
            "Mode: GENERATED_SEMANTICS\n"
        )
        self.assertEqual((self.output / "prompt.txt").read_text(), expected_prompt)
        self.assertEqual(self.codex_stdin.read_text(), expected_prompt)
        self.assertIn(
            "fake codex stdout", (self.output / "codex-output.log").read_text()
        )
        self.assertEqual(
            (self.output / "codex-last.txt").read_text(),
            "reviewer last message\n",
        )
        self.assertEqual(
            (self.output / "codex-trace/2026/07/21/rollout.jsonl").read_text(),
            '{"turn": 1}\n',
        )
        self.assertTrue((self.output / "REVIEW.md").is_file())
        self.assertTrue((self.output / "evidence/command.log").is_file())
        self.assertEqual(
            self.profile_listing.read_text().splitlines(),
            [
                "auth.json",
                "skills",
                "skills/using-kit",
                "skills/using-kit/SKILL.md",
            ],
        )
        metrics = self.metrics()
        self.assertEqual(metrics["model_exit_code"], 0)
        self.assertEqual(metrics["harness_exit_code"], 0)
        self.assertFalse(metrics["timed_out"])
        self.assertEqual(metrics["mem_peak_bytes"], 4567)
        self.assertEqual(list(self.supervisor_parent.iterdir()), [])

    def test_fixed_sandbox_flags_and_model_status_are_preserved(self) -> None:
        result = self.run_entrypoint(FAKE_CODEX_RC="23")

        self.assertEqual(result.returncode, 23, result.stderr)
        arguments = [
            item.decode() for item in self.codex_args.read_bytes().split(b"\0") if item
        ]
        self.assertEqual(arguments[:3], ["-a", "never", "exec"])
        self.assertEqual(
            arguments[3:12],
            [
                "--sandbox",
                "workspace-write",
                "--add-dir",
                str(self.work),
                "--ignore-user-config",
                "--skip-git-repo-check",
                "-C",
                str(self.output),
                "-m",
            ],
        )
        self.assertEqual(arguments[12], "gpt-5.6-sol")
        self.assertIn("model_reasoning_effort=xhigh", arguments)
        last_path = Path(arguments[arguments.index("--output-last-message") + 1])
        self.assertTrue(last_path.is_relative_to(self.supervisor_parent))
        self.assertFalse(last_path.is_relative_to(self.output))
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", arguments)
        metrics = self.metrics()
        self.assertEqual(metrics["model_exit_code"], 23)
        self.assertEqual(metrics["harness_exit_code"], 0)

    def test_missing_last_message_is_a_harness_error(self) -> None:
        result = self.run_entrypoint(FAKE_WRITE_LAST="0")

        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.output / "codex-last.txt").exists())
        metrics = self.metrics()
        self.assertEqual(metrics["model_exit_code"], 0)
        self.assertNotEqual(metrics["harness_exit_code"], 0)

    def test_linked_last_message_source_is_a_harness_error(self) -> None:
        result = self.run_entrypoint(FAKE_LAST_SYMLINK="1")

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.sentinel.read_text(), "sentinel must remain unchanged\n")
        self.assertFalse((self.output / "codex-last.txt").exists())
        self.assertNotEqual(self.metrics()["harness_exit_code"], 0)

    def test_destination_symlink_is_replaced_without_following_it(self) -> None:
        result = self.run_entrypoint(FAKE_DESTINATION_ACTION="prompt_symlink")

        self.assertEqual(result.returncode, 0, result.stderr)
        destination = self.output / "prompt.txt"
        self.assertTrue(destination.is_file())
        self.assertFalse(destination.is_symlink())
        self.assertEqual(self.sentinel.read_text(), "sentinel must remain unchanged\n")
        self.assertEqual(destination.read_text(), self.codex_stdin.read_text())

    def test_destination_directory_is_rejected(self) -> None:
        result = self.run_entrypoint(FAKE_DESTINATION_ACTION="log_directory")

        self.assertNotEqual(result.returncode, 0)
        self.assertTrue((self.output / "codex-output.log").is_dir())
        metrics = self.metrics()
        self.assertEqual(metrics["model_exit_code"], 0)
        self.assertNotEqual(metrics["harness_exit_code"], 0)

    def test_setup_failure_does_not_start_codex(self) -> None:
        self.auth.unlink()

        result = self.run_entrypoint()

        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.codex_args.exists())
        self.assertFalse((self.output / "metrics.json").exists())

    def test_linked_trace_source_is_rejected(self) -> None:
        result = self.run_entrypoint(FAKE_TRACE_SYMLINK="1")

        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.output / "codex-trace").exists())
        self.assertNotEqual(self.metrics()["harness_exit_code"], 0)

    def test_kill_after_status_137_is_recorded_as_timeout(self) -> None:
        result = self.run_entrypoint(FAKE_TIMEOUT_FORCE_RC="137")

        self.assertEqual(result.returncode, 137, result.stderr)
        metrics = self.metrics()
        self.assertEqual(metrics["model_exit_code"], 137)
        self.assertEqual(metrics["harness_exit_code"], 0)
        self.assertTrue(metrics["timed_out"])

    def test_background_process_group_is_dead_before_publication(self) -> None:
        result = self.run_entrypoint(FAKE_BACKGROUND_RACE="1")

        self.assertEqual(result.returncode, 0, result.stderr)
        time.sleep(0.35)
        self.assertEqual(
            (self.output / "prompt.txt").read_text(), self.codex_stdin.read_text()
        )


class AuditLauncherTests(AuditFixture):
    def install_launcher(self, repo: Path) -> Path:
        audit_dir = repo / "docker/audit"
        prompt_dir = repo / "prompts"
        audit_dir.mkdir(parents=True)
        prompt_dir.mkdir(parents=True)
        launcher = audit_dir / "run_task.sh"
        shutil.copy2(REPO / "docker/audit/run_task.sh", launcher)
        shutil.copy2(REPO / "docker/audit/entrypoint.sh", audit_dir / "entrypoint.sh")
        shutil.copy2(REPO / "tools/audit_contract.py", repo / "tools/audit_contract.py")
        shutil.copy2(REPO / "prompts/audit.md", prompt_dir / "audit.md")
        return launcher

    def print_config(
        self, repo: Path, config: str
    ) -> subprocess.CompletedProcess[str]:
        launcher = self.install_launcher(repo)
        return subprocess.run(
            ("bash", str(launcher), "--print-config", config, self.PROBLEM),
            check=False,
            capture_output=True,
            text=True,
        )

    def test_print_config_uses_fixed_reviewer_and_supplied_semantics_mount(self) -> None:
        config = "codex-gpt-5.6-sol-xhigh-kit-semantics-fix-kit"
        repo, task = self.make_candidate(
            directory_config=config,
            manifest_config="codex-gpt-5.6-sol-xhigh-kit-semantics",
            condition="kit-semantics",
            supplied_semantics=True,
        )

        result = self.print_config(repo, config)

        self.assertEqual(result.returncode, 0, result.stderr)
        lines = result.stdout.splitlines()
        for expected in (
            "model=gpt-5.6-sol",
            "effort=xhigh",
            "memory=8g",
            "memory_swap=8g",
            "timeout_s=3600",
            "condition=kit-semantics",
            "semantics_mode=SUPPLIED_SEMANTICS",
            "mount_reference_semantics=1",
            "record_layout=legacy",
            f"candidate={task.resolve()}",
            f"generation_root={task.resolve()}",
        ):
            self.assertIn(expected, lines)
        self.assertIn(
            f"reference_semantics={(repo / 'data/reference/src').resolve()}",
            lines,
        )

    def test_print_config_omits_reference_semantics_for_generated_mode(self) -> None:
        config = "future-kit-fix"
        repo, _ = self.make_candidate(
            directory_config=config,
            manifest_config="future-kit",
            condition="kit",
            supplied_semantics=False,
        )

        result = self.print_config(repo, config)

        self.assertEqual(result.returncode, 0, result.stderr)
        lines = result.stdout.splitlines()
        self.assertIn("condition=kit", lines)
        self.assertIn("semantics_mode=GENERATED_SEMANTICS", lines)
        self.assertIn("mount_reference_semantics=0", lines)
        self.assertFalse(
            any(line.startswith("reference_semantics=") for line in lines)
        )

    def test_launcher_allows_the_nested_codex_sandbox_to_create_namespaces(self) -> None:
        launcher = (REPO / "docker/audit/run_task.sh").read_text()

        self.assertIn("--security-opt seccomp=unconfined", launcher)

    def test_launcher_mounts_generation_records_read_only(self) -> None:
        launcher = (REPO / "docker/audit/run_task.sh").read_text()

        # The auditor's Kit is the campaign-frozen bundle, decoupled from
        # the moving generation Kit; the campaign lock pins its lock hash.
        self.assertIn('KIT_SKILLS="$REPO/data/audit-skills"', launcher)
        self.assertIn(
            'AUDIT_KIT_LOCK="$REPO/data/audit-kit-skills.lock.json"',
            launcher,
        )
        self.assertIn('--bundle "$KIT_SKILLS" --lock "$AUDIT_KIT_LOCK"', launcher)
        self.assertIn("check_audit_campaign.py", launcher)
        for mount in (
            'source=$GENERATION_ROOT,target=/generation-evidence,readonly',
            'source=$RUN_MANIFEST,target=/run.json,readonly',
            'source=$TASK_MANIFEST,target=/task.json,readonly',
            'source=$STAGE1_RESULT,target=/generation-result.json,readonly',
            'source=$CAMPAIGN_LOCK,target=/audit-campaign-lock.json,readonly',
        ):
            self.assertIn(mount, launcher)
        self.assertIn('document["container_paths"] = container_paths', launcher)


if __name__ == "__main__":
    unittest.main()
