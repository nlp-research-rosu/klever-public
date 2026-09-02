import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ("codex", "claude-code", "opencode")


class MatrixSchedulerTests(unittest.TestCase):
    def test_preserves_task_arguments_and_returns_nonzero_after_child_failure(self):
        config = "config with spaces [*]?"
        passing_problem = "passes * [one]?"
        failing_problem = "fails ? [two]*"

        for runner in RUNNERS:
            with self.subTest(runner=runner), tempfile.TemporaryDirectory() as tmp:
                temp_root = Path(tmp)
                runner_dir = temp_root / "docker" / runner
                runner_dir.mkdir(parents=True)
                matrix_script = runner_dir / "run_matrix.sh"
                shutil.copy2(
                    REPO_ROOT / "docker" / runner / "run_matrix.sh",
                    matrix_script,
                )

                capture_path = temp_root / "captured-arguments.tsv"
                fake_run_task = runner_dir / "run_task.sh"
                fake_run_task.write_text(
                    "#!/usr/bin/env bash\n"
                    "printf '%s\\t%s\\t%s\\n' \"$#\" \"${1-}\" \"${2-}\" "
                    ">> \"$SCHED_CAPTURE\"\n"
                    "if [[ \"$#\" -eq 2 && \"$1\" == \"$FAIL_CONFIG\" "
                    "&& \"$2\" == \"$FAIL_PROBLEM\" ]]; then\n"
                    "  exit 23\n"
                    "fi\n"
                    "exit 0\n"
                )
                fake_run_task.chmod(0o755)

                config_dir = temp_root / "runs" / config
                (config_dir / passing_problem).mkdir(parents=True)
                (config_dir / failing_problem).mkdir()

                env = os.environ.copy()
                env.update(
                    {
                        "SCHED_CAPTURE": str(capture_path),
                        "FAIL_CONFIG": config,
                        "FAIL_PROBLEM": failing_problem,
                    }
                )
                result = subprocess.run(
                    [
                        "bash",
                        str(matrix_script),
                        "--jobs",
                        "1",
                        "--config",
                        config,
                    ],
                    cwd=temp_root,
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                self.assertNotEqual(result.returncode, 0, result.stderr)
                self.assertIn("FAILED:", result.stderr)
                self.assertIn("=== SUMMARY (from metrics.json) ===", result.stderr)

                captured = [
                    tuple(line.split("\t"))
                    for line in capture_path.read_text().splitlines()
                ]
                self.assertCountEqual(
                    captured,
                    [
                        ("2", config, passing_problem),
                        ("2", config, failing_problem),
                    ],
                )


if __name__ == "__main__":
    unittest.main()
