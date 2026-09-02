import ast
import importlib.util
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO = Path(__file__).resolve().parents[1]


def generation_prompt_paths() -> tuple[Path, ...]:
    populator = load_populator()
    return tuple(
        REPO / "prompts" / condition.prompt_file
        for condition in populator.CONDITIONS
    )


def load_kit_checker():
    path = REPO / "tools/check_kit_bundle.py"
    spec = importlib.util.spec_from_file_location("check_kit_bundle", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def make_kit_source(root: Path) -> Path:
    source = root / "kit"
    plugin = source / ".codex-plugin/plugin.json"
    skill = source / "skills/example/SKILL.md"
    plugin.parent.mkdir(parents=True)
    skill.parent.mkdir(parents=True)
    plugin.write_text('{"version": "1.2.3"}\n')
    skill.write_text("# Example\n")
    (source / "skills").chmod(0o755)
    skill.parent.chmod(0o755)
    skill.chmod(0o644)
    plugin.chmod(0o644)
    git(source, "init", "-q")
    git(source, "add", ".codex-plugin/plugin.json", "skills/example/SKILL.md")
    git(
        source,
        "-c",
        "user.name=Benchmark Test",
        "-c",
        "user.email=benchmark@example.invalid",
        "commit",
        "-qm",
        "initial",
    )
    return source


def make_bundle(root: Path, *, empty_slot: bool = False) -> tuple[Path, Path, dict]:
    bundle = root / "bundle"
    skill_dir = bundle / "example"
    skill = skill_dir / "SKILL.md"
    skill_dir.mkdir(parents=True)
    skill.write_text("# Example\n")
    bundle.chmod(0o755)
    skill_dir.chmod(0o755)
    skill.chmod(0o644)
    entries = {
        ".": {"type": "directory", "mode": "0755"},
        "example": {"type": "directory", "mode": "0755"},
        "example/SKILL.md": {"type": "file", "mode": "0644"},
    }
    if empty_slot:
        slot = bundle / "slot"
        slot.mkdir()
        slot.chmod(0o755)
        entries["slot"] = {"type": "directory", "mode": "0755"}
    lock = {
        "schema_version": 2,
        "files": {
            "example/SKILL.md": hashlib.sha256(skill.read_bytes()).hexdigest(),
        },
        "entries": entries,
    }
    return bundle, skill, lock


class PromptAssetTests(unittest.TestCase):
    def test_all_164_prompt_assets_match_lock(self) -> None:
        lock = json.loads((REPO / "data/humaneval-prompts.lock.json").read_text())
        self.assertEqual(lock["schema_version"], 1)
        self.assertEqual(set(lock["tasks"]), {f"HumanEval/{n}" for n in range(164)})
        for task_id, entry in lock["tasks"].items():
            path = REPO / "data/questions" / entry["directory"] / "prompt.py"
            self.assertTrue(path.is_file(), task_id)
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(digest, entry["sha256"], task_id)

    def test_lock_maps_by_task_number_not_directory_spelling(self) -> None:
        lock = json.loads((REPO / "data/humaneval-prompts.lock.json").read_text())
        self.assertEqual(lock["tasks"]["HumanEval/66"]["directory"], "66-digitsum")


class InstructionPromptTests(unittest.TestCase):
    def test_generation_prompt_paths_follow_production_condition_registry(
        self,
    ) -> None:
        registry = mock.Mock(
            CONDITIONS=(mock.Mock(prompt_file="production-wired.md"),)
        )
        with mock.patch.object(
            sys.modules[__name__], "load_populator", return_value=registry
        ):
            names = {path.name for path in generation_prompt_paths()}

        self.assertEqual(names, {"production-wired.md"})

    def test_prompt_assets_are_registered_generation_and_pipeline_prompts(
        self,
    ) -> None:
        populator = load_populator()
        generation_names = {
            condition.prompt_file for condition in populator.CONDITIONS
        }
        asset_names = {path.name for path in (REPO / "prompts").glob("*.md")}

        self.assertEqual(
            asset_names,
            generation_names
            | {
                "audit.md",
                "infrastructure-resume.md",
                "oom-resume.md",
                "terminal-resume.md",
                "timeout-resume.md",
                "lemma-discovery.md",
                "klean-prove.md",
                "klean-audit.md",
            },
        )

    def test_exactly_four_condition_prompts_exist(self) -> None:
        paths = generation_prompt_paths()
        self.assertEqual(len(paths), 4)
        self.assertTrue(all(path.is_file() for path in paths))

    def test_prompts_require_fresh_implementation_without_answer_language(self) -> None:
        forbidden = ("canonical.py", "GOLDEN", "copy the reference", "copy `")
        for path in generation_prompt_paths():
            text = path.read_text()
            self.assertIn("`prompt.py`", text, path.name)
            self.assertIn("create `solution.py`", text, path.name)
            self.assertIn("KPROVE_PASSED", text, path.name)
            for phrase in forbidden:
                self.assertNotIn(phrase, text, path.name)

    def test_kit_prompts_defer_to_gate_status(self) -> None:
        for name in ("kit-bare.md", "kit-semantics.md"):
            text = (REPO / "prompts" / name).read_text()
            self.assertIn("Gate A", text)
            self.assertIn("Gate B", text)
            self.assertIn("Gate C", text)
            self.assertIn("PROOF.md", text)
            self.assertIn("full HumanEval contract", text)
            self.assertIn("bounded unrollings", text)
            self.assertIn("A `SOUND-BUT-LIMITED` result is", text)

    def test_kit_prompt_deliverables_include_proof_report(self) -> None:
        for name in ("kit-bare.md", "kit-semantics.md"):
            text = (REPO / "prompts" / name).read_text()
            deliverables = text.split("## Deliverables\n\n", 1)[1].split("\n\n", 1)[0]
            self.assertIn("`PROOF.md`", deliverables, name)

    def test_prompts_use_ordered_runner_result_decision(self) -> None:
        for path in generation_prompt_paths():
            text = " ".join(path.read_text().split())
            self.assertIn(
                "Choose exactly one marker using this ordered decision; stop at "
                "the first matching case.",
                text,
                path.name,
            )
            passed = text.find(
                "1. `KPROVE_PASSED` iff every required positive target-proof command"
            )
            blocked = text.find(
                "2. Otherwise, `BLOCKED` iff a concrete hard blocker"
            )
            partial = text.find("3. Otherwise, `PARTIAL`")
            self.assertNotEqual(-1, passed, path.name)
            self.assertNotEqual(-1, blocked, path.name)
            self.assertNotEqual(-1, partial, path.name)
            self.assertLess(passed, blocked, path.name)
            self.assertLess(blocked, partial, path.name)
            self.assertIn(
                "commands intended to close the task's proof claims",
                text,
                path.name,
            )
            self.assertIn(
                "Expected-failure mutation probes and other negative validation "
                "probes are judged by their expected non-zero result and do not "
                "disqualify this marker.",
                text,
                path.name,
            )
            self.assertIn(
                "the positive proof condition was not met",
                text,
                path.name,
            )
            self.assertIn(
                "This ordered precedence is total and mutually exclusive. "
                "Incomplete deliverables or a later Gate status do not create a "
                "second marker.",
                text,
                path.name,
            )

    def test_kit_prompts_separate_runner_result_from_proof_quality(self) -> None:
        for name in ("kit-bare.md", "kit-semantics.md"):
            text = " ".join((REPO / "prompts" / name).read_text().split())
            for headline in (
                "`Incomplete work`",
                "`SOUND-BUT-LIMITED`",
                "`FORMALLY-SOUND-UNVALIDATED`",
                "`VALIDATED`",
            ):
                self.assertIn(headline, text, name)
            self.assertIn(
                "The final `RESULT:` runner marker is separate from the `PROOF.md` "
                "proof-quality headline.",
                text,
                name,
            )
            self.assertIn(
                "`KPROVE_PASSED` reports positive target-proof execution only; it "
                "neither requires nor implies a `VALIDATED` proof-quality headline",
                text,
                name,
            )
            self.assertIn(
                "never equate that execution marker with soundness or intent "
                "validation",
                text,
                name,
            )


class DocumentationTests(unittest.TestCase):
    def test_active_harness_has_no_canonical_copy_preserve_or_instruction_path(
        self,
    ) -> None:
        offenders = []
        active_harness_files = list(generation_prompt_paths())
        active_harness_files.extend(
            candidate
            for candidate in (REPO / "docker").rglob("*")
            if candidate.is_file()
            and "audit" not in candidate.relative_to(REPO / "docker").parts
        )
        for path in sorted(active_harness_files):
            relative = path.relative_to(REPO)
            if "secrets" in relative.parts or path.name == ".env":
                continue
            if "canonical.py" in path.read_text(errors="ignore"):
                offenders.append(str(relative))
        for path in sorted((REPO / "tools").iterdir()):
            if (
                path.is_file()
                and path.name != "populate_runs.py"
                and path.suffix in {".py", ".sh", ".txt"}
                and "canonical.py" in path.read_text(errors="ignore")
            ):
                offenders.append(str(path.relative_to(REPO)))
        self.assertEqual(offenders, [])

        populator_path = REPO / "tools/populate_runs.py"
        source = populator_path.read_text()
        tree = ast.parse(source)
        literals = [
            node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and "canonical.py" in node.value
        ]
        self.assertCountEqual(
            literals, ["canonical.py", ": canonical.py is forbidden"]
        )
        rejection_calls = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "rglob"
            and len(node.args) == 1
            and isinstance(node.args[0], ast.Constant)
            and node.args[0].value == "canonical.py"
        ]
        self.assertEqual(len(rejection_calls), 1)
        copy_calls = [
            ast.get_source_segment(source, node) or ""
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in {"copy", "copy2", "copytree"}
        ]
        self.assertNotIn("canonical.py", "\n".join(copy_calls))

    def test_claude_reset_scripts_preserve_exact_seed_inputs(self) -> None:
        expected = [
            "prompt.py",
            "py2mpy.py",
            "run-input.json",
            "reference-semantics",
        ]
        for relative in (
            "docker/claude-code/babysit.sh",
            "tools/opus_throttle.sh",
        ):
            with self.subTest(script=relative):
                source = " ".join((REPO / relative).read_text().split())
                matches = re.findall(
                    r'find "\$d" -mindepth 1 -maxdepth 1 (.*?) '
                    r'-exec rm -rf \{\} \+',
                    source,
                )
                self.assertEqual(len(matches), 1)
                self.assertEqual(
                    re.findall(r"! -name ([A-Za-z0-9._-]+)", matches[0]),
                    expected,
                )

    def test_claude_throttle_launches_only_through_validating_wrapper(self) -> None:
        throttle = (REPO / "tools/opus_throttle.sh").read_text()
        active = " ".join(
            line.strip()
            for line in throttle.splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ).replace("\\ ", "")
        launch = (
            'bash "$REPO/docker/claude-code/run_task.sh" "$CFG" "$PROB" '
            '>> "$REPO/_setup/opus_throttle_tasks.log" 2>&1 &'
        )
        self.assertEqual(active.count(launch), 1)
        queue = re.search(r"EXPECTED_CONFIGS=\((.*?)\)", throttle, re.DOTALL)
        self.assertIsNotNone(queue)
        self.assertEqual(
            queue.group(1).split(),
            [
                "claude-code-opus-xhigh-4-8-bare",
                "claude-code-opus-xhigh-4-8-semantics",
                "claude-code-opus-xhigh-4-8-kit",
                "claude-code-opus-xhigh-4-8-kit-semantics",
            ],
        )
        for bypass in ("docker compose", "prompt_for", "KITV", "COMPOSE="):
            self.assertNotIn(bypass, active)

        matrix = (REPO / "docker/claude-code/run_matrix.sh").read_text()
        matrix_active = " ".join(
            line.strip()
            for line in matrix.splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ).replace("\\ ", "")
        self.assertEqual(matrix_active.count('"$HERE/run_task.sh"'), 1)
        self.assertNotIn("docker compose", matrix_active)

        babysit = (REPO / "docker/claude-code/babysit.sh").read_text()
        babysit_active = " ".join(
            line.strip()
            for line in babysit.splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ).replace("\\ ", "")
        self.assertIn(
            'supervise_matrix "$HERE/run_matrix.sh"', babysit_active
        )
        self.assertNotIn("docker compose", babysit_active)

        wrapper = (REPO / "docker/claude-code/run_task.sh").read_text()
        self.assertLess(
            wrapper.index("--validate-task"), wrapper.index("docker compose")
        )

    def test_claude_matrix_and_status_ignore_nonactive_directories(self) -> None:
        matrix = " ".join(
            (REPO / "docker/claude-code/run_matrix.sh").read_text().split()
        )
        self.assertIn("ls -d claude-code-*/", matrix)
        self.assertNotIn("ls -d */", matrix)

        status = (REPO / "docker/claude-code/status.sh").read_text()
        self.assertIn("cfg == 'archive'", status)
        self.assertIn("cfg.startswith('.')", status)

    def test_reference_semantics_documents_supported_compilation_routes(self) -> None:
        contents = (REPO / "data/reference/src/semantics.k").read_bytes()
        marker = b'requires "semantics/syntax.k"'
        self.assertIn(marker, contents)
        header, tail = contents.split(marker, 1)
        joined = header.decode()
        self.assertIn("--main-module MPY-KRUN", joined)
        self.assertIn(
            "Proof definitions import\n// MPY and any explicit proof extensions",
            joined,
        )
        self.assertNotIn("reference/tests/run.sh", joined)
        self.assertNotIn("lemmas/lemmas.k", joined)
        digest = hashlib.sha256(marker + tail).hexdigest()
        self.assertEqual(
            digest,
            "d17137c3064fe6d70ee1113b43025494aeeff747833ee53fcc956d2984cd1c59",
        )

    def test_root_readme_documents_benchmark_boundaries(self) -> None:
        text = (REPO / "README.md").read_text()
        normalized = " ".join(text.split())
        required = (
            "`prompt.py`",
            "`py2mpy.py`",
            "`run-input.json`",
            "`reference-semantics/`",
            "`/kit-skills`",
            "`canonical.py`",
            "official tests",
            "oracle",
            "Codex and Claude support all four conditions",
            "OpenCode supports only `bare` and `semantics`",
            "only supported launcher inspection mechanism",
            "`--print-config`",
            "`--validate-task`",
            "46af96a89de7b297e9dd4e9cfc2bf248e6d4698f",
            "ac515c9de2c87ac2366c9ea3d55c78cad172897b",
            "schema version 2",
            "python3 tools/check_kit_bundle.py",
            "python3 tools/populate_runs.py",
            "bash tests/smoke-containers.sh",
            "separate verifier",
            "`runs/archive/` is immutable",
            "24 task folders per configuration",
            "does not launch",
            "Stop before any sample launch",
        )
        for fragment in required:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, normalized)

    def test_runner_docs_describe_safe_routing_and_result_marker(self) -> None:
        docs = {
            runner: (REPO / "docker" / runner / "README.md").read_text()
            for runner in ("codex", "claude-code", "opencode")
        }
        for runner, text in docs.items():
            with self.subTest(runner=runner):
                for fragment in (
                    "`prompt.py`",
                    "`run-input.json`",
                    "`--print-config`",
                    "`--validate-task`",
                    "`KPROVE_PASSED`",
                ):
                    self.assertIn(fragment, text)
        for runner in ("codex", "claude-code"):
            with self.subTest(runner=runner):
                self.assertIn("`kit-semantics`", docs[runner])
                self.assertIn("`docker-compose.kit.yml`", docs[runner])
                self.assertIn("no Kit mount", docs[runner])
        self.assertIn("does not support Kit conditions", docs["opencode"])

    def test_resumable_klean_pipeline_is_fully_documented(self) -> None:
        root = (REPO / "README.md").read_text()
        codex = (REPO / "docker/codex/README.md").read_text()
        klean = (REPO / "docker/klean/README.md").read_text()
        lean_audit = (REPO / "docker/klean-audit/README.md").read_text()
        combined = "\n".join((root, codex, klean, lean_audit))
        for fragment in (
            "01-k-proof",
            "02-k-audit",
            "03-lemma-discovery",
            "04-klean-generation",
            "05-lean-proof",
            "06-lean-audit",
            "resume_lemma_discovery_task.sh",
            "resume_lean_task.sh",
            "KLEAN_NO_OBLIGATIONS still proceeds to Stage 6",
            "same Codex session",
            "20-minute",
            "one-hour initial",
            "two-hour default cumulative",
            "does not receive Stage 2 audit feedback",
            "classification-only",
            "classification-plus-proof",
            "3,600",
            "runner-state/",
            "python3 tools/create_run.py",
            "python3 tools/run_pipeline.py status",
            "python3 tools/run_pipeline.py run",
            "python3 tools/migrate_six_stage_layout.py --dry-run",
            "python3 tools/migrate_six_stage_layout.py --apply",
            "Active runs must not be migrated",
            "docker/klean/generate_task.sh",
            "docker/klean-audit/run_task.sh",
            "manual",
            "KLEAN_PREFLIGHT_ERROR",
            "AUDIT_ERROR",
            "must not be archived",
            "No live model",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, combined)
        for obsolete in (
            "Resumable five-stage K/Klean/Lean pipeline",
            "The terminal `KLEAN_NO_OBLIGATIONS` status",
            "the terminal `KLEAN_NO_OBLIGATIONS` status",
        ):
            with self.subTest(obsolete=obsolete):
                self.assertNotIn(obsolete, combined)
        for text, fragments in (
            (
                root,
                (
                    "In both modes, a separate no-network mechanical "
                    "container reruns deterministic preflight",
                    "Classification-only confirms the no-obligation "
                    "generation",
                    "Proof mode additionally clean-builds and type-checks "
                    "the candidate",
                ),
            ),
            (
                lean_audit,
                (
                    "In both modes, the no-network, no-auth mechanical "
                    "container reruns deterministic Klean preflight",
                    "Classification-only confirms the no-obligation "
                    "generation",
                    "Proof mode additionally runs `lake clean` and "
                    "`lake build`",
                ),
            ),
        ):
            for fragment in fragments:
                with self.subTest(stage6_fragment=fragment):
                    self.assertIn(fragment, text)
        self.assertNotIn(
            "In classification-plus-proof mode, a separate no-network",
            lean_audit,
        )

    def test_population_brief_uses_isolated_condition_contract(self) -> None:
        text = (REPO / "tools/populate_prompt.txt").read_text()
        for fragment in (
            "prompt.py",
            "run-input.json",
            "bare",
            "semantics",
            "kit",
            "kit-semantics",
            "docker-compose.kit.yml",
            "KPROVE_PASSED",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)


