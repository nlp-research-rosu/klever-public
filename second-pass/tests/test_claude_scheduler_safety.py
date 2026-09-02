import json
import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
BABYSIT = REPO / "docker/claude-code/babysit.sh"
THROTTLE = REPO / "tools/opus_throttle.sh"
OPUS_CONFIGS = (
    "claude-code-opus-xhigh-4-8-bare",
    "claude-code-opus-xhigh-4-8-semantics",
    "claude-code-opus-xhigh-4-8-kit",
    "claude-code-opus-xhigh-4-8-kit-semantics",
)


class BabysitterSafetyTests(unittest.TestCase):
    def test_supervisor_monitors_its_exact_live_child_and_returns_child_status(
        self,
    ) -> None:
        source = BABYSIT.read_text()
        self.assertIn(
            '[[ "${BASH_SOURCE[0]}" == "$0" ]]',
            source,
            "the test must be able to source functions without starting a scheduler",
        )
        self.assertIn('kill -0 "$matrix_pid"', source)
        self.assertIn('wait "$matrix_pid"', source)
        self.assertNotIn(
            'pgrep -f "claude-code/run_task.sh|run_matrix.sh --jobs $JOBS"',
            source,
        )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fake_matrix = root / "fake-matrix.sh"
            pid_file = root / "matrix.pid"
            marker = root / "monitored-live-child"
            fake_matrix.write_text(
                textwrap.dedent(
                    """\
                    #!/usr/bin/env bash
                    printf '%s\n' "$$" > "$WATCH_PID_FILE"
                    sleep 0.25
                    exit 37
                    """
                )
            )
            fake_matrix.chmod(0o755)
            command = textwrap.dedent(
                """\
                source "$1"
                limit_failure_present() {
                  local watched
                  watched="$(cat "$WATCH_PID_FILE")"
                  if kill -0 "$watched" 2>/dev/null; then
                    : > "$MONITOR_MARKER"
                  fi
                  return 1
                }
                BABYSIT_POLL_SECONDS=0.01
                supervise_matrix "$2"
                """
            )
            environment = os.environ.copy()
            environment.update(
                WATCH_PID_FILE=str(pid_file),
                MONITOR_MARKER=str(marker),
            )
            result = subprocess.run(
                ["bash", "-c", command, "scheduler-test", str(BABYSIT), str(fake_matrix)],
                cwd=REPO,
                env=environment,
                capture_output=True,
                text=True,
                timeout=5,
            )

            self.assertEqual(result.returncode, 37, result.stderr)
            self.assertTrue(marker.is_file(), "child was not monitored while live")

    def test_main_propagates_an_unintentional_matrix_failure(self) -> None:
        source = BABYSIT.read_text()
        self.assertIn("main()", source)
        self.assertIn("refresh_credentials()", source)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = root / "runs" / OPUS_CONFIGS[0]
            (config / "0-sample").mkdir(parents=True)
            (root / "_setup").mkdir()
            calls = root / "supervise-calls"
            command = textwrap.dedent(
                """\
                source "$1"
                REPO="$2"
                HERE="$2/fake-harness"
                CONFIG_GLOB='claude-code-opus-*'
                reset_limit_failures() { :; }
                remaining_tasks() { echo 1; }
                usage_decision() { echo GO; }
                refresh_credentials() { :; }
                supervise_matrix() {
                  printf 'called\n' >> "$SUPERVISE_CALLS"
                  if [[ "$(wc -l < "$SUPERVISE_CALLS")" -eq 1 ]]; then
                    return "$LIMIT_STOP_RC"
                  fi
                  return 37
                }
                main
                """
            )
            environment = os.environ.copy()
            environment["SUPERVISE_CALLS"] = str(calls)
            result = subprocess.run(
                ["bash", "-c", command, "scheduler-test", str(BABYSIT), str(root)],
                cwd=REPO,
                env=environment,
                capture_output=True,
                text=True,
                timeout=5,
            )

            self.assertEqual(result.returncode, 37, result.stderr)
            self.assertEqual(calls.read_text().splitlines(), ["called", "called"])

    def test_session_limit_stops_only_supervised_xargs_and_returns_retry_status(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fake_matrix = root / "fake-matrix.sh"
            matrix_fifo = root / "matrix-input"
            unrelated_fifo = root / "unrelated-input"
            unrelated_survived = root / "unrelated-survived"
            os.mkfifo(matrix_fifo)
            os.mkfifo(unrelated_fifo)
            fake_matrix.write_text(
                textwrap.dedent(
                    """\
                    #!/usr/bin/env bash
                    exec 9<> "$MATRIX_FIFO"
                    xargs -0 <&9
                    rc=$?
                    exit "$rc"
                    """
                )
            )
            fake_matrix.chmod(0o755)
            command = textwrap.dedent(
                """\
                source "$1"
                BABYSIT_POLL_SECONDS=0.01
                limit_failure_present() { return 0; }

                exec 8<> "$UNRELATED_FIFO"
                xargs -0 <&8 &
                unrelated_pid=$!

                supervise_rc=0
                supervise_matrix "$2" || supervise_rc=$?
                if kill -0 "$unrelated_pid" 2>/dev/null; then
                  : > "$UNRELATED_SURVIVED"
                fi
                kill "$unrelated_pid" 2>/dev/null || true
                wait "$unrelated_pid" 2>/dev/null || true
                exit "$supervise_rc"
                """
            )
            environment = os.environ.copy()
            environment.update(
                MATRIX_FIFO=str(matrix_fifo),
                UNRELATED_FIFO=str(unrelated_fifo),
                UNRELATED_SURVIVED=str(unrelated_survived),
            )
            result = subprocess.run(
                ["bash", "-c", command, "scheduler-test", str(BABYSIT), str(fake_matrix)],
                cwd=REPO,
                env=environment,
                capture_output=True,
                text=True,
                timeout=5,
            )

            self.assertEqual(result.returncode, 75, result.stderr)
            self.assertTrue(
                unrelated_survived.is_file(),
                "supervisor stopped an unrelated xargs process",
            )


class OpusThrottleSafetyTests(unittest.TestCase):
    @staticmethod
    def _write_selection(root: Path) -> list[str]:
        problem_ids = [f"{number}-selected" for number in range(24)]
        data = root / "data"
        data.mkdir(parents=True)
        (data / "selection.json").write_text(
            json.dumps({"selected": [{"id": problem} for problem in problem_ids]})
            + "\n"
        )
        (root / "runs").mkdir()
        return problem_ids

    def _validate(self, root: Path) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["HUMANEVAL_BENCHMARK_ROOT"] = str(root)
        return subprocess.run(
            ["bash", str(THROTTLE), "--validate-queue"],
            cwd=REPO,
            env=environment,
            capture_output=True,
            text=True,
            timeout=5,
        )

    def test_queue_validation_requires_all_four_configs_and_exact_selected_tasks(
        self,
    ) -> None:
        source = THROTTLE.read_text()
        self.assertIn("--validate-queue", source)
        self.assertIn("HUMANEVAL_BENCHMARK_ROOT", source)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            problem_ids = self._write_selection(root)

            empty = self._validate(root)
            self.assertNotEqual(empty.returncode, 0)
            self.assertIn(OPUS_CONFIGS[0], empty.stderr)

            for config_name in OPUS_CONFIGS[:3]:
                config = root / "runs" / config_name
                for problem in problem_ids:
                    (config / problem).mkdir(parents=True, exist_ok=True)
            three_conditions = self._validate(root)
            self.assertNotEqual(three_conditions.returncode, 0)
            self.assertIn(OPUS_CONFIGS[3], three_conditions.stderr)

            final_config = root / "runs" / OPUS_CONFIGS[3]
            for problem in problem_ids[:-1]:
                (final_config / problem).mkdir(parents=True, exist_ok=True)
            (final_config / "not-a-selected-task").mkdir(parents=True)
            missing_selected = self._validate(root)
            self.assertNotEqual(missing_selected.returncode, 0)
            self.assertIn(problem_ids[-1], missing_selected.stderr)

            (final_config / problem_ids[-1]).mkdir()
            complete = self._validate(root)
            self.assertEqual(complete.returncode, 0, complete.stderr)
            self.assertIn("validated 96 expected task folders", complete.stdout)


if __name__ == "__main__":
    unittest.main()
