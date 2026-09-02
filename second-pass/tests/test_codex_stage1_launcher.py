import json
import os
import shutil
import subprocess
import tempfile
import unittest
import uuid
from pathlib import Path

from tests.test_pipeline_layout import PipelineLayoutFixture
from tools import pipeline_contract, stage1_runner


REPO = Path(__file__).resolve().parent.parent


class Stage1LauncherTests(PipelineLayoutFixture):
    def setUp(self) -> None:
        super().setUp()
        self.run_id = "experiment-alpha"
        pipeline_contract.create_run(
            self.repo,
            run_id=self.run_id,
            config="codex-gpt-special-xhigh-kit-semantics",
            problem_ids=[self.PROBLEM],
        )
        self.fake_root = self.repo / "fake-docker-state"
        self.fake_root.mkdir()
        self.scenarios = self.fake_root / "scenarios.json"
        self.calls = self.fake_root / "calls.jsonl"
        self.session_id = str(uuid.uuid4())
        self.fake_docker = self.repo / "fake-docker"
        self.fake_docker.write_text(
            """#!/usr/bin/env python3
import json
import os
from pathlib import Path
import sys

root = Path(os.environ["FAKE_DOCKER_ROOT"])
args = sys.argv[1:]
with (root / "calls.jsonl").open("a") as stream:
    stream.write(json.dumps({
        "args": args,
        "invocation": os.environ.get("INVOCATION_DIR"),
        "workspace": os.environ.get("WORKSPACE_DIR"),
        "home": os.environ.get("CODEX_HOME_DIR"),
        "prompt": os.environ.get("PROMPT_PATH"),
        "kind": os.environ.get("INVOCATION_KIND"),
        "session": os.environ.get("SESSION_ID"),
        "model": os.environ.get("MODEL"),
        "timeout": os.environ.get("TIMEOUT_S"),
        "memory": os.environ.get("MEMORY_LIMIT"),
    }) + "\\n")

if args[0] == "compose":
    scenarios_path = root / "scenarios.json"
    scenarios = json.loads(scenarios_path.read_text())
    scenario = scenarios.pop(0)
    scenarios_path.write_text(json.dumps(scenarios))
    name = args[args.index("--name") + 1]
    (root / f"{name}.json").write_text(json.dumps({
        "State": {
            "ExitCode": scenario.get("container_exit", scenario["exit"]),
            "OOMKilled": scenario.get("oom", False),
        },
        "Image": "sha256:fake-image",
    }))
    invocation = Path(os.environ["INVOCATION_DIR"])
    invocation.joinpath("codex-output.log").write_text("fake output\\n")
    invocation.joinpath("codex-last.txt").write_text(scenario.get(
        "last",
        "RESULT: KPROVE_PASSED — fake proof completed.\\n",
    ))
    invocation.joinpath("prompt.txt").write_text(
        Path(os.environ["PROMPT_PATH"]).read_text()
    )
    if not scenario.get("missing_trace", False):
        trace = invocation / "codex-trace/2026/07/23"
        trace.mkdir(parents=True)
        trace.joinpath("rollout.jsonl").write_text(json.dumps({
            "type": "session_meta",
            "payload": {"id": os.environ["FAKE_SESSION_ID"]},
        }) + "\\n")
    invocation.joinpath("metrics.json").write_text(json.dumps({
        "model_exit_code": scenario.get("model_exit", scenario["exit"]),
        "harness_exit_code": scenario.get("harness_exit", 0),
        "final_exit_code": scenario.get("final_exit", scenario["exit"]),
        "duration_s": scenario.get("duration", 1),
        "timeout_marker": scenario.get("timeout", False),
        "oom_killed": scenario.get("cgroup_oom", False),
    }) + "\\n")
    raise SystemExit(scenario["exit"])
if args[0] == "inspect":
    print("[" + (root / f"{args[1]}.json").read_text() + "]")
    raise SystemExit(0)
if args[0] == "rm":
    raise SystemExit(0)
raise SystemExit(99)
"""
        )
        self.fake_docker.chmod(0o755)

    def set_scenarios(self, *documents: dict[str, object]) -> None:
        self.scenarios.write_text(json.dumps(documents))

    def run_stage(
        self,
        *,
        infrastructure_retry: bool = False,
        oom_resume: bool = False,
        terminal_resume: bool = False,
    ) -> dict[str, object]:
        old = os.environ.get("FAKE_DOCKER_ROOT")
        old_session = os.environ.get("FAKE_SESSION_ID")
        os.environ["FAKE_DOCKER_ROOT"] = str(self.fake_root)
        os.environ["FAKE_SESSION_ID"] = self.session_id
        try:
            return stage1_runner.run_stage1(
                self.repo,
                self.run_id,
                self.PROBLEM,
                docker=str(self.fake_docker),
                infrastructure_retry=infrastructure_retry,
                oom_resume=oom_resume,
                terminal_resume=terminal_resume,
            )
        finally:
            if old is None:
                os.environ.pop("FAKE_DOCKER_ROOT", None)
            else:
                os.environ["FAKE_DOCKER_ROOT"] = old
            if old_session is None:
                os.environ.pop("FAKE_SESSION_ID", None)
            else:
                os.environ["FAKE_SESSION_ID"] = old_session

    def read_calls(self) -> list[dict[str, object]]:
        return [json.loads(line) for line in self.calls.read_text().splitlines()]

    def prepare_infrastructure_blocked_second(self) -> None:
        initial = pipeline_contract.prepare_invocation(
            self.repo, self.run_id, self.PROBLEM, "01-k-proof"
        )
        trace = initial.path / "codex-trace/2026/07/23"
        trace.mkdir(parents=True)
        trace.joinpath("rollout.jsonl").write_text(
            json.dumps(
                {
                    "type": "session_meta",
                    "payload": {"id": self.session_id},
                }
            )
            + "\n"
        )
        pipeline_contract.finalize_invocation(
            self.repo,
            self.run_id,
            self.PROBLEM,
            "01-k-proof",
            initial.name,
            exit_code=143,
            duration_s=3600,
            timeout_marker=True,
            oom_killed=False,
            image_id="sha256:legacy",
        )
        second = pipeline_contract.prepare_invocation(
            self.repo, self.run_id, self.PROBLEM, "01-k-proof"
        )
        second.path.joinpath("codex-output.log").write_text(
            "bwrap: No permissions to create a new namespace\n"
        )
        pipeline_contract.finalize_invocation(
            self.repo,
            self.run_id,
            self.PROBLEM,
            "01-k-proof",
            second.name,
            exit_code=0,
            duration_s=60,
            timeout_marker=False,
            oom_killed=False,
            image_id="sha256:broken",
        )

    def test_print_config_reads_manifest_without_preparing_invocation(self) -> None:
        document = stage1_runner.inspect_stage1(
            self.repo, self.run_id, self.PROBLEM
        )
        self.assertEqual(document["config"], "codex-gpt-special-xhigh-kit-semantics")
        self.assertEqual(document["model"], "gpt-special")
        self.assertEqual(document["condition"], "kit-semantics")
        self.assertEqual(document["kit"], 1)
        self.assertEqual(document["prompt"], "kit-semantics.md")
        self.assertEqual(
            list(
                (
                    self.repo
                    / f"runs/{self.run_id}/tasks/{self.PROBLEM}/01-k-proof/invocations"
                ).iterdir()
            ),
            [],
        )

    def test_success_uses_exact_stage_mounts_and_finalizes_initial(self) -> None:
        self.set_scenarios({"exit": 0})
        result = self.run_stage()
        self.assertEqual(result["status"], "SUCCEEDED")
        invocations = (
            self.repo
            / f"runs/{self.run_id}/tasks/{self.PROBLEM}/01-k-proof/invocations"
        )
        self.assertEqual([path.name for path in invocations.iterdir()], ["001-initial"])
        calls = self.read_calls()
        compose = calls[0]
        self.assertEqual(compose["kind"], "initial")
        self.assertEqual(compose["session"], "")
        self.assertEqual(compose["model"], "gpt-special")
        self.assertEqual(compose["timeout"], "3600")
        self.assertEqual(
            compose["workspace"],
            str(
                self.repo
                / f"runs/{self.run_id}/tasks/{self.PROBLEM}/01-k-proof/workspace"
            ),
        )
        self.assertEqual(
            compose["home"],
            str(self.repo / f"runner-state/{self.run_id}/{self.PROBLEM}/codex-home"),
        )
        self.assertIn("--name", compose["args"])
        self.assertNotIn("--rm", compose["args"])

    def test_result_marker_parser_requires_one_exact_terminal_marker(self) -> None:
        last = self.repo / "last.txt"
        for marker in ("KPROVE_PASSED", "PARTIAL", "BLOCKED"):
            with self.subTest(marker=marker):
                last.write_text(
                    f"Summary.\n\nRESULT: {marker} — exact explanation.\n"
                )
                self.assertEqual(
                    stage1_runner.parse_stage1_result(last), marker
                )
        for label, content in (
            ("missing", "Summary only.\n"),
            ("malformed", "RESULT: KPROVE_PASSED - wrong dash\n"),
            (
                "multiple",
                "RESULT: PARTIAL — first.\n"
                "RESULT: KPROVE_PASSED — second.\n",
            ),
            ("empty", "RESULT: KPROVE_PASSED — \n"),
        ):
            with self.subTest(label=label):
                last.write_text(content)
                with self.assertRaises(stage1_runner.Stage1RunnerError):
                    stage1_runner.parse_stage1_result(last)

    def test_exit_zero_blocked_marker_is_not_success(self) -> None:
        self.set_scenarios(
            {
                "exit": 0,
                "last": "RESULT: BLOCKED — command execution failed.\n",
            }
        )
        result = self.run_stage()
        self.assertEqual(result["status"], "FAILED")

    def test_explicit_infrastructure_retry_resumes_same_session_once(
        self,
    ) -> None:
        self.prepare_infrastructure_blocked_second()
        self.set_scenarios({"exit": 0})

        result = self.run_stage(infrastructure_retry=True)

        self.assertEqual(result["status"], "SUCCEEDED")
        calls = [
            call
            for call in self.read_calls()
            if call["args"][0] == "compose"
        ]
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]["kind"], "infrastructure-retry")
        self.assertEqual(calls[0]["session"], self.session_id)
        self.assertEqual(calls[0]["timeout"], "3600")
        self.assertEqual(
            Path(calls[0]["prompt"]).name,
            "infrastructure-resume.md",
        )
        invocations = (
            self.repo
            / f"runs/{self.run_id}/tasks/{self.PROBLEM}"
            / "01-k-proof/invocations"
        )
        self.assertEqual(
            sorted(path.name for path in invocations.iterdir()),
            [
                "001-initial",
                "002-timeout-resume",
                "003-infrastructure-retry",
            ],
        )

    def test_wrapper_timeout_automatically_resumes_same_session_once(self) -> None:
        self.set_scenarios(
            {"exit": 143, "timeout": True, "duration": 3600},
            {"exit": 0, "duration": 12},
        )
        result = self.run_stage()
        self.assertEqual(result["status"], "SUCCEEDED")
        calls = [call for call in self.read_calls() if call["args"][0] == "compose"]
        self.assertEqual([call["kind"] for call in calls], ["initial", "timeout-resume"])
        self.assertEqual(calls[1]["session"], self.session_id)
        self.assertEqual(calls[1]["timeout"], "3600")
        self.assertEqual(Path(calls[1]["prompt"]).name, "timeout-resume.md")
        result_path = (
            self.repo
            / f"runs/{self.run_id}/tasks/{self.PROBLEM}/01-k-proof/result.json"
        )
        self.assertEqual(json.loads(result_path.read_text())["status"], "SUCCEEDED")

    def test_explicit_oom_resume_uses_same_session_and_16g(self) -> None:
        initial = pipeline_contract.prepare_invocation(
            self.repo, self.run_id, self.PROBLEM, "01-k-proof"
        )
        trace = initial.path / "codex-trace/2026/07/23"
        trace.mkdir(parents=True)
        trace.joinpath("rollout.jsonl").write_text(
            json.dumps(
                {
                    "type": "session_meta",
                    "payload": {"id": self.session_id},
                }
            )
            + "\n"
        )
        pipeline_contract.finalize_invocation(
            self.repo,
            self.run_id,
            self.PROBLEM,
            "01-k-proof",
            initial.name,
            exit_code=137,
            duration_s=100,
            timeout_marker=False,
            oom_killed=True,
            image_id="sha256:legacy",
        )
        self.set_scenarios({"exit": 0})

        result = self.run_stage(oom_resume=True)

        self.assertEqual(result["status"], "SUCCEEDED")
        calls = [
            call
            for call in self.read_calls()
            if call["args"][0] == "compose"
        ]
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]["kind"], "timeout-resume")
        self.assertEqual(calls[0]["session"], self.session_id)
        self.assertEqual(calls[0]["timeout"], "3600")
        self.assertEqual(calls[0]["memory"], "16g")
        self.assertEqual(Path(calls[0]["prompt"]).name, "oom-resume.md")
        manifest = json.loads(
            (
                self.repo
                / f"runs/{self.run_id}/tasks/{self.PROBLEM}/01-k-proof"
                / "invocations/002-oom-resume/invocation.json"
            ).read_text()
        )
        self.assertEqual(manifest["kind"], "oom-resume")
        self.assertEqual(manifest["memory_limit_bytes"], 16 * 1024**3)

    def test_explicit_terminal_resume_uses_same_session_and_8g(self) -> None:
        initial = pipeline_contract.prepare_invocation(
            self.repo, self.run_id, self.PROBLEM, "01-k-proof"
        )
        trace = initial.path / "codex-trace/2026/07/23"
        trace.mkdir(parents=True)
        trace.joinpath("rollout.jsonl").write_text(
            json.dumps(
                {
                    "type": "session_meta",
                    "payload": {"id": self.session_id},
                }
            )
            + "\n"
        )
        pipeline_contract.finalize_invocation(
            self.repo,
            self.run_id,
            self.PROBLEM,
            "01-k-proof",
            initial.name,
            exit_code=1,
            duration_s=100,
            timeout_marker=False,
            oom_killed=False,
            image_id="sha256:legacy",
        )
        self.set_scenarios({"exit": 0})

        result = self.run_stage(terminal_resume=True)

        self.assertEqual(result["status"], "SUCCEEDED")
        calls = [
            call
            for call in self.read_calls()
            if call["args"][0] == "compose"
        ]
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]["kind"], "timeout-resume")
        self.assertEqual(calls[0]["session"], self.session_id)
        self.assertEqual(calls[0]["timeout"], "3600")
        self.assertEqual(calls[0]["memory"], "8g")
        self.assertEqual(
            Path(calls[0]["prompt"]).name, "terminal-resume.md"
        )

    def test_plain_exit_124_and_oom_do_not_resume(self) -> None:
        for label, scenario, expected in (
            ("plain-124", {"exit": 124}, "FAILED"),
            ("oom", {"exit": 137, "oom": True}, "OOM"),
        ):
            with self.subTest(label=label):
                if label != "plain-124":
                    # Each run is immutable; use a second task/run for the OOM case.
                    other = "19-sort-numbers"
                    self.make_problem(other)
                    pipeline_contract.create_run(
                        self.repo,
                        run_id="oom-experiment",
                        config="codex-gpt-special-xhigh-bare",
                        problem_ids=[other],
                    )
                    run_id, problem = "oom-experiment", other
                else:
                    run_id, problem = self.run_id, self.PROBLEM
                self.set_scenarios(scenario)
                old_root = os.environ.get("FAKE_DOCKER_ROOT")
                old_session = os.environ.get("FAKE_SESSION_ID")
                os.environ["FAKE_DOCKER_ROOT"] = str(self.fake_root)
                os.environ["FAKE_SESSION_ID"] = self.session_id
                try:
                    result = stage1_runner.run_stage1(
                        self.repo,
                        run_id,
                        problem,
                        docker=str(self.fake_docker),
                    )
                finally:
                    if old_root is None:
                        os.environ.pop("FAKE_DOCKER_ROOT", None)
                    else:
                        os.environ["FAKE_DOCKER_ROOT"] = old_root
                    if old_session is None:
                        os.environ.pop("FAKE_SESSION_ID", None)
                    else:
                        os.environ["FAKE_SESSION_ID"] = old_session
                self.assertEqual(result["status"], expected)

    def test_timeout_without_persistable_session_stops_before_resume(self) -> None:
        self.set_scenarios(
            {"exit": 143, "timeout": True, "missing_trace": True}
        )
        result = self.run_stage()
        self.assertEqual(result["status"], "TIMEOUT")
        self.assertFalse(result["resumable"])
        calls = [call for call in self.read_calls() if call["args"][0] == "compose"]
        self.assertEqual(len(calls), 1)

    def test_harness_failure_uses_final_not_model_exit_code(self) -> None:
        self.set_scenarios(
            {
                "exit": 70,
                "model_exit": 0,
                "harness_exit": 70,
                "final_exit": 70,
                "missing_trace": True,
            }
        )
        result = self.run_stage()
        self.assertEqual(result["status"], "FAILED")
        self.assertIsNone(result["session_id"])

    def test_compose_declares_separate_mount_modes(self) -> None:
        compose = (REPO / "docker/codex/docker-compose.yml").read_text()
        self.assertIn("${WORKSPACE_DIR:-/tmp}:/workspace:rw", compose)
        self.assertIn("${INVOCATION_DIR:-/tmp}:/invocation-output:rw", compose)
        self.assertIn("${CODEX_HOME_DIR:-/tmp}:/codex-home:rw", compose)
        self.assertIn("${PROMPT_PATH:-../../prompts/bare.md}:/invocation-prompt.md:ro", compose)
        self.assertIn("seccomp=unconfined", compose)
        self.assertNotIn("cap_add:", compose)

    def test_shell_cli_uses_run_id_problem_grammar(self) -> None:
        # Copy only the launcher stack; it must locate the run manifest rather
        # than infer configuration from the run directory name.
        for relative in (
            "docker/codex/run_task.sh",
            "tools/stage1_runner.py",
            "tools/pipeline_contract.py",
        ):
            destination = self.repo / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO / relative, destination)
        result = subprocess.run(
            [
                "bash",
                str(self.repo / "docker/codex/run_task.sh"),
                "--print-config",
                self.run_id,
                self.PROBLEM,
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"run_id={self.run_id}\n", result.stdout)
        self.assertIn("model=gpt-special\n", result.stdout)


if __name__ == "__main__":
    unittest.main()