class KitBundleTests(unittest.TestCase):
    def assert_bundle_rejected(self, checker, bundle: Path, lock: dict) -> None:
        lock_path = bundle.parent / "kit-skills.lock.json"
        lock_path.write_text(json.dumps(lock))
        with (
            mock.patch.object(checker, "LOCK_PATH", lock_path),
            mock.patch.object(checker, "BUNDLE", bundle),
            mock.patch.object(sys, "argv", ["check_kit_bundle.py"]),
            self.assertRaises(SystemExit),
        ):
            checker.main()

    def test_bundled_files_match_lock(self) -> None:
        lock = json.loads((REPO / "data/kit-skills.lock.json").read_text())
        self.assertEqual(lock.get("schema_version"), 2)
        self.assertEqual(
            lock["commit"], "46af96a89de7b297e9dd4e9cfc2bf248e6d4698f"
        )
        self.assertEqual(
            lock["skills_tree"], "ac515c9de2c87ac2366c9ea3d55c78cad172897b"
        )
        actual = {}
        for path in sorted(p for p in (REPO / "data/skills").rglob("*") if p.is_file()):
            actual[path.relative_to(REPO / "data/skills").as_posix()] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
        self.assertEqual(actual, lock["files"])

    def test_bundle_contains_seven_skills_and_shared_contract(self) -> None:
        skills = list((REPO / "data/skills").glob("*/SKILL.md"))
        self.assertEqual(len(skills), 7)
        self.assertTrue(
            (REPO / "data/skills/shared/proof-extension-soundness.md").is_file()
        )

    def test_build_lock_rejects_unstaged_source_skill_edit(self) -> None:
        checker = load_kit_checker()
        with tempfile.TemporaryDirectory() as tmp:
            source = make_kit_source(Path(tmp))
            (source / "skills/example/SKILL.md").write_text("# Edited\n")
            with self.assertRaisesRegex(ValueError, "source"):
                checker.build_lock(source)

    def test_build_lock_rejects_staged_source_change(self) -> None:
        checker = load_kit_checker()
        with tempfile.TemporaryDirectory() as tmp:
            source = make_kit_source(Path(tmp))
            skill = source / "skills/example/SKILL.md"
            skill.write_text("# Staged\n")
            git(source, "add", "skills/example/SKILL.md")
            skill.write_text("# Example\n")
            with self.assertRaisesRegex(ValueError, "source"):
                checker.build_lock(source)

    def test_build_lock_rejects_untracked_source_skill(self) -> None:
        checker = load_kit_checker()
        with tempfile.TemporaryDirectory() as tmp:
            source = make_kit_source(Path(tmp))
            (source / "skills/untracked.md").write_text("unexpected\n")
            with self.assertRaisesRegex(ValueError, "source"):
                checker.build_lock(source)

    def test_build_lock_rejects_ignored_source_skill(self) -> None:
        checker = load_kit_checker()
        with tempfile.TemporaryDirectory() as tmp:
            source = make_kit_source(Path(tmp))
            (source / ".git/info/exclude").write_text("skills/ignored.md\n")
            (source / "skills/ignored.md").write_text("unexpected\n")
            with self.assertRaisesRegex(ValueError, "source"):
                checker.build_lock(source)

    def test_build_lock_rejects_dirty_plugin_manifest(self) -> None:
        checker = load_kit_checker()
        with tempfile.TemporaryDirectory() as tmp:
            source = make_kit_source(Path(tmp))
            (source / ".codex-plugin/plugin.json").write_text(
                '{"version": "9.9.9"}\n'
            )
            with self.assertRaisesRegex(ValueError, "source"):
                checker.build_lock(source)

    def test_write_lock_rejects_dirty_source_before_replacing_lock(self) -> None:
        checker = load_kit_checker()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = make_kit_source(root)
            lock_path = root / "kit-skills.lock.json"
            lock_path.write_text("sentinel\n")
            (source / "skills/example/SKILL.md").write_text("# Edited\n")
            with (
                mock.patch.object(checker, "LOCK_PATH", lock_path),
                mock.patch.object(checker, "BUNDLE", source / "skills"),
                mock.patch.object(
                    sys,
                    "argv",
                    ["check_kit_bundle.py", "--source", str(source), "--write-lock"],
                ),
                self.assertRaises(SystemExit),
            ):
                checker.main()
            self.assertEqual(lock_path.read_text(), "sentinel\n")

    def test_write_lock_preserves_lock_when_clean_source_diverges_from_bundle(
        self,
    ) -> None:
        checker = load_kit_checker()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = make_kit_source(root)
            skill = source / "skills/example/SKILL.md"
            skill.write_text("# Divergent\n")
            git(source, "add", "skills/example/SKILL.md")
            git(
                source,
                "-c",
                "user.name=Benchmark Test",
                "-c",
                "user.email=benchmark@example.invalid",
                "commit",
                "-qm",
                "divergent source",
            )
            bundle, _, _ = make_bundle(root)
            lock_path = root / "kit-skills.lock.json"
            sentinel = b"sentinel lock bytes\n"
            lock_path.write_bytes(sentinel)
            with (
                mock.patch.object(checker, "LOCK_PATH", lock_path),
                mock.patch.object(checker, "BUNDLE", bundle),
                mock.patch.object(
                    sys,
                    "argv",
                    ["check_kit_bundle.py", "--source", str(source), "--write-lock"],
                ),
                self.assertRaises(SystemExit),
            ):
                checker.main()
            self.assertEqual(lock_path.read_bytes(), sentinel)

    def test_write_lock_preserves_lock_when_final_source_check_fails(self) -> None:
        checker = load_kit_checker()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            bundle, _, candidate = make_bundle(root)
            lock_path = root / "kit-skills.lock.json"
            sentinel = b"sentinel lock bytes\n"
            lock_path.write_bytes(sentinel)
            with (
                mock.patch.object(checker, "LOCK_PATH", lock_path),
                mock.patch.object(checker, "BUNDLE", bundle),
                mock.patch.object(
                    checker,
                    "build_lock",
                    side_effect=[candidate, checker.BundleError("source changed")],
                ),
                mock.patch.object(
                    sys,
                    "argv",
                    ["check_kit_bundle.py", "--source", str(source), "--write-lock"],
                ),
                self.assertRaises(SystemExit),
            ):
                checker.main()
            self.assertEqual(lock_path.read_bytes(), sentinel)

    def test_build_lock_records_complete_topology_and_modes(self) -> None:
        checker = load_kit_checker()
        with tempfile.TemporaryDirectory() as tmp:
            source = make_kit_source(Path(tmp))
            lock = checker.build_lock(source)
            self.assertEqual(lock.get("schema_version"), 2)
            self.assertEqual(
                lock.get("entries"),
                {
                    ".": {"type": "directory", "mode": "0755"},
                    "example": {"type": "directory", "mode": "0755"},
                    "example/SKILL.md": {"type": "file", "mode": "0644"},
                },
            )

    def test_build_lock_rejects_untracked_empty_source_directory(self) -> None:
        checker = load_kit_checker()
        with tempfile.TemporaryDirectory() as tmp:
            source = make_kit_source(Path(tmp))
            (source / "skills/empty").mkdir()
            with self.assertRaisesRegex(ValueError, "source"):
                checker.build_lock(source)

    def test_bundle_rejects_identical_byte_file_symlink(self) -> None:
        checker = load_kit_checker()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundle, skill, lock = make_bundle(root)
            target = root / "outside.md"
            target.write_bytes(skill.read_bytes())
            skill.unlink()
            skill.symlink_to(target)
            self.assert_bundle_rejected(checker, bundle, lock)

    def test_bundle_rejects_live_directory_symlink(self) -> None:
        checker = load_kit_checker()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundle, _, lock = make_bundle(root, empty_slot=True)
            slot = bundle / "slot"
            slot.rmdir()
            target = root / "outside"
            target.mkdir()
            slot.symlink_to(target, target_is_directory=True)
            self.assert_bundle_rejected(checker, bundle, lock)

    def test_bundle_rejects_broken_symlink(self) -> None:
        checker = load_kit_checker()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundle, _, lock = make_bundle(root, empty_slot=True)
            slot = bundle / "slot"
            slot.rmdir()
            slot.symlink_to(root / "missing")
            self.assert_bundle_rejected(checker, bundle, lock)

    def test_bundle_rejects_unexpected_empty_directory(self) -> None:
        checker = load_kit_checker()
        with tempfile.TemporaryDirectory() as tmp:
            bundle, _, lock = make_bundle(Path(tmp))
            (bundle / "unexpected").mkdir()
            self.assert_bundle_rejected(checker, bundle, lock)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "os.mkfifo is unavailable")
    def test_bundle_rejects_fifo(self) -> None:
        checker = load_kit_checker()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundle, _, lock = make_bundle(root, empty_slot=True)
            slot = bundle / "slot"
            slot.rmdir()
            os.mkfifo(slot)
            self.assert_bundle_rejected(checker, bundle, lock)

    def test_bundle_rejects_permission_mode_mismatch(self) -> None:
        checker = load_kit_checker()
        with tempfile.TemporaryDirectory() as tmp:
            bundle, skill, lock = make_bundle(Path(tmp))
            skill.chmod(0o600)
            self.assert_bundle_rejected(checker, bundle, lock)


