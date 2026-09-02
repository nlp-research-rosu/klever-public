import json
import os
import subprocess
import tempfile
import unittest
import uuid
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
ENTRYPOINT = REPO / "docker/codex/entrypoint.sh"


class LeanLauncherTests(unittest.TestCase):
    def test_public_stage5_launcher_and_failing_compatibility_shim(
        self,
    ) -> None:
        launcher = (
            REPO / "docker/codex/resume_lean_task.sh"
        )
        self.assertTrue(launcher.is_file())
        source = launcher.read_text()
        self.assertIn("tools/stage5_runner.py", source)
        self.assertNotIn("tools/stage4_runner.py", source)

        replaced = subprocess.run(
            ["bash", str(REPO / "docker/codex/resume_klean_task.sh")],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(replaced.returncode, 2)
        self.assertEqual(replaced.stdout, "")
        self.assertEqual(
            replaced.stderr,
            "resume_klean_task.sh was replaced by "
            "resume_lean_task.sh\n",
        )


class CodexEntrypointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.workspace = self.root / "workspace"
        self.workspace.mkdir()
        self.invocation = self.root / "invocation"
        self.invocation.mkdir()
        self.home = self.root / "codex-home"
        self.home.mkdir(mode=0o700)
        self.auth = self.root / "approved-auth.json"
        self.auth.write_text('{"tokens": "approved"}\n')
        self.kit = self.root / "approved-kit"
        (self.kit / "using-kit").mkdir(parents=True)
        (self.kit / "using-kit/SKILL.md").write_text("# approved Kit\n")
        self.prompt = self.root / "prompt.md"
        self.prompt.write_text("Do the benchmark task.\n")
        self.supervisor = self.root / "supervisor"
        self.supervisor.mkdir(mode=0o700)
        self.cgroup = self.root / "cgroup"
        self.cgroup.mkdir()
        (self.cgroup / "memory.peak").write_text("12345\n")
        (self.cgroup / "memory.events").write_text("oom 0\noom_kill 0\n")
        self.argv_log = self.root / "argv.json"
        self.stdin_log = self.root / "stdin.txt"
        self.bwrap_log = self.root / "bwrap.json"
        self.session_id = str(uuid.uuid4())
        self.fake_bwrap = self.bin / "bwrap"
        self.fake_bwrap.write_text(
            """#!/usr/bin/env python3
import json
import os
from pathlib import Path
import sys

Path(os.environ["FAKE_BWRAP_LOG"]).write_text(json.dumps(sys.argv[1:]))
raise SystemExit(int(os.environ.get("FAKE_BWRAP_RC", "0")))
"""
        )
        self.fake_bwrap.chmod(0o755)
        self.fake_codex = self.bin / "codex"
        self.fake_codex.write_text(
            """#!/usr/bin/env python3
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

args = sys.argv[1:]
Path(os.environ["FAKE_ARGV_LOG"]).write_text(json.dumps(args))
Path(os.environ["FAKE_STDIN_LOG"]).write_text(sys.stdin.read())
last = Path(args[args.index("--output-last-message") + 1])
last.write_text("fake final message\\n")
session = os.environ["FAKE_SESSION_ID"]
trace = Path(os.environ["CODEX_HOME"]) / "sessions/2026/07/23/rollout.jsonl"
trace.parent.mkdir(parents=True, exist_ok=True)
trace.write_text(json.dumps(
    {"type": "session_meta", "payload": {"id": session}}
) + "\\n")
mode = os.environ.get("FAKE_CODEX_MODE", "success")
if mode == "timeout":
    child = subprocess.Popen([
        sys.executable, "-c",
        "import signal,time; signal.signal(signal.SIGTERM, signal.SIG_IGN); time.sleep(60)"
    ])
    Path(os.environ["FAKE_CHILD_PID"]).write_text(str(child.pid))
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    time.sleep(60)
print("fake codex stdout")
raise SystemExit(int(os.environ.get("FAKE_CODEX_RC", "0")))
"""
        )
        self.fake_codex.chmod(0o755)

    def environment(self, invocation: Path, *, kind: str, session: str = "") -> dict[str, str]:
        environment = os.environ.copy()
        environment.update(
            {
                "PATH": f"{self.bin}:{environment['PATH']}",
                "WORKSPACE": str(self.workspace),
                "INVOCATION_OUTPUT": str(invocation),
                "CODEX_HOME": str(self.home),
                "CODEX_AUTH_FILE": str(self.auth),
                "KIT_SKILLS_DIR": str(self.kit),
                "PROMPT_FILE": str(self.prompt),
                "SUPERVISOR_PARENT": str(self.supervisor),
                "CGROUP_ROOT": str(self.cgroup),
                "INVOCATION_KIND": kind,
                "SESSION_ID": session,
                "MODEL": "fake-model",
                "EFFORT": "xhigh",
                "KIT": "1",
                "TIMEOUT_S": "5",
                "TIMEOUT_GRACE_S": "1",
                "FAKE_ARGV_LOG": str(self.argv_log),
                "FAKE_STDIN_LOG": str(self.stdin_log),
                "FAKE_BWRAP_LOG": str(self.bwrap_log),
                "FAKE_SESSION_ID": self.session_id,
                "FAKE_CHILD_PID": str(self.root / "child.pid"),
                "CODEX_BWRAP": str(self.fake_bwrap),
                "FROZEN_TOOLCHAIN_CHECK": "/bin/true",
            }
        )
        return environment

    def run_entrypoint(
        self,
        invocation: Path,
        *,
        kind: str = "initial",
        session: str = "",
        extra: dict[str, str] | None = None,
        timeout: int = 15,
    ) -> subprocess.CompletedProcess[str]:
        environment = self.environment(invocation, kind=kind, session=session)
        if extra:
            environment.update(extra)
        return subprocess.run(
            ["bash", str(ENTRYPOINT)],
            cwd=self.root,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )

    def test_initial_then_exact_session_resume_use_persistent_home(self) -> None:
        initial = self.run_entrypoint(self.invocation)
        self.assertEqual(initial.returncode, 0, initial.stderr)
        initial_args = json.loads(self.argv_log.read_text())
        self.assertIn("exec", initial_args)
        self.assertNotIn("resume", initial_args)
        self.assertIn("--sandbox", initial_args)
        self.assertIn("workspace-write", initial_args)
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", initial_args)
        self.assertNotIn("--add-dir", initial_args)
        self.assertEqual(self.stdin_log.read_text(), self.prompt.read_text())
        self.assertEqual(
            (self.home / "auth.json").read_bytes(), self.auth.read_bytes()
        )
        self.assertEqual(
            (self.home / "skills/using-kit/SKILL.md").read_bytes(),
            (self.kit / "using-kit/SKILL.md").read_bytes(),
        )
        self.assertTrue((self.invocation / "codex-output.log").is_file())
        self.assertTrue((self.invocation / "codex-last.txt").is_file())
        self.assertTrue((self.invocation / "codex-trace").is_dir())
        metrics = json.loads((self.invocation / "metrics.json").read_text())
        self.assertFalse(metrics["timeout_marker"])
        self.assertFalse(metrics["oom_killed"])
        self.assertEqual(metrics["mem_peak_bytes"], 12345)
        self.assertEqual(
            sorted(path.name for path in self.invocation.iterdir()),
            [
                "codex-last.txt",
                "codex-output.log",
                "codex-trace",
                "metrics.json",
                "prompt.txt",
            ],
        )

        system_skills = self.home / "skills/.system"
        system_skills.mkdir()
        system_skills.joinpath(".codex-system-skills.marker").write_text(
            "managed by Codex\n"
        )
        resumed_output = self.root / "resumed-invocation"
        resumed_output.mkdir()
        resumed = self.run_entrypoint(
            resumed_output, kind="timeout-resume", session=self.session_id
        )
        self.assertEqual(resumed.returncode, 0, resumed.stderr)
        resumed_args = json.loads(self.argv_log.read_text())
        resume_index = resumed_args.index("resume")
        self.assertEqual(resumed_args[resume_index + 1], self.session_id)
        self.assertEqual(resumed_args[-1], "-")
        self.assertEqual(
            (self.home / "auth.json").read_bytes(), self.auth.read_bytes()
        )
        self.assertTrue((resumed_output / "codex-trace").is_dir())

    def test_resume_rejects_extra_non_system_skill(self) -> None:
        initial = self.run_entrypoint(self.invocation)
        self.assertEqual(initial.returncode, 0, initial.stderr)
        rogue = self.home / "skills/rogue"
        rogue.mkdir()
        rogue.joinpath("SKILL.md").write_text("# unapproved\n")
        self.argv_log.unlink()
        resumed_output = self.root / "resumed-invocation"
        resumed_output.mkdir()

        resumed = self.run_entrypoint(
            resumed_output,
            kind="timeout-resume",
            session=self.session_id,
        )

        self.assertEqual(resumed.returncode, 70)
        self.assertFalse(self.argv_log.exists())
        self.assertIn(
            "persisted Kit skills differ from approved Kit",
            resumed.stderr,
        )

    def test_infrastructure_retry_resumes_exact_session(self) -> None:
        result = self.run_entrypoint(
            self.invocation,
            kind="infrastructure-retry",
            session=self.session_id,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        arguments = json.loads(self.argv_log.read_text())
        resume_index = arguments.index("resume")
        self.assertEqual(arguments[resume_index + 1], self.session_id)

    def test_bubblewrap_preflight_runs_before_model(self) -> None:
        result = self.run_entrypoint(self.invocation)
        self.assertEqual(result.returncode, 0, result.stderr)
        arguments = json.loads(self.bwrap_log.read_text())
        self.assertIn("--unshare-user", arguments)
        self.assertIn("--unshare-pid", arguments)
        self.assertIn("--unshare-net", arguments)
        self.assertIn("--ro-bind", arguments)
        self.assertTrue(self.argv_log.exists())

    def test_bubblewrap_preflight_failure_stops_before_model(self) -> None:
        result = self.run_entrypoint(
            self.invocation, extra={"FAKE_BWRAP_RC": "1"}
        )
        self.assertEqual(result.returncode, 70)
        self.assertFalse(self.argv_log.exists())
        self.assertIn("sandbox preflight failed", result.stderr)

    def test_watchdog_marks_timeout_before_killing_whole_process_group(self) -> None:
        result = self.run_entrypoint(
            self.invocation,
            extra={
                "TIMEOUT_S": "1",
                "TIMEOUT_GRACE_S": "0.2",
                "FAKE_CODEX_MODE": "timeout",
            },
            timeout=8,
        )
        self.assertNotEqual(result.returncode, 0)
        metrics = json.loads((self.invocation / "metrics.json").read_text())
        self.assertTrue(metrics["timeout_marker"])
        self.assertNotEqual(metrics["model_exit_code"], 124)
        child_pid = int((self.root / "child.pid").read_text())
        with self.assertRaises(ProcessLookupError):
            os.kill(child_pid, 0)

    def test_exit_124_without_watchdog_marker_is_not_a_timeout(self) -> None:
        result = self.run_entrypoint(
            self.invocation,
            extra={"FAKE_CODEX_RC": "124"},
        )
        self.assertEqual(result.returncode, 124)
        metrics = json.loads((self.invocation / "metrics.json").read_text())
        self.assertFalse(metrics["timeout_marker"])
        self.assertEqual(metrics["model_exit_code"], 124)

    def test_rejects_resume_without_uuid_before_running_model(self) -> None:
        result = self.run_entrypoint(
            self.invocation, kind="timeout-resume", session="not-a-uuid"
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.argv_log.exists())
        self.assertFalse((self.invocation / "metrics.json").exists())


if __name__ == "__main__":
    unittest.main()
