import contextlib
import importlib.util
import io
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO = Path(__file__).resolve().parents[1]
SMOKE_SCRIPT = REPO / "tests/smoke-containers.sh"


def load_populator():
    path = REPO / "tools/populate_runs.py"
    spec = importlib.util.spec_from_file_location("populate_runs_active_tests", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ManifestRegularFileTests(unittest.TestCase):
    @unittest.skipUnless(hasattr(os, "mkfifo"), "os.mkfifo is unavailable")
    def test_manifest_fifo_is_rejected_promptly_by_cli(self) -> None:
        module = load_populator()
        config = "codex-fifo-xhigh-bare"
        problem = "8-sum-product"
        with tempfile.TemporaryDirectory(prefix="manifest-fifo-") as tmp:
            runs_root = Path(tmp) / "runs"
            with contextlib.redirect_stdout(io.StringIO()):
                module.populate(config, repo=REPO, runs_root=runs_root)
            task = runs_root / config / problem
            manifest = task / "run-input.json"
            manifest.unlink()
            os.mkfifo(manifest)

            try:
                result = subprocess.run(
                    [
                        sys.executable,
                        str(REPO / "tools/populate_runs.py"),
                        "--validate-task",
                        config,
                        problem,
                        str(task),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=2,
                )
            except subprocess.TimeoutExpired:
                self.fail("manifest validation blocked while opening a FIFO")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("run-input.json", result.stderr)
            self.assertIn("regular file", result.stderr)
            self.assertNotIn("Traceback", result.stderr)


class ActiveRunTests(unittest.TestCase):
    CONFIG = "codex-audit-xhigh-bare"
    PROBLEM = "8-sum-product"

    def setUp(self) -> None:
        self.populator = load_populator()

    def populate(self, runs_root: Path) -> Path:
        with contextlib.redirect_stdout(io.StringIO()):
            self.populator.populate(self.CONFIG, repo=REPO, runs_root=runs_root)
        return runs_root / self.CONFIG

    def audit(self, runs_root: Path) -> list[str]:
        return self.populator.audit_active_runs(REPO, runs_root)

    def assert_audit_mentions(self, runs_root: Path, *fragments: str) -> None:
        rendered = "\n".join(self.audit(runs_root))
        for fragment in fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, rendered)

    def test_real_active_runs_satisfy_contract_without_archive_traversal(self) -> None:
        self.assertEqual(self.audit(REPO / "runs"), [])

    def assert_main_checkout_has_no_live_pipeline_processes_before_integration(
        self,
    ) -> None:
        from tools import migrate_six_stage_layout

        common_git = subprocess.run(
            ["git", "rev-parse", "--git-common-dir"],
            cwd=REPO,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        common_git_path = Path(common_git)
        if not common_git_path.is_absolute():
            common_git_path = REPO / common_git_path
        main_checkout = common_git_path.resolve().parent
        runs_root = main_checkout / "runs"
        if not runs_root.exists() and not runs_root.is_symlink():
            run_ids = []
        else:
            run_ids = sorted(
                path.name
                for path in runs_root.iterdir()
                if path.name != "archive"
                and path.is_dir()
                and not path.is_symlink()
            )

        blockers = migrate_six_stage_layout._active_process_blockers(run_ids)

        self.assertEqual(
            blockers,
            [],
            "active main-checkout pipeline processes block integration:\n"
            + json.dumps(blockers, indent=2, sort_keys=True),
        )

    def test_main_checkout_has_no_live_pipeline_processes_before_integration(
        self,
    ) -> None:
        self.assert_main_checkout_has_no_live_pipeline_processes_before_integration()

    def test_integration_guard_treats_missing_main_runs_as_empty(self) -> None:
        with tempfile.TemporaryDirectory(prefix="clean-clone-") as tmp:
            common_git = Path(tmp) / ".git"
            completed = subprocess.CompletedProcess(
                args=["git", "rev-parse", "--git-common-dir"],
                returncode=0,
                stdout=str(common_git) + "\n",
                stderr="",
            )
            with mock.patch.object(subprocess, "run", return_value=completed):
                try:
                    self.assert_main_checkout_has_no_live_pipeline_processes_before_integration()
                except FileNotFoundError as error:
                    self.fail(
                        "missing main-checkout runs must be treated as empty: "
                        f"{error}"
                    )

    def test_integration_guard_still_reports_existing_run_blockers(self) -> None:
        from tools import migrate_six_stage_layout

        with tempfile.TemporaryDirectory(prefix="active-main-run-") as tmp:
            root = Path(tmp)
            common_git = root / ".git"
            run_id = "active-six-stage-run"
            (root / "runs" / run_id).mkdir(parents=True)
            completed = subprocess.CompletedProcess(
                args=["git", "rev-parse", "--git-common-dir"],
                returncode=0,
                stdout=str(common_git) + "\n",
                stderr="",
            )
            active = (
                (
                    12345,
                    ("python3", "tools/run_pipeline.py", "run", run_id),
                ),
            )
            with (
                mock.patch.object(subprocess, "run", return_value=completed),
                mock.patch.object(
                    migrate_six_stage_layout,
                    "_candidate_processes",
                    return_value=active,
                ),
                self.assertRaisesRegex(
                    AssertionError,
                    r"active main-checkout pipeline processes block "
                    r"integration:[\s\S]*active-six-stage-run",
                ),
            ):
                self.assert_main_checkout_has_no_live_pipeline_processes_before_integration()

    def test_stage_oriented_pipeline_run_is_not_a_legacy_active_config(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(prefix="stage-oriented-run-") as tmp:
            runs_root = Path(tmp) / "runs"
            run = runs_root / "pipeline-run"
            tasks = run / "tasks"
            tasks.mkdir(parents=True)
            (run / "run.json").write_text("{}\n")
            (run / "task-list.txt").write_text("8-sum-product\n")
            if hasattr(os, "mkfifo"):
                os.mkfifo(tasks / "must-not-be-traversed")

            self.assertEqual(self.audit(runs_root), [])

    def test_stage_oriented_pipeline_run_with_usage_summary_is_not_legacy(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(prefix="stage-oriented-usage-run-") as tmp:
            runs_root = Path(tmp) / "runs"
            run = runs_root / "pipeline-run"
            tasks = run / "tasks"
            tasks.mkdir(parents=True)
            (run / "run.json").write_text("{}\n")
            (run / "task-list.txt").write_text("8-sum-product\n")
            (run / "usage-summary.json").write_text("{}\n")
            if hasattr(os, "mkfifo"):
                os.mkfifo(tasks / "must-not-be-traversed")

            self.assertEqual(self.audit(runs_root), [])

    def test_runs_root_must_be_a_real_directory(self) -> None:
        with tempfile.TemporaryDirectory(prefix="active-root-") as tmp:
            root = Path(tmp)
            target = root / "target"
            target.mkdir()
            linked = root / "linked-runs"
            linked.symlink_to(target, target_is_directory=True)
            self.assert_audit_mentions(linked, "runs root", "real directory")

            regular = root / "regular-runs"
            regular.write_text("not a directory\n")
            self.assert_audit_mentions(regular, "runs root", "real directory")

            self.assert_audit_mentions(
                root / "missing-runs", "runs root", "real directory"
            )

    def test_selection_must_contain_24_distinct_problem_ids(self) -> None:
        with tempfile.TemporaryDirectory(prefix="active-selection-") as tmp:
            repo = Path(tmp) / "repo"
            selection = repo / "data/selection.json"
            selection.parent.mkdir(parents=True)
            selection.write_text(
                json.dumps({"selected": [{"id": "duplicate"}] * 24}) + "\n"
            )
            runs_root = repo / "runs"
            runs_root.mkdir()
            rendered = "\n".join(
                self.populator.audit_active_runs(repo, runs_root)
            )
            self.assertIn("exactly 24 distinct problem IDs", rendered)

    def test_selection_rejects_every_unsafe_problem_id_with_no_active_configs(
        self,
    ) -> None:
        unsafe_ids = (
            "",
            ".hidden",
            ".",
            "..",
            "/absolute",
            "nested/task",
            r"nested\task",
            "control\ncharacter",
            "delete\x7fcharacter",
        )
        for unsafe in unsafe_ids:
            with self.subTest(problem_id=repr(unsafe)), tempfile.TemporaryDirectory(
                prefix="active-unsafe-selection-"
            ) as tmp:
                repo = Path(tmp) / "repo"
                selection = repo / "data/selection.json"
                selection.parent.mkdir(parents=True)
                selected = [
                    {"id": f"safe-{index}"} for index in range(23)
                ] + [{"id": unsafe}]
                selection.write_text(json.dumps({"selected": selected}) + "\n")
                runs_root = repo / "runs"
                (runs_root / "archive").mkdir(parents=True)

                rendered = "\n".join(
                    self.populator.audit_active_runs(repo, runs_root)
                )

                self.assertIn("nonhidden safe path component", rendered)

    def test_population_rejects_all_unsafe_ids_before_creating_any_task(self) -> None:
        with tempfile.TemporaryDirectory(prefix="population-unsafe-selection-") as tmp:
            root = Path(tmp)
            repo = root / "repo"
            runs_root = root / "runs"
            config = "codex-selection-xhigh-bare"
            selected = ("safe-problem", "nested/problem")
            selection = repo / "data/selection.json"
            selection.parent.mkdir(parents=True)
            selection.write_text(
                json.dumps({"selected": [{"id": value} for value in selected]})
                + "\n"
            )
            for problem_id in selected:
                prompt = repo / "data/questions" / problem_id / "prompt.py"
                prompt.parent.mkdir(parents=True)
                prompt.write_text("def example():\n    pass\n")
            translator = repo / "tools/py2mpy.py"
            translator.parent.mkdir(parents=True)
            translator.write_text("# translator\n")
            instruction = repo / "prompts/bare.md"
            instruction.parent.mkdir(parents=True)
            instruction.write_text("implement\n")

            error = None
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    self.populator.populate(config, repo=repo, runs_root=runs_root)
            except Exception as caught:  # Assert the public failure type below.
                error = caught

            self.assertIsInstance(error, ValueError)
            self.assertIn("problem ID", str(error))
            self.assertFalse(runs_root.exists(), "population left a partial runs root")
            self.assertFalse((root / "escaped").exists())

    def test_archive_sentinel_is_skipped_without_traversal(self) -> None:
        with tempfile.TemporaryDirectory(prefix="active-archive-") as tmp:
            runs_root = Path(tmp) / "runs"
            sentinel = runs_root / "archive/sentinel/canonical.py"
            sentinel.parent.mkdir(parents=True)
            sentinel.write_text("must not be inspected\n")
            self.assertEqual(self.audit(runs_root), [])

    def test_archive_must_be_a_real_directory(self) -> None:
        with tempfile.TemporaryDirectory(prefix="active-archive-node-") as tmp:
            root = Path(tmp)
            runs_root = root / "runs"
            runs_root.mkdir()
            target = root / "archive-target"
            target.mkdir()
            (runs_root / "archive").symlink_to(target, target_is_directory=True)
            self.assert_audit_mentions(
                runs_root, "archive", "real directory"
            )

    def test_config_live_and_broken_symlinks_are_rejected(self) -> None:
        for label, live in (("live", True), ("broken", False)):
            with self.subTest(label=label), tempfile.TemporaryDirectory(
                prefix=f"active-config-{label}-"
            ) as tmp:
                root = Path(tmp)
                runs_root = root / "runs"
                runs_root.mkdir()
                target = root / "config-target"
                if live:
                    target.mkdir()
                (runs_root / self.CONFIG).symlink_to(
                    target, target_is_directory=True
                )
                self.assert_audit_mentions(
                    runs_root, self.CONFIG, "real directory"
                )

    def test_hidden_config_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="active-hidden-config-") as tmp:
            runs_root = Path(tmp) / "runs"
            (runs_root / ".hidden-bare").mkdir(parents=True)
            self.assert_audit_mentions(runs_root, ".hidden-bare", "hidden")

    def test_config_regular_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="active-file-config-") as tmp:
            runs_root = Path(tmp) / "runs"
            runs_root.mkdir()
            (runs_root / self.CONFIG).write_text("not a directory\n")
            self.assert_audit_mentions(
                runs_root, self.CONFIG, "real directory"
            )

    @unittest.skipUnless(hasattr(os, "mkfifo"), "os.mkfifo is unavailable")
    def test_config_fifo_is_rejected_without_reading(self) -> None:
        with tempfile.TemporaryDirectory(prefix="active-fifo-config-") as tmp:
            runs_root = Path(tmp) / "runs"
            runs_root.mkdir()
            os.mkfifo(runs_root / self.CONFIG)
            self.assert_audit_mentions(
                runs_root, self.CONFIG, "real directory"
            )

    @unittest.skipUnless(hasattr(socket, "AF_UNIX"), "Unix sockets unavailable")
    def test_config_socket_is_rejected_without_opening(self) -> None:
        with tempfile.TemporaryDirectory(prefix="active-socket-config-") as tmp:
            runs_root = Path(tmp) / "runs"
            runs_root.mkdir()
            with socket.socket(socket.AF_UNIX) as node:
                node.bind(str(runs_root / self.CONFIG))
                self.assert_audit_mentions(
                    runs_root, self.CONFIG, "real directory"
                )

    def test_task_live_and_broken_symlinks_are_rejected(self) -> None:
        for label, live in (("live", True), ("broken", False)):
            with self.subTest(label=label), tempfile.TemporaryDirectory(
                prefix=f"active-task-{label}-"
            ) as tmp:
                root = Path(tmp)
                runs_root = root / "runs"
                config_dir = self.populate(runs_root)
                task = config_dir / self.PROBLEM
                shutil.rmtree(task)
                target = root / "task-target"
                if live:
                    target.mkdir()
                task.symlink_to(target, target_is_directory=True)
                self.assert_audit_mentions(
                    runs_root, self.CONFIG, self.PROBLEM, "real directory"
                )

    def test_hidden_task_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="active-hidden-task-") as tmp:
            runs_root = Path(tmp) / "runs"
            config_dir = self.populate(runs_root)
            (config_dir / ".hidden").mkdir()
            self.assert_audit_mentions(runs_root, ".hidden", "hidden")

    def test_task_regular_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="active-file-task-") as tmp:
            runs_root = Path(tmp) / "runs"
            config_dir = self.populate(runs_root)
            task = config_dir / self.PROBLEM
            shutil.rmtree(task)
            task.write_text("not a directory\n")
            self.assert_audit_mentions(
                runs_root, self.CONFIG, self.PROBLEM, "real directory"
            )

    @unittest.skipUnless(hasattr(os, "mkfifo"), "os.mkfifo is unavailable")
    def test_task_fifo_is_rejected_without_reading(self) -> None:
        with tempfile.TemporaryDirectory(prefix="active-fifo-task-") as tmp:
            runs_root = Path(tmp) / "runs"
            config_dir = self.populate(runs_root)
            task = config_dir / self.PROBLEM
            shutil.rmtree(task)
            os.mkfifo(task)
            self.assert_audit_mentions(
                runs_root, self.CONFIG, self.PROBLEM, "real directory"
            )

    @unittest.skipUnless(hasattr(socket, "AF_UNIX"), "Unix sockets unavailable")
    def test_task_socket_is_rejected_without_opening(self) -> None:
        with tempfile.TemporaryDirectory(prefix="active-socket-task-") as tmp:
            runs_root = Path(tmp) / "runs"
            config_dir = self.populate(runs_root)
            task = config_dir / self.PROBLEM
            shutil.rmtree(task)
            with socket.socket(socket.AF_UNIX) as node:
                node.bind(str(task))
                self.assert_audit_mentions(
                    runs_root, self.CONFIG, self.PROBLEM, "real directory"
                )

    def test_task_names_must_equal_the_selected_set(self) -> None:
        with tempfile.TemporaryDirectory(prefix="active-task-set-") as tmp:
            runs_root = Path(tmp) / "runs"
            config_dir = self.populate(runs_root)
            shutil.rmtree(config_dir / self.PROBLEM)
            self.assert_audit_mentions(
                runs_root, self.CONFIG, "task set", self.PROBLEM, "missing"
            )

    def test_selected_task_seed_is_validated_with_context(self) -> None:
        with tempfile.TemporaryDirectory(prefix="active-seed-") as tmp:
            runs_root = Path(tmp) / "runs"
            config_dir = self.populate(runs_root)
            (config_dir / self.PROBLEM / "prompt.py").write_text("stale\n")
            self.assert_audit_mentions(
                runs_root,
                self.CONFIG,
                self.PROBLEM,
                "missing or stale seed file",
            )