def load_populator():
    path = REPO / "tools/populate_runs.py"
    spec = importlib.util.spec_from_file_location("populate_runs", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PopulationTests(unittest.TestCase):
    def test_condition_suffixes_are_unambiguous(self) -> None:
        module = load_populator()
        cases = {
            "codex-model-xhigh-bare": (False, False, "bare.md"),
            "codex-model-xhigh-semantics": (False, True, "with-semantics.md"),
            "codex-model-xhigh-kit": (True, False, "kit-bare.md"),
            "codex-model-xhigh-kit-semantics": (True, True, "kit-semantics.md"),
        }
        for config, expected in cases.items():
            condition = module.parse_condition(config)
            self.assertEqual(
                (condition.kit, condition.semantics, condition.prompt_file), expected
            )

    def test_populated_kit_semantics_task_never_contains_canonical(self) -> None:
        module = load_populator()
        with tempfile.TemporaryDirectory() as tmp:
            runs = Path(tmp) / "runs"
            module.populate(
                "codex-test-xhigh-kit-semantics", repo=REPO, runs_root=runs
            )
            task = runs / "codex-test-xhigh-kit-semantics" / "8-sum-product"
            self.assertTrue((task / "prompt.py").is_file())
            self.assertTrue((task / "py2mpy.py").is_file())
            self.assertTrue((task / "reference-semantics/semantics.k").is_file())
            self.assertTrue((task / "run-input.json").is_file())
            self.assertFalse((task / "canonical.py").exists())

    def test_existing_answer_visible_task_is_rejected(self) -> None:
        module = load_populator()
        with tempfile.TemporaryDirectory() as tmp:
            runs = Path(tmp) / "runs"
            task = runs / "codex-test-xhigh-bare" / "8-sum-product"
            task.mkdir(parents=True)
            (task / "canonical.py").write_text("def answer(): return 42\n")
            with self.assertRaisesRegex(module.SeedContractError, "canonical.py"):
                module.populate("codex-test-xhigh-bare", repo=REPO, runs_root=runs)

    def test_nested_answer_visible_task_is_rejected(self) -> None:
        module = load_populator()
        with tempfile.TemporaryDirectory() as tmp:
            runs = Path(tmp) / "runs"
            config = "codex-test-xhigh-bare"
            module.populate(config, repo=REPO, runs_root=runs)
            task = runs / config / "8-sum-product"
            nested = task / "generated/evidence"
            nested.mkdir(parents=True)
            (nested / "canonical.py").write_text("def answer(): return 42\n")
            with self.assertRaisesRegex(module.SeedContractError, "canonical.py"):
                module.populate(config, repo=REPO, runs_root=runs)

    def test_task_directory_symlink_escape_is_rejected(self) -> None:
        module = load_populator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runs = root / "runs"
            config = "codex-test-xhigh-bare"
            module.populate(config, repo=REPO, runs_root=runs)
            task = runs / config / "8-sum-product"
            escaped = root / "escaped-task"
            task.rename(escaped)
            task.symlink_to(escaped, target_is_directory=True)
            with self.assertRaisesRegex(module.SeedContractError, "task directory"):
                module.populate(config, repo=REPO, runs_root=runs)

    def test_broken_task_directory_symlink_is_rejected(self) -> None:
        module = load_populator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runs = root / "runs"
            config = "codex-test-xhigh-bare"
            task = runs / config / "8-sum-product"
            task.parent.mkdir(parents=True)
            task.symlink_to(root / "missing-task", target_is_directory=True)
            with self.assertRaisesRegex(module.SeedContractError, "task directory"):
                module.populate(config, repo=REPO, runs_root=runs)

    def test_required_seed_file_symlinks_are_rejected(self) -> None:
        module = load_populator()
        sources = {
            "prompt.py": REPO / "data/questions/8-sum-product/prompt.py",
            "py2mpy.py": REPO / "tools/py2mpy.py",
        }
        for filename, source in sources.items():
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as tmp:
                runs = Path(tmp) / "runs"
                config = "codex-test-xhigh-bare"
                module.populate(config, repo=REPO, runs_root=runs)
                seed = runs / config / "8-sum-product" / filename
                seed.unlink()
                seed.symlink_to(source)
                with self.assertRaisesRegex(module.SeedContractError, "symlink"):
                    module.populate(config, repo=REPO, runs_root=runs)

    def test_existing_task_without_manifest_is_rejected(self) -> None:
        module = load_populator()
        with tempfile.TemporaryDirectory() as tmp:
            runs = Path(tmp) / "runs"
            config = "codex-test-xhigh-bare"
            module.populate(config, repo=REPO, runs_root=runs)
            manifest = runs / config / "8-sum-product/run-input.json"
            manifest.unlink()
            with self.assertRaisesRegex(module.SeedContractError, "run-input.json"):
                module.populate(config, repo=REPO, runs_root=runs)

    def test_existing_task_with_malformed_manifest_is_rejected(self) -> None:
        module = load_populator()
        with tempfile.TemporaryDirectory() as tmp:
            runs = Path(tmp) / "runs"
            config = "codex-test-xhigh-bare"
            module.populate(config, repo=REPO, runs_root=runs)
            manifest = runs / config / "8-sum-product/run-input.json"
            manifest.write_text("{not-json\n")
            with self.assertRaisesRegex(module.SeedContractError, "run-input.json"):
                module.populate(config, repo=REPO, runs_root=runs)

    def test_existing_task_with_stale_manifest_is_rejected(self) -> None:
        module = load_populator()
        with tempfile.TemporaryDirectory() as tmp:
            runs = Path(tmp) / "runs"
            config = "codex-test-xhigh-bare"
            module.populate(config, repo=REPO, runs_root=runs)
            manifest = runs / config / "8-sum-product/run-input.json"
            stale = json.loads(manifest.read_text())
            stale["inputs"]["translator_sha256"] = "0" * 64
            manifest.write_text(json.dumps(stale, indent=2, sort_keys=True) + "\n")
            with self.assertRaisesRegex(module.SeedContractError, "run-input.json"):
                module.populate(config, repo=REPO, runs_root=runs)

    def test_extra_reference_semantics_file_is_rejected(self) -> None:
        module = load_populator()
        with tempfile.TemporaryDirectory() as tmp:
            runs = Path(tmp) / "runs"
            config = "codex-test-xhigh-semantics"
            module.populate(config, repo=REPO, runs_root=runs)
            task = runs / config / "8-sum-product"
            extra = task / "reference-semantics/generated/oracle.py"
            extra.parent.mkdir(parents=True)
            extra.write_text("def oracle(): return 42\n")
            with self.assertRaisesRegex(
                module.SeedContractError, "reference-semantics"
            ):
                module.populate(config, repo=REPO, runs_root=runs)

    def test_extra_empty_reference_semantics_directory_is_rejected(self) -> None:
        module = load_populator()
        with tempfile.TemporaryDirectory() as tmp:
            runs = Path(tmp) / "runs"
            config = "codex-test-xhigh-semantics"
            module.populate(config, repo=REPO, runs_root=runs)
            task = runs / config / "8-sum-product"
            (task / "reference-semantics/unexpected-empty").mkdir()
            with self.assertRaisesRegex(
                module.SeedContractError, "reference-semantics"
            ):
                module.populate(config, repo=REPO, runs_root=runs)

    def test_broken_reference_semantics_symlink_is_rejected_for_bare(self) -> None:
        module = load_populator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runs = root / "runs"
            config = "codex-test-xhigh-bare"
            module.populate(config, repo=REPO, runs_root=runs)
            task = runs / config / "8-sum-product"
            semantics = task / "reference-semantics"
            semantics.symlink_to(root / "missing-semantics", target_is_directory=True)
            with self.assertRaisesRegex(
                module.SeedContractError, "reference-semantics"
            ):
                module.populate(config, repo=REPO, runs_root=runs)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "os.mkfifo is unavailable")
    def test_reference_semantics_fifo_is_rejected_without_reading(self) -> None:
        module = load_populator()
        with tempfile.TemporaryDirectory() as tmp:
            runs = Path(tmp) / "runs"
            config = "codex-test-xhigh-semantics"
            module.populate(config, repo=REPO, runs_root=runs)
            task = runs / config / "8-sum-product"
            os.mkfifo(task / "reference-semantics/unexpected.fifo")
            with self.assertRaisesRegex(
                module.SeedContractError, "reference-semantics"
            ):
                module.populate(config, repo=REPO, runs_root=runs)

    def test_failed_manifest_build_leaves_no_partial_task(self) -> None:
        module = load_populator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            problem_id = "example"
            prompt = repo / "data/questions" / problem_id / "prompt.py"
            prompt.parent.mkdir(parents=True)
            prompt.write_text("def example(x):\n    pass\n")
            selection = repo / "data/selection.json"
            selection.parent.mkdir(parents=True, exist_ok=True)
            selection.write_text(json.dumps({"selected": [{"id": problem_id}]}))
            translator = repo / "tools/py2mpy.py"
            translator.parent.mkdir(parents=True)
            translator.write_text("# translator\n")
            runs = root / "runs"
            config = "codex-test-xhigh-bare"
            with self.assertRaises(FileNotFoundError):
                module.populate(config, repo=repo, runs_root=runs)
            self.assertFalse((runs / config / problem_id).exists())

    def test_archive_path_config_is_rejected(self) -> None:
        module = load_populator()
        with tempfile.TemporaryDirectory() as tmp:
            runs = Path(tmp) / "runs"
            with self.assertRaisesRegex(ValueError, "safe path component"):
                module.populate(
                    "archive/retry-bare", repo=REPO, runs_root=runs
                )
            self.assertFalse((runs / "archive").exists())

    def test_absolute_path_config_is_rejected(self) -> None:
        module = load_populator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runs = root / "runs"
            escaped = root / "escaped-bare"
            with self.assertRaisesRegex(ValueError, "safe path component"):
                module.populate(str(escaped), repo=REPO, runs_root=runs)
            self.assertFalse(escaped.exists())
            self.assertFalse(runs.exists())

    def test_safe_single_component_config_is_accepted(self) -> None:
        module = load_populator()
        with tempfile.TemporaryDirectory() as tmp:
            runs = Path(tmp) / "runs"
            config = "codex-safe-xhigh-bare"
            self.assertEqual(
                module.populate(config, repo=REPO, runs_root=runs), (24, 0)
            )
            self.assertTrue(
                (runs / config / "8-sum-product/run-input.json").is_file()
            )

    def test_populated_bare_task_has_only_bare_seed_inputs(self) -> None:
        module = load_populator()
        with tempfile.TemporaryDirectory() as tmp:
            runs = Path(tmp) / "runs"
            module.populate("codex-test-xhigh-bare", repo=REPO, runs_root=runs)
            task = runs / "codex-test-xhigh-bare" / "8-sum-product"
            self.assertTrue((task / "prompt.py").is_file())
            self.assertTrue((task / "py2mpy.py").is_file())
            self.assertFalse((task / "canonical.py").exists())
            self.assertFalse((task / "reference-semantics").exists())


class RunnerIsolationTests(unittest.TestCase):
    PROBLEM = "8-sum-product"

    def setUp(self) -> None:
        self.fixture = tempfile.TemporaryDirectory(
            prefix="runner-isolation-repo-", dir="/tmp"
        )
        self.repo = Path(self.fixture.name) / "repo"
        self._copy_runner_fixture()
        self.runs = self.repo / "runs"
        self.runs.mkdir()
        (self.runs / "archive").mkdir()
        self.created_configs: set[str] = set()
        self.populator = load_populator()
        self.outside = tempfile.TemporaryDirectory(
            prefix="runner-isolation-outside-", dir="/tmp"
        )
        self.fake_bin = tempfile.TemporaryDirectory(
            prefix="runner-isolation-bin-", dir="/tmp"
        )
        self.docker_marker = Path(self.fake_bin.name) / "docker-called"
        fake_docker = Path(self.fake_bin.name) / "docker"
        fake_docker.write_text(
            "#!/bin/sh\n"
            ': > "$RUNNER_DOCKER_MARKER"\n'
            'echo "launcher attempted to invoke Docker" >&2\n'
            "exit 99\n"
        )
        fake_docker.chmod(0o755)

    def _copy_runner_fixture(self) -> None:
        files = (
            "tools/populate_runs.py",
            "tools/py2mpy.py",
            "data/questions/8-sum-product/prompt.py",
            "data/kit-skills.lock.json",
            "prompts/bare.md",
            "prompts/with-semantics.md",
            "prompts/kit-bare.md",
            "prompts/kit-semantics.md",
            "docker/codex/run_task.sh",
            "docker/claude-code/run_task.sh",
            "docker/opencode/run_task.sh",
        )
        for relative in files:
            source = REPO / relative
            destination = self.repo / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        shutil.copytree(
            REPO / "data/reference/src", self.repo / "data/reference/src"
        )

    def tearDown(self) -> None:
        self.fake_bin.cleanup()
        self.outside.cleanup()
        self.fixture.cleanup()

    def compose_config(self, runner: str, kit: bool) -> str:
        directory = REPO / "docker" / runner
        command = ["docker", "compose", "-f", str(directory / "docker-compose.yml")]
        if kit:
            command += ["-f", str(directory / "docker-compose.kit.yml")]
        command += ["config"]
        env = os.environ | {
            "TASK_DIR": str(REPO / "data/questions/8-sum-product")
        }
        return subprocess.run(
            command, check=True, capture_output=True, text=True, env=env
        ).stdout

    def prepare_task(self, config: str, problem: str = PROBLEM) -> Path:
        config_dir = self.runs / config
        if config not in self.created_configs:
            self.assertFalse(config_dir.exists(), f"test config already exists: {config}")
            self.created_configs.add(config)
        task_dir = config_dir / problem
        task_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(
            self.repo / "data/questions/8-sum-product/prompt.py", task_dir
        )
        shutil.copy2(self.repo / "tools/py2mpy.py", task_dir)
        condition = self.populator.parse_condition(config)
        if condition.semantics:
            shutil.copytree(
                self.repo / "data/reference/src",
                task_dir / "reference-semantics",
            )
        manifest = self.populator.build_manifest(self.repo, config, problem)
        (task_dir / "run-input.json").write_text(
            self.populator.render_manifest(manifest)
        )
        self.populator.validate_task_seed(self.repo, config, problem, task_dir)
        return task_dir

    def register_config(self, config: str) -> Path:
        config_dir = self.runs / config
        self.assertFalse(config_dir.exists() or config_dir.is_symlink())
        self.created_configs.add(config)
        return config_dir

    @staticmethod
    def runner_config(runner: str, label: str, condition: str = "bare") -> str:
        if runner == "codex":
            return f"codex-{label}-xhigh-{condition}"
        if runner == "claude-code":
            return f"claude-code-opus-xhigh-{label}-{condition}"
        if runner == "opencode":
            return f"opencode-{label}-{condition}"
        raise AssertionError(f"unknown runner: {runner}")

    def print_config_result(
        self,
        runner: str,
        config: str,
        problem: str = PROBLEM,
        *,
        prepare: bool = True,
        extra_args: tuple[str, ...] = (),
    ) -> subprocess.CompletedProcess[str]:
        if prepare:
            self.prepare_task(config, problem)
        env = os.environ | {
            "PATH": f"{self.fake_bin.name}{os.pathsep}{os.environ['PATH']}",
            "RUNNER_DOCKER_MARKER": str(self.docker_marker),
        }
        result = subprocess.run(
            [
                str(self.repo / "docker" / runner / "run_task.sh"),
                "--print-config",
                config,
                problem,
                *extra_args,
            ],
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertFalse(
            self.docker_marker.exists(),
            f"{runner} invoked Docker while inspecting {config}",
        )
        return result

    def validate_task_result(
        self, config: str, task_dir: Path
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(self.repo / "tools/populate_runs.py"),
                "--validate-task",
                config,
                self.PROBLEM,
                str(task_dir),
            ],
            capture_output=True,
            text=True,
        )

    def print_config(
        self, runner: str, config: str, problem: str = PROBLEM
    ) -> str:
        result = self.print_config_result(runner, config, problem)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def assert_print_config(
        self,
        runner: str,
        config: str,
        *,
        model: str,
        condition: str,
        prompt: str,
        kit: int,
    ) -> None:
        task_dir = self.repo / "runs" / config / self.PROBLEM
        expected = [
            f"config={config}",
            f"problem={self.PROBLEM}",
            f"task_dir={task_dir}",
            f"model={model}",
            f"condition={condition}",
            f"prompt={prompt}",
            f"kit={kit}",
            "compose_file=docker-compose.yml",
        ]
        if kit:
            expected.append("compose_file=docker-compose.kit.yml")
        self.assertEqual(self.print_config(runner, config).splitlines(), expected)

    def test_base_compose_has_no_kit_mount(self) -> None:
        for runner in ("codex", "claude-code"):
            with self.subTest(runner=runner):
                config = self.compose_config(runner, False)
                self.assertNotIn("target: /kit-skills", config)
                self.assertNotIn(f"source: {REPO / 'data/skills'}", config)

    def test_launcher_fixtures_are_outside_repository_runs(self) -> None:
        self.assertNotEqual(self.runs, REPO / "runs")
        self.assertEqual(self.runs.parent, self.repo)
        self.assertEqual(
            self.repo.parent, Path("/tmp") / Path(self.fixture.name).name
        )

    def test_kit_override_adds_one_approved_read_only_mount(self) -> None:
        for runner in ("codex", "claude-code"):
            with self.subTest(runner=runner):
                config = self.compose_config(runner, True)
                self.assertEqual(config.count("target: /kit-skills"), 1)
                self.assertEqual(config.count(f"source: {REPO / 'data/skills'}"), 1)
                block = config.split("target: /kit-skills", 1)[1][:120]
                self.assertIn("read_only: true", block)

    def test_codex_and_claude_print_kit_semantics_without_launching(self) -> None:
        cases = (
            ("codex", "codex-test-xhigh-kit-semantics"),
            ("claude-code", "claude-code-opus-xhigh-test-kit-semantics"),
        )
        for runner, config in cases:
            with self.subTest(runner=runner):
                output = self.print_config(runner, config)
                self.assertIn("condition=kit-semantics", output)
                self.assertIn("prompt=kit-semantics.md", output)
                self.assertIn("kit=1", output)
                self.assertIn("compose_file=docker-compose.kit.yml", output)

    def test_codex_and_claude_match_all_four_conditions_in_order(self) -> None:
        runners = {
            "codex": "codex-test-xhigh-{condition}",
            "claude-code": "claude-code-opus-xhigh-test-{condition}",
        }
        conditions = {
            "kit-semantics": ("kit-semantics.md", 1),
            "kit": ("kit-bare.md", 1),
            "bare": ("bare.md", 0),
            "semantics": ("with-semantics.md", 0),
        }
        for runner, template in runners.items():
            for condition, (prompt, kit) in conditions.items():
                with self.subTest(runner=runner, condition=condition):
                    config = template.format(condition=condition)
                    output = self.print_config(runner, config)
                    self.assertIn(f"condition={condition}\n", output)
                    self.assertIn(f"prompt={prompt}\n", output)
                    self.assertIn(f"kit={kit}\n", output)
                    self.assertEqual(
                        output.count("compose_file=docker-compose.kit.yml"), kit
                    )

    def test_opencode_rejects_unsupported_kit_conditions(self) -> None:
        for condition in ("kit", "kit-semantics"):
            with self.subTest(condition=condition):
                result = self.print_config_result(
                    "opencode", f"opencode-kimi-k3-{condition}"
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("does not support Kit conditions", result.stderr)

    def test_supported_launchers_print_exact_config_without_launching(self) -> None:
        cases = (
            (
                "codex",
                "codex-test-xhigh-bare",
                "test",
                "bare",
                "bare.md",
            ),
            (
                "claude-code",
                "claude-code-opus-xhigh-test-bare",
                "opus",
                "bare",
                "bare.md",
            ),
            (
                "opencode",
                "opencode-kimi-k3-semantics",
                "openrouter/moonshotai/kimi-k3",
                "semantics",
                "with-semantics.md",
            ),
        )
        for runner, config, model, condition, prompt in cases:
            with self.subTest(runner=runner):
                self.assert_print_config(
                    runner,
                    config,
                    model=model,
                    condition=condition,
                    prompt=prompt,
                    kit=0,
                )

    def test_claude_rejects_config_without_runner_prefix(self) -> None:
        result = self.print_config_result(
            "claude-code", "other-opus-xhigh-bare"
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Not a claude-code config", result.stderr)

    def test_launchers_reject_unsafe_config_before_task_path_resolution(self) -> None:
        unsafe = (
            "archive/retry-bare",
            r"archive\retry-bare",
            ".",
            "..",
            "codex-test-xhigh-bare\nretry",
        )
        for runner in ("codex", "claude-code", "opencode"):
            for config in unsafe:
                with self.subTest(runner=runner, config=repr(config)):
                    result = self.print_config_result(
                        runner, config, prepare=False
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("safe path component", result.stderr)

    def test_launchers_reject_unsafe_problem_before_task_path_resolution(self) -> None:
        configs = {
            "codex": "codex-test-xhigh-bare",
            "claude-code": "claude-code-opus-xhigh-test-bare",
            "opencode": "opencode-kimi-k3-bare",
        }
        unsafe = ("archive/retry", r"archive\retry", ".", "..", "task\nretry")
        for runner, config in configs.items():
            for problem in unsafe:
                with self.subTest(runner=runner, problem=repr(problem)):
                    result = self.print_config_result(
                        runner, config, problem, prepare=False
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("safe path component", result.stderr)

    def test_task_validator_cli_accepts_valid_seed(self) -> None:
        config = "codex-validator-xhigh-semantics"
        task_dir = self.prepare_task(config)
        result = self.validate_task_result(config, task_dir)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_task_validator_cli_reports_contract_failure_concisely(self) -> None:
        config = "codex-validator-xhigh-bare"
        task_dir = self.prepare_task(config)
        (task_dir / "run-input.json").unlink()
        result = self.validate_task_result(config, task_dir)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("run-input.json", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_launchers_reject_live_and_broken_config_symlinks(self) -> None:
        outside_root = Path(self.outside.name)
        outside_target = outside_root / "config-target"
        outside_target.mkdir()
        targets = {
            "archive": self.runs / "archive",
            "outside": outside_target,
            "broken": outside_root / "missing-config-target",
        }
        for runner in ("codex", "claude-code", "opencode"):
            for label, target in targets.items():
                with self.subTest(runner=runner, target=label):
                    config = self.runner_config(runner, f"config-link-{label}")
                    self.register_config(config).symlink_to(
                        target, target_is_directory=True
                    )
                    result = self.print_config_result(
                        runner, config, prepare=False
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("real directory", result.stderr)

    def test_launchers_reject_live_and_broken_task_symlinks(self) -> None:
        outside_root = Path(self.outside.name)
        outside_target = outside_root / "task-target"
        outside_target.mkdir()
        targets = {
            "archive": self.runs / "archive",
            "outside": outside_target,
            "broken": outside_root / "missing-task-target",
        }
        for runner in ("codex", "claude-code", "opencode"):
            for label, target in targets.items():
                with self.subTest(runner=runner, target=label):
                    config = self.runner_config(runner, f"task-link-{label}")
                    config_dir = self.register_config(config)
                    config_dir.mkdir()
                    (config_dir / self.PROBLEM).symlink_to(
                        target, target_is_directory=True
                    )
                    result = self.print_config_result(
                        runner, config, prepare=False
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("real directory", result.stderr)

    def test_launchers_validate_answer_free_seed_before_printing(self) -> None:
        mutations = (
            (
                "missing-manifest",
                "bare",
                lambda task: (task / "run-input.json").unlink(),
            ),
            (
                "stale-manifest",
                "bare",
                lambda task: (task / "run-input.json").write_text("{}\n"),
            ),
            (
                "nested-canonical",
                "bare",
                self.add_nested_canonical,
            ),
            (
                "linked-prompt",
                "bare",
                self.link_prompt,
            ),
            (
                "missing-semantics",
                "semantics",
                lambda task: shutil.rmtree(task / "reference-semantics"),
            ),
            (
                "wrong-semantics",
                "semantics",
                lambda task: (task / "reference-semantics/semantics.k").write_text(
                    "module WRONG endmodule\n"
                ),
            ),
        )
        for runner in ("codex", "claude-code", "opencode"):
            for label, condition, mutate in mutations:
                with self.subTest(runner=runner, mutation=label):
                    config = self.runner_config(runner, label, condition)
                    task_dir = self.prepare_task(config)
                    mutate(task_dir)
                    result = self.print_config_result(
                        runner, config, prepare=False
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("task seed validation failed", result.stderr)

    @staticmethod
    def add_nested_canonical(task_dir: Path) -> None:
        nested = task_dir / "generated/evidence"
        nested.mkdir(parents=True)
        (nested / "canonical.py").write_text("def answer(): return 42\n")

    def link_prompt(self, task_dir: Path) -> None:
        prompt = task_dir / "prompt.py"
        prompt.unlink()
        prompt.symlink_to(
            self.repo / "data/questions/8-sum-product/prompt.py"
        )

    def test_launchers_require_exact_config_grammar(self) -> None:
        malformed = {
            "codex": (
                "codex-test-bare",
                "codex-test-xhigh-extra-bare",
            ),
            "claude-code": (
                "claude-code-notopus-xhigh-test-bare",
                "claude-code-fableish-xhigh-test-bare",
                "claude-code-test-opus-bare",
                "claude-code-opus-bare",
                "claude-code-opus-xhigh-bare",
            ),
            "opencode": (
                "opencode-bare",
                "opencode--bare",
            ),
        }
        for runner, configs in malformed.items():
            for config in configs:
                with self.subTest(runner=runner, config=config):
                    self.prepare_task(config)
                    result = self.print_config_result(
                        runner, config, prepare=False
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("config grammar", result.stderr)

    def test_launchers_reject_extra_positional_arguments(self) -> None:
        for runner in ("codex", "claude-code", "opencode"):
            with self.subTest(runner=runner):
                config = self.runner_config(runner, "extra-arg")
                result = self.print_config_result(
                    runner,
                    config,
                    extra_args=("unexpected",),
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("usage:", result.stderr)