class ContainerSmokeScriptTests(unittest.TestCase):
    def source(self) -> str:
        self.assertTrue(SMOKE_SCRIPT.is_file(), "missing container smoke script")
        return SMOKE_SCRIPT.read_text()

    def check_block(self, name: str) -> str:
        match = re.search(
            rf"read -r -d '' {name} <<'CHECKS' \|\| true\n(.*?)\nCHECKS",
            self.source(),
            re.DOTALL,
        )
        self.assertIsNotNone(match, f"missing {name} check block")
        return match.group(1)

    def test_in_container_check_preamble_stops_after_first_failure(self) -> None:
        common = self.check_block("COMMON_CHECKS")
        preamble = common.splitlines()[0]
        self.assertEqual(preamble, "set -euo pipefail")
        with tempfile.TemporaryDirectory(prefix="smoke-fail-fast-") as tmp:
            continued = Path(tmp) / "continued"
            checks = f'{preamble}\nfalse\nprintf reached > "$1"\n'
            result = subprocess.run(
                ["/bin/bash", "-c", checks, "smoke", str(continued)],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(continued.exists(), "checks continued after failure")

    def test_smoke_uses_guarded_temporary_production_populated_seeds(self) -> None:
        source = self.source()
        self.assertIn("set -euo pipefail", source)
        self.assertIn(
            "mktemp -d /tmp/humaneval-container-smoke.XXXXXXXX", source
        )
        self.assertIn("trap cleanup EXIT", source)
        self.assertIn("trap 'exit 130' INT", source)
        self.assertIn("trap 'exit 143' TERM", source)
        self.assertIn("populate(", source)
        self.assertIn("runs_root=", source)
        self.assertIn("codex-smoke-xhigh-bare", source)
        self.assertIn("codex-smoke-xhigh-kit", source)
        self.assertNotIn("$REPO/runs", source)

    def test_smoke_has_one_raw_offline_docker_run_helper(self) -> None:
        source = self.source()
        self.assertEqual(source.count("docker run"), 1)
        for fragment in (
            "--rm",
            '--name "$container_name"',
            "--pull=never",
            "--network none",
            "--read-only",
            "--entrypoint /bin/bash",
            'type=bind,source=$task_dir,target=/work,readonly',
            '"$image" -c "$checks" smoke "$expected_cli"',
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, source)
        for forbidden in (
            "docker compose",
            "docker image",
            "docker pull",
            "docker build",
            "--version",
            "--user",
            "--workdir",
            "/var/run/docker.sock",
            "/auth",
            "/secrets",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source)

    def test_smoke_uses_unique_task_local_container_names(self) -> None:
        source = self.source()
        self.assertIn('SMOKE_ID="${SMOKE_ROOT##*.}"', source)
        self.assertIn(
            'container_name="humaneval-container-smoke-${SMOKE_ID}-',
            source,
        )
        self.assertNotIn("docker stop", source)
        self.assertNotIn("docker rm", source)

    def test_smoke_declares_three_base_and_two_kit_image_checks(self) -> None:
        source = self.source()
        for image, cli in (
            ("humaneval-codex-runner:latest", "codex"),
            ("humaneval-claude-runner:latest", "claude"),
            ("humaneval-opencode-runner:latest", "opencode"),
        ):
            with self.subTest(image=image):
                self.assertIn(image, source)
                self.assertIn(cli, source)
        self.assertIn(
            'type=bind,source=$REPO/data/skills,target=/kit-skills,readonly',
            source,
        )
        self.assertEqual(source.count("run_container base"), 3)
        self.assertEqual(source.count("run_container kit"), 2)

    def test_smoke_checks_only_declared_defaults_seed_and_executable_presence(
        self,
    ) -> None:
        source = self.source()
        for fragment in (
            'test "$PWD" = /work',
            'test "$(id -u)" = 1000',
            'test "$(id -g)" = 1000',
            'test "$(id -un)" = agent',
            'test "$HOME" = /home/agent',
            "test -r prompt.py",
            "test -r py2mpy.py",
            "test -r run-input.json",
            "test ! -e canonical.py",
            "test ! -L canonical.py",
            "command -v python3",
            "command -v kompile",
            "command -v krun",
            "command -v kprove",
            'command -v "$1"',
            "test ! -e /kit-skills",
            "test ! -L /kit-skills",
            "grep -Fxq 'name: using-kit' /kit-skills/using-kit/SKILL.md",
            "grep -Fxq '# Proof-extension soundness contract'",
            '/kit-skills/shared/proof-extension-soundness.md',
            '$2 == "/kit-skills"',
            "ro(,|$)",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, source)

    def test_readme_scopes_base_kit_assertion_to_kit_skills_path(self) -> None:
        readme = (REPO / "README.md").read_text()
        self.assertIn("absence of a `/kit-skills` path", readme)
        self.assertNotIn("absence of baked-in Kit content", readme)


if __name__ == "__main__":
    unittest.main()
