import copy
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
import uuid
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from tools import migrate_six_stage_layout, pipeline_contract


RUN_ID = "fixture-schema-v2-run"
PROBLEM = "0-fixture"
SECOND_RUN_ID = "fixture-schema-v2-run-two"
SECOND_PROBLEM = "1-fixture"

EXPECTED_LAYOUT = {
    "schema_from": 2,
    "schema_to": 3,
    "moves": {
        "03-klean-generation": "04-klean-generation/legacy-v2",
        "04-lean-proof": "05-lean-proof/legacy-v2",
        "05-lean-audit": "06-lean-audit/legacy-v2",
    },
    "creates": [
        "03-lemma-discovery/workspace",
        "03-lemma-discovery/invocations",
        "04-klean-generation/generations",
        "05-lean-proof/workspace",
        "05-lean-proof/invocations",
        "06-lean-audit/executions",
    ],
}


class SixStageMigrationFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name)
        self.run = self.repo / "runs" / RUN_ID
        self.task = self.run / "tasks" / PROBLEM
        self.state = self.repo / "runner-state" / RUN_ID / PROBLEM
        self.task.mkdir(parents=True)
        self.state.mkdir(parents=True)
        self._write_schema_v2_run()

    @staticmethod
    def write_json(path: Path, document: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")

    def _write_schema_v2_run(self) -> None:
        self.write_json(
            self.run / "run.json",
            {
                "schema_version": 2,
                "run_id": RUN_ID,
                "tasks": [PROBLEM],
                "timeouts": {
                    "k_initial_s": 3600,
                    "k_total_s": 7200,
                    "lean_initial_s": 3600,
                    "lean_total_s": 7200,
                },
            },
        )
        (self.run / "task-list.txt").write_text(f"{PROBLEM}\n")
        self.write_json(
            self.task / "task.json",
            {
                "schema_version": 2,
                "problem_id": PROBLEM,
                "current_stage": "05-lean-audit",
                "inputs": {"problem_prompt_sha256": "a" * 64},
            },
        )

        fixtures = {
            "01-k-proof/workspace/spec.k": b"module SPEC endmodule\n",
            "02-k-audit/executions/001/verdict.json": (
                b'{"audit_status":"COMPLETE","verdict":"PASS"}\n'
            ),
            "02-k-audit/selected.json": b'{"relative_path":"executions/001"}\n',
            "03-klean-generation/generations/001/target.lean": (
                b"theorem legacy : True := by trivial\n"
            ),
            "03-klean-generation/selected.json": (
                b'{"relative_path":"generations/001"}\n'
            ),
            "04-lean-proof/workspace/Proof.lean": (
                b"theorem legacy : True := by trivial\n"
            ),
            "04-lean-proof/result.json": (
                b'{"schema_version":2,"status":"SUCCEEDED"}\n'
            ),
            "05-lean-audit/executions/001/verdict.json": (
                b'{"audit_status":"COMPLETE","verdict":"PASS"}\n'
            ),
            "05-lean-audit/selected.json": (
                b'{"relative_path":"executions/001"}\n'
            ),
        }
        for relative, content in fixtures.items():
            path = self.task / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        (self.task / "01-k-proof/invocations").mkdir()

        codex_home = self.state / "codex-home"
        rollout = codex_home / "sessions/2026/07/24/rollout.jsonl"
        rollout.parent.mkdir(parents=True)
        session_id = str(uuid.UUID(int=1))
        rollout.write_text(
            json.dumps(
                {
                    "type": "session_meta",
                    "payload": {"id": session_id},
                }
            )
            + "\n"
        )
        (codex_home / "auth.json").write_bytes(b"fixture-credential-state\n")
        home_stat = codex_home.stat()
        self.write_json(
            self.state / "session.json",
            {
                "schema_version": 2,
                "session_id": session_id,
                "codex_home_relative": "codex-home",
                "codex_home_device": home_stat.st_dev,
                "codex_home_inode": home_stat.st_ino,
                "source": "01-k-proof/001-initial",
            },
        )
        stage1_invocation = (
            self.task / "01-k-proof/invocations/001-initial"
        )
        stage1_trace = stage1_invocation / "codex-trace"
        stage1_trace.mkdir(parents=True)
        stage1_rollout = stage1_trace / "rollout.jsonl"
        stage1_rollout.write_bytes(rollout.read_bytes())
        self.write_json(
            stage1_invocation / "invocation.json",
            {
                "schema_version": 2,
                "stage": "01-k-proof",
                "name": "001-initial",
                "status": "SUCCEEDED",
                "session_id": session_id,
            },
        )
        self.write_json(
            self.task / "01-k-proof/result.json",
            {
                "schema_version": 2,
                "status": "SUCCEEDED",
                "invocation": "001-initial",
                "session_id": session_id,
            },
        )
        ledger = [
            {
                "sequence": 1,
                "event": "invocation_finalized",
                "stage": "01-k-proof",
            },
            {
                "sequence": 2,
                "event": "stage_output_selected",
                "stage": "02-k-audit",
            },
            {
                "sequence": 3,
                "event": "stage_output_selected",
                "stage": "03-klean-generation",
            },
            {
                "sequence": 4,
                "event": "invocation_finalized",
                "stage": "04-lean-proof",
            },
            {
                "sequence": 5,
                "event": "stage_output_selected",
                "stage": "05-lean-audit",
            },
        ]
        (self.state / "stage-ledger.jsonl").write_text(
            "".join(json.dumps(event, sort_keys=True) + "\n" for event in ledger)
        )

    def repository_hashes(self) -> dict[str, str]:
        return {
            "run": pipeline_contract.sha256_tree(self.run),
            "state": pipeline_contract.sha256_tree(
                self.repo / "runner-state" / RUN_ID
            ),
        }

    def hashes_for_runs(self, run_ids: list[str]) -> dict[str, str]:
        return {
            f"run:{run_id}": pipeline_contract.sha256_tree(
                self.repo / "runs" / run_id
            )
            for run_id in run_ids
        } | {
            f"state:{run_id}": pipeline_contract.sha256_tree(
                self.repo / "runner-state" / run_id
            )
            for run_id in run_ids
        }

    def clone_run(self) -> None:
        cloned_run = self.repo / "runs" / SECOND_RUN_ID
        cloned_state = self.repo / "runner-state" / SECOND_RUN_ID
        shutil.copytree(self.run, cloned_run)
        shutil.copytree(
            self.repo / "runner-state" / RUN_ID,
            cloned_state,
        )
        (cloned_run / "tasks" / PROBLEM).rename(
            cloned_run / "tasks" / SECOND_PROBLEM
        )
        (cloned_state / PROBLEM).rename(cloned_state / SECOND_PROBLEM)

        run_manifest = json.loads((cloned_run / "run.json").read_text())
        run_manifest.update(
            {"run_id": SECOND_RUN_ID, "tasks": [SECOND_PROBLEM]}
        )
        self.write_json(cloned_run / "run.json", run_manifest)
        (cloned_run / "task-list.txt").write_text(f"{SECOND_PROBLEM}\n")
        task_manifest = json.loads(
            (
                cloned_run / "tasks" / SECOND_PROBLEM / "task.json"
            ).read_text()
        )
        task_manifest["problem_id"] = SECOND_PROBLEM
        self.write_json(
            cloned_run / "tasks" / SECOND_PROBLEM / "task.json",
            task_manifest,
        )
        task_state = cloned_state / SECOND_PROBLEM
        session = json.loads((task_state / "session.json").read_text())
        home_stat = (task_state / "codex-home").stat()
        session["codex_home_device"] = home_stat.st_dev
        session["codex_home_inode"] = home_stat.st_ino
        self.write_json(task_state / "session.json", session)

    def crash_apply_at(
        self,
        plan: dict[str, object],
        boundary: str,
        occurrence: int = 1,
    ) -> None:
        pid = os.fork()
        if pid == 0:
            migrate_six_stage_layout._candidate_processes = lambda: ()
            observed = 0

            def crash(name: str) -> None:
                nonlocal observed
                if name != boundary:
                    return
                observed += 1
                if observed == occurrence:
                    os._exit(91)

            migrate_six_stage_layout._publication_boundary = crash
            try:
                migrate_six_stage_layout.apply_migration(self.repo, plan)
            except BaseException:
                os._exit(92)
            os._exit(93)
        waited, status = os.waitpid(pid, 0)
        self.assertEqual(waited, pid)
        self.assertTrue(os.WIFEXITED(status))
        self.assertEqual(os.WEXITSTATUS(status), 91)

    def crash_during_tombstone_deletion(
        self,
        plan: dict[str, object],
    ) -> None:
        pid = os.fork()
        if pid == 0:
            migrate_six_stage_layout._candidate_processes = lambda: ()
            original_rmtree = shutil.rmtree

            def crash_rmtree(
                path: str | os.PathLike[str],
                *args: object,
                **kwargs: object,
            ) -> None:
                target = Path(path)
                if target.name.endswith(".tombstone"):
                    regular = next(
                        candidate
                        for candidate in target.rglob("*")
                        if candidate.is_file()
                    )
                    regular.unlink()
                    os._exit(91)
                original_rmtree(path, *args, **kwargs)

            migrate_six_stage_layout.shutil.rmtree = crash_rmtree
            try:
                migrate_six_stage_layout.apply_migration(self.repo, plan)
            except BaseException:
                os._exit(92)
            os._exit(93)
        waited, status = os.waitpid(pid, 0)
        self.assertEqual(waited, pid)
        self.assertTrue(os.WIFEXITED(status))
        self.assertEqual(os.WEXITSTATUS(status), 91)

    def stage_hashes(self) -> dict[str, str]:
        return {
            stage: pipeline_contract.sha256_tree(self.task / stage)
            for stage in (
                "01-k-proof",
                "02-k-audit",
                "03-klean-generation",
                "04-lean-proof",
                "05-lean-audit",
            )
        }

    def plan_without_processes(self) -> dict[str, object]:
        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=(),
        ):
            return migrate_six_stage_layout.plan_migration(
                self.repo,
                [RUN_ID],
            )


class SixStageMigrationTests(SixStageMigrationFixture):
    def test_dry_run_reports_exact_layout_and_is_read_only(self) -> None:
        before = self.repository_hashes()

        plan = self.plan_without_processes()

        self.assertEqual(
            {name: plan[name] for name in EXPECTED_LAYOUT},
            EXPECTED_LAYOUT,
        )
        self.assertEqual(plan["blockers"], [])
        self.assertEqual(
            plan["runs"][0]["source_sha256"],
            before["run"],
        )
        self.assertEqual(
            plan["runs"][0]["runner_state_sha256"],
            before["state"],
        )
        self.assertEqual(self.repository_hashes(), before)
        self.assertFalse(
            any(self.repo.joinpath("runs").glob(".six-stage-migration-*"))
        )
        self.assertFalse(
            any(
                self.repo.joinpath("runner-state").glob(
                    ".six-stage-migration-*"
                )
            )
        )

    def test_apply_preserves_legacy_trees_and_starts_stages_three_to_six_empty(
        self,
    ) -> None:
        original = self.stage_hashes()
        credential = (self.state / "codex-home/auth.json").read_bytes()
        plan = self.plan_without_processes()
        session_proof = plan["runs"][0]["tasks"][0][
            "session_provenance"
        ]
        self.assertEqual(session_proof["status"], "RECOVERABLE")
        self.assertRegex(session_proof["session_id"], r"^[0-9a-f-]{36}$")
        self.assertTrue(session_proof["persistent_rollouts"])
        self.assertTrue(session_proof["stage1_rollouts"])
        self.assertRegex(
            session_proof["stage1_result_sha256"],
            r"^[0-9a-f]{64}$",
        )
        self.assertRegex(
            session_proof["stage1_invocation_sha256"],
            r"^[0-9a-f]{64}$",
        )

        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=(),
        ):
            result = migrate_six_stage_layout.apply_migration(
                self.repo,
                plan,
            )

        self.assertEqual(result["status"], "COMPLETE")
        self.assertEqual(result["runs"], [RUN_ID])
        self.assertEqual(
            pipeline_contract.sha256_tree(self.task / "01-k-proof"),
            original["01-k-proof"],
        )
        self.assertEqual(
            pipeline_contract.sha256_tree(self.task / "02-k-audit"),
            original["02-k-audit"],
        )
        for source, destination in EXPECTED_LAYOUT["moves"].items():
            with self.subTest(source=source):
                self.assertEqual(
                    pipeline_contract.sha256_tree(self.task / destination),
                    original[source],
                )
        for relative in EXPECTED_LAYOUT["creates"]:
            self.assertEqual(list((self.task / relative).iterdir()), [])
        self.assertFalse(
            (self.task / "04-klean-generation/selected.json").exists()
        )
        self.assertEqual(
            json.loads((self.run / "run.json").read_text())["schema_version"],
            3,
        )
        run_manifest = json.loads((self.run / "run.json").read_text())
        self.assertEqual(run_manifest["timeouts"]["lemma_initial_s"], 1200)
        self.assertEqual(run_manifest["timeouts"]["lemma_total_s"], 1200)
        task_manifest = json.loads((self.task / "task.json").read_text())
        self.assertEqual(task_manifest["schema_version"], 3)
        self.assertEqual(task_manifest["current_stage"], "03-lemma-discovery")

        self.assertEqual(
            (self.state / "codex-home/auth.json").read_bytes(),
            credential,
        )
        self.assertFalse(any(self.run.rglob("auth.json")))
        session = pipeline_contract._read_session_state(self.state)
        self.assertEqual(session["schema_version"], 3)
        task_manifest = json.loads((self.task / "task.json").read_text())
        self.assertEqual(
            task_manifest["session_provenance"]["status"],
            "RECOVERABLE",
        )
        self.assertEqual(
            task_manifest["session_provenance"]["session_id"],
            session["session_id"],
        )
        self.assertNotIn("pipeline_block", task_manifest)

    def assert_unrecoverable_session_migrates_blocked(
        self,
        reason: str,
        preserved_session: bytes | None,
    ) -> None:
        original = self.repository_hashes()
        plan = self.plan_without_processes()
        recovery = plan["runs"][0]["tasks"][0][
            "session_provenance"
        ]
        self.assertEqual(recovery["status"], "UNRECOVERABLE")
        self.assertEqual(recovery["reason"], reason)

        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=(),
        ):
            migrate_six_stage_layout.apply_migration(
                self.repo,
                plan,
            )

        task_manifest = json.loads(
            (self.task / "task.json").read_text()
        )
        self.assertEqual(
            task_manifest["pipeline_block"],
            "SESSION_STATE_UNRECOVERABLE",
        )
        self.assertEqual(
            task_manifest["session_provenance"]["reason"],
            reason,
        )
        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError,
            "SESSION_STATE_UNRECOVERABLE",
        ):
            pipeline_contract.require_task_unblocked(
                self.task,
                "Stage 3",
            )
        if preserved_session is not None:
            self.assertEqual(
                (
                    self.state / "legacy-v2/session.json"
                ).read_bytes(),
                preserved_session,
            )
        self.assertNotEqual(self.repository_hashes(), original)

    def test_absent_session_state_migrates_blocked(self) -> None:
        (self.state / "session.json").unlink()
        self.assert_unrecoverable_session_migrates_blocked(
            "SESSION_STATE_MISSING",
            None,
        )

    def test_malformed_session_state_migrates_blocked_and_preserved(
        self,
    ) -> None:
        malformed = b"{malformed legacy bytes\n"
        (self.state / "session.json").write_bytes(malformed)
        self.assert_unrecoverable_session_migrates_blocked(
            "SESSION_STATE_MALFORMED",
            malformed,
        )

    def test_mismatched_session_state_migrates_blocked_and_preserved(
        self,
    ) -> None:
        session_path = self.state / "session.json"
        session = json.loads(session_path.read_text())
        session["session_id"] = str(uuid.UUID(int=2))
        self.write_json(session_path, session)
        preserved = session_path.read_bytes()
        self.assert_unrecoverable_session_migrates_blocked(
            "SESSION_ID_MISMATCH",
            preserved,
        )

    def test_device_number_drift_with_identical_rollout_remains_recoverable(
        self,
    ) -> None:
        session_path = self.state / "session.json"
        session = json.loads(session_path.read_text())
        session["codex_home_device"] += 1
        self.write_json(session_path, session)

        plan = self.plan_without_processes()

        recovery = plan["runs"][0]["tasks"][0]["session_provenance"]
        self.assertEqual(recovery["status"], "RECOVERABLE")
        self.assertEqual(
            sorted(
                item["sha256"]
                for item in recovery["persistent_rollouts"]
            ),
            sorted(
                item["sha256"] for item in recovery["stage1_rollouts"]
            ),
        )

    def test_device_number_drift_with_changed_rollout_is_unrecoverable(
        self,
    ) -> None:
        session_path = self.state / "session.json"
        session = json.loads(session_path.read_text())
        session["codex_home_device"] += 1
        self.write_json(session_path, session)
        rollout = next(
            (self.state / "codex-home/sessions").rglob("*.jsonl")
        )
        rollout.write_text(
            rollout.read_text()
            + json.dumps({"type": "response_item", "payload": {}})
            + "\n"
        )

        plan = self.plan_without_processes()

        recovery = plan["runs"][0]["tasks"][0]["session_provenance"]
        self.assertEqual(recovery["status"], "UNRECOVERABLE")
        self.assertEqual(recovery["reason"], "SESSION_ID_MISMATCH")

    def test_valid_timeout_resume_session_remains_recoverable(self) -> None:
        session = json.loads((self.state / "session.json").read_text())
        resumed = self.task / (
            "01-k-proof/invocations/002-timeout-resume"
        )
        resumed_trace = resumed / "codex-trace"
        resumed_trace.mkdir(parents=True)
        shutil.copy2(
            self.task
            / "01-k-proof/invocations/001-initial/codex-trace/rollout.jsonl",
            resumed_trace / "rollout.jsonl",
        )
        self.write_json(
            resumed / "invocation.json",
            {
                "schema_version": 2,
                "stage": "01-k-proof",
                "name": "002-timeout-resume",
                "status": "SUCCEEDED",
                "session_id": session["session_id"],
            },
        )
        self.write_json(
            self.task / "01-k-proof/result.json",
            {
                "schema_version": 2,
                "status": "SUCCEEDED",
                "invocation": "002-timeout-resume",
                "session_id": session["session_id"],
            },
        )

        plan = self.plan_without_processes()

        self.assertEqual(
            plan["runs"][0]["tasks"][0]["session_provenance"][
                "status"
            ],
            "RECOVERABLE",
        )

    def test_publication_failure_restores_original_run_and_state(self) -> None:
        before = self.repository_hashes()
        plan = self.plan_without_processes()

        def fail_after_run_exchange(boundary: str) -> None:
            if boundary == "after-run-exchange":
                raise RuntimeError("injected publication failure")

        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=(),
        ), mock.patch.object(
            migrate_six_stage_layout,
            "_publication_boundary",
            side_effect=fail_after_run_exchange,
        ):
            with self.assertRaisesRegex(
                RuntimeError,
                "injected publication failure",
            ):
                migrate_six_stage_layout.apply_migration(self.repo, plan)

        self.assertEqual(self.repository_hashes(), before)
        self.assertEqual(
            json.loads((self.run / "run.json").read_text())["schema_version"],
            2,
        )
        self.assertFalse(
            any(self.repo.joinpath("runs").glob(".six-stage-migration-*"))
        )
        self.assertFalse(
            any(
                self.repo.joinpath("runner-state").glob(
                    ".six-stage-migration-*"
                )
            )
        )

    def test_fsync_failure_after_exchange_restores_originals(self) -> None:
        before = self.repository_hashes()
        plan = self.plan_without_processes()
        calls = 0

        def fail_once(_first: Path, _second: Path) -> None:
            nonlocal calls
            calls += 1
            if calls == 1:
                raise OSError("injected post-exchange fsync failure")

        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=(),
        ), mock.patch.object(
            migrate_six_stage_layout,
            "_fsync_exchange_parents",
            side_effect=fail_once,
        ):
            with self.assertRaisesRegex(
                OSError,
                "post-exchange fsync failure",
            ):
                migrate_six_stage_layout.apply_migration(self.repo, plan)

        self.assertEqual(self.repository_hashes(), before)
        self.assertFalse(
            (
                self.repo
                / "runner-state/.six-stage-migration-transaction.json"
            ).exists()
        )
        self.assertFalse(
            any(self.repo.joinpath("runs").glob(".six-stage-migration-*"))
        )
        self.assertFalse(
            any(
                self.repo.joinpath("runner-state").glob(
                    ".six-stage-migration-*"
                )
            )
        )

    def test_fsync_tree_flushes_every_regular_file_and_directory(self) -> None:
        expected_files = {
            path.resolve()
            for path in self.run.rglob("*")
            if path.is_file()
        }
        expected_directories = {
            self.run.resolve(),
            *(
                path.resolve()
                for path in self.run.rglob("*")
                if path.is_dir()
            ),
        }
        observed_files: set[Path] = set()
        observed_directories: set[Path] = set()

        def observe_fsync(descriptor: int) -> None:
            mode = os.fstat(descriptor).st_mode
            target = Path(os.readlink(f"/proc/self/fd/{descriptor}")).resolve()
            if stat.S_ISREG(mode):
                observed_files.add(target)
            elif stat.S_ISDIR(mode):
                observed_directories.add(target)

        fsync_tree = getattr(
            migrate_six_stage_layout,
            "_fsync_tree",
            None,
        )
        self.assertIsNotNone(fsync_tree)
        with mock.patch.object(os, "fsync", side_effect=observe_fsync):
            fsync_tree(self.run)

        self.assertEqual(observed_files, expected_files)
        self.assertEqual(observed_directories, expected_directories)

    def test_staged_tree_fsync_failure_precedes_journal_and_exchange(
        self,
    ) -> None:
        before = self.repository_hashes()
        plan = self.plan_without_processes()

        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=(),
        ), mock.patch.object(
            migrate_six_stage_layout,
            "_fsync_tree",
            create=True,
            side_effect=OSError("injected staged-tree fsync failure"),
        ) as fsync_tree, mock.patch.object(
            migrate_six_stage_layout,
            "_write_journal",
            wraps=migrate_six_stage_layout._write_journal,
        ) as write_journal, mock.patch.object(
            migrate_six_stage_layout,
            "_atomic_exchange",
            wraps=migrate_six_stage_layout._atomic_exchange,
        ) as exchange:
            with self.assertRaisesRegex(
                migrate_six_stage_layout.SixStageMigrationError,
                "cannot fsync staged tree",
            ):
                migrate_six_stage_layout.apply_migration(self.repo, plan)

        self.assertTrue(fsync_tree.called)
        write_journal.assert_not_called()
        exchange.assert_not_called()
        self.assertEqual(self.repository_hashes(), before)
        self.assertFalse(
            (
                self.repo
                / "runner-state/.six-stage-migration-transaction.json"
            ).exists()
        )

    def test_partial_copy_failure_owns_and_removes_destination(self) -> None:
        source = self.run
        destination = self.repo / "runs/.six-stage-migration-partial"
        expected = pipeline_contract.sha256_tree(source)

        def partial_copy(
            _source: Path,
            observed_destination: Path,
            **_kwargs: object,
        ) -> None:
            observed_destination.mkdir()
            (observed_destination / "partial.bin").write_bytes(b"partial")
            raise OSError("injected partial copy failure")

        with mock.patch.object(
            migrate_six_stage_layout.shutil,
            "copytree",
            side_effect=partial_copy,
        ):
            with self.assertRaisesRegex(
                migrate_six_stage_layout.SixStageMigrationError,
                "cannot copy migration source",
            ):
                migrate_six_stage_layout._copy_tree(
                    source,
                    destination,
                    expected,
                )

        self.assertFalse(destination.exists())

    def test_apply_rejects_duplicate_run_ids_before_staging(self) -> None:
        before = self.repository_hashes()
        plan = self.plan_without_processes()
        plan["runs"].append(copy.deepcopy(plan["runs"][0]))

        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=(),
        ):
            with self.assertRaisesRegex(
                migrate_six_stage_layout.SixStageMigrationError,
                "duplicate run ID",
            ):
                migrate_six_stage_layout.apply_migration(self.repo, plan)

        self.assertEqual(self.repository_hashes(), before)
        self.assertFalse(
            any(self.repo.joinpath("runs").glob(".six-stage-migration-*"))
        )

    def test_apply_rejects_unsafe_run_id_before_staging(self) -> None:
        before = self.repository_hashes()
        plan = self.plan_without_processes()
        plan["runs"][0]["run_id"] = "../escape"

        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=(),
        ):
            with self.assertRaisesRegex(
                migrate_six_stage_layout.SixStageMigrationError,
                "safe",
            ):
                migrate_six_stage_layout.apply_migration(self.repo, plan)

        self.assertEqual(self.repository_hashes(), before)
        self.assertFalse(
            any(self.repo.joinpath("runs").glob(".six-stage-migration-*"))
        )

    def test_apply_rejects_unsafe_and_duplicate_problem_ids(self) -> None:
        for problem, pattern in (
            ("../escape", "safe"),
            (PROBLEM, "duplicate problem ID"),
        ):
            with self.subTest(problem=problem):
                before = self.repository_hashes()
                plan = self.plan_without_processes()
                forged = copy.deepcopy(plan["runs"][0]["tasks"][0])
                forged["problem_id"] = problem
                plan["runs"][0]["tasks"].append(forged)

                with mock.patch.object(
                    migrate_six_stage_layout,
                    "_candidate_processes",
                    return_value=(),
                ):
                    with self.assertRaisesRegex(
                        migrate_six_stage_layout.SixStageMigrationError,
                        pattern,
                    ):
                        migrate_six_stage_layout.apply_migration(
                            self.repo,
                            plan,
                        )
                self.assertEqual(self.repository_hashes(), before)
                self.assertFalse(
                    any(
                        self.repo.joinpath("runs").glob(
                            ".six-stage-migration-*"
                        )
                    )
                )

    def test_apply_rejects_omitted_source_manifest_task(self) -> None:
        before = self.repository_hashes()
        plan = self.plan_without_processes()
        plan["runs"][0]["tasks"] = []

        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=(),
        ):
            with self.assertRaisesRegex(
                migrate_six_stage_layout.SixStageMigrationError,
                "tasks do not match source manifest",
            ):
                migrate_six_stage_layout.apply_migration(self.repo, plan)

        self.assertEqual(self.repository_hashes(), before)
        self.assertEqual(
            json.loads((self.run / "run.json").read_text())["schema_version"],
            2,
        )

    def test_apply_refuses_active_codex_audit_klean_and_pipeline_processes(
        self,
    ) -> None:
        before = self.repository_hashes()
        active = (
            (101, ("codex", "exec", "--", RUN_ID)),
            (102, ("python3", "docker/audit/run_task.sh", RUN_ID, PROBLEM)),
            (103, ("bash", "docker/klean/generate_task.sh", RUN_ID, PROBLEM)),
            (104, ("python3", "tools/run_pipeline.py", "run", RUN_ID)),
        )
        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=active,
        ):
            blocked_plan = migrate_six_stage_layout.plan_migration(
                self.repo,
                [RUN_ID],
            )
        self.assertEqual(
            {blocker["process_kind"] for blocker in blocked_plan["blockers"]},
            {"codex", "audit", "klean", "pipeline"},
        )
        self.assertEqual(self.repository_hashes(), before)

        plan = self.plan_without_processes()
        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=active,
        ):
            with self.assertRaisesRegex(
                migrate_six_stage_layout.SixStageMigrationError,
                "active",
            ):
                migrate_six_stage_layout.apply_migration(self.repo, plan)
        self.assertEqual(self.repository_hashes(), before)

    def test_dry_run_ignores_unrelated_keyword_named_tool_paths(
        self,
    ) -> None:
        unrelated = (
            (
                105,
                (
                    "python3",
                    (
                        "/tmp/klean-tools/unrelated_report.py"
                    ),
                    RUN_ID,
                ),
            ),
            (
                106,
                (
                    "python3",
                    "/tmp/pipeline-tools/unrelated_report.py",
                    RUN_ID,
                ),
            ),
        )

        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=unrelated,
        ):
            plan = migrate_six_stage_layout.plan_migration(
                self.repo,
                [RUN_ID],
            )

        self.assertEqual(plan["blockers"], [])

    def test_realistic_post_exec_runner_argv_is_classified(self) -> None:
        active = (
            (
                201,
                ("python3", "tools/stage4_runner.py", RUN_ID, PROBLEM),
            ),
            (
                202,
                ("python3", "tools/audit_contract.py", RUN_ID, PROBLEM),
            ),
            (
                203,
                ("python3", "tools/stage3_runner.py", RUN_ID, PROBLEM),
            ),
            (
                204,
                ("python3", "tools/run_pipeline.py", "run", RUN_ID),
            ),
        )
        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=active,
        ):
            plan = migrate_six_stage_layout.plan_migration(
                self.repo,
                [RUN_ID],
            )

        self.assertEqual(
            {
                blocker["pid"]: blocker["process_kind"]
                for blocker in plan["blockers"]
            },
            {
                201: "klean",
                202: "audit",
                203: "codex",
                204: "pipeline",
            },
        )
        self.assertEqual(
            migrate_six_stage_layout._process_kind(
                (
                    "python3",
                    "tools/stage4_runner.py",
                    "stage4_runner.py",
                    PROBLEM,
                ),
                ["stage4_runner.py"],
            ),
            "klean",
        )

    def test_active_process_run_matching_uses_exact_arguments(self) -> None:
        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=(
                (
                    205,
                    ("python3", "tools/stage4_runner.py", "run-10", PROBLEM),
                ),
            ),
        ):
            blockers = migrate_six_stage_layout._active_process_blockers(
                ["run-1"]
            )

        self.assertEqual(blockers, [])

    def test_cli_dry_run_reports_blocker_but_apply_refuses_it(self) -> None:
        active = (
            (101, ("python3", "tools/run_pipeline.py", "run", RUN_ID)),
        )
        output = io.StringIO()
        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=active,
        ), redirect_stdout(output):
            status = migrate_six_stage_layout.main(
                [
                    "--repo",
                    str(self.repo),
                    "--dry-run",
                    RUN_ID,
                ]
            )
        self.assertEqual(status, 0)
        self.assertEqual(
            json.loads(output.getvalue())["blockers"][0]["process_kind"],
            "pipeline",
        )

        error = io.StringIO()
        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=active,
        ), redirect_stderr(error):
            status = migrate_six_stage_layout.main(
                [
                    "--repo",
                    str(self.repo),
                    "--apply",
                    RUN_ID,
                ]
            )
        self.assertEqual(status, 2)
        self.assertIn("active", error.getvalue())
        self.assertEqual(
            json.loads((self.run / "run.json").read_text())["schema_version"],
            2,
        )

    def test_cli_retry_reports_validated_recovery_as_complete(self) -> None:
        plan = self.plan_without_processes()
        self.crash_apply_at(plan, "after-publication-validation")
        output = io.StringIO()
        error = io.StringIO()
        report = self.repo / "recovered-result.json"

        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=(),
        ), redirect_stdout(output), redirect_stderr(error):
            status = migrate_six_stage_layout.main(
                [
                    "--repo",
                    str(self.repo),
                    "--apply",
                    RUN_ID,
                    "--report",
                    str(report),
                ]
            )

        self.assertEqual(status, 0)
        self.assertEqual(error.getvalue(), "")
        result = json.loads(output.getvalue())
        self.assertEqual(result["mode"], "apply")
        self.assertEqual(result["status"], "COMPLETE")
        self.assertEqual(result["recovery"], "COMPLETED")
        self.assertEqual(result["runs"], [RUN_ID])
        self.assertEqual(json.loads(report.read_text()), result)
        self.assertFalse(
            (
                self.repo
                / "runner-state/.six-stage-migration-transaction.json"
            ).exists()
        )

    def test_live_pipeline_process_blocks_apply(self) -> None:
        before = self.repository_hashes()
        process = subprocess.Popen(
            [
                sys.executable,
                "-c",
                "import time; time.sleep(30)",
                "tools/run_pipeline.py",
                RUN_ID,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            plan = migrate_six_stage_layout.plan_migration(
                self.repo,
                [RUN_ID],
            )

            self.assertIn(
                process.pid,
                [blocker["pid"] for blocker in plan["blockers"]],
            )
            with self.assertRaisesRegex(
                migrate_six_stage_layout.SixStageMigrationError,
                "active pipeline process",
            ):
                migrate_six_stage_layout.apply_migration(self.repo, plan)
            self.assertEqual(self.repository_hashes(), before)
        finally:
            process.terminate()
            process.wait(timeout=5)

    def test_apply_rejects_source_changed_after_planning(self) -> None:
        plan = self.plan_without_processes()
        evidence = self.task / "03-klean-generation/generations/001/target.lean"
        evidence.write_bytes(evidence.read_bytes() + b"-- changed\n")
        changed = self.repository_hashes()

        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=(),
        ):
            with self.assertRaisesRegex(
                migrate_six_stage_layout.SixStageMigrationError,
                "changed after planning",
            ):
                migrate_six_stage_layout.apply_migration(self.repo, plan)

        self.assertEqual(self.repository_hashes(), changed)
        self.assertEqual(
            json.loads((self.run / "run.json").read_text())["schema_version"],
            2,
        )

    def test_recovery_rolls_back_interrupted_multi_run_publication(self) -> None:
        self.clone_run()
        run_ids = [RUN_ID, SECOND_RUN_ID]
        before = self.hashes_for_runs(run_ids)
        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=(),
        ):
            plan = migrate_six_stage_layout.plan_migration(
                self.repo,
                run_ids,
            )

        self.crash_apply_at(plan, "after-run-exchange", occurrence=2)

        journal = (
            self.repo
            / "runner-state/.six-stage-migration-transaction.json"
        )
        self.assertTrue(journal.is_file())
        migrate_six_stage_layout.recover_transaction(self.repo)

        self.assertEqual(self.hashes_for_runs(run_ids), before)
        self.assertFalse(journal.exists())
        self.assertFalse(
            any(self.repo.joinpath("runs").glob(".six-stage-migration-*"))
        )
        self.assertFalse(
            any(
                self.repo.joinpath("runner-state").glob(
                    ".six-stage-migration-*"
                )
            )
        )

    def test_active_journal_run_blocks_recovery_before_mutation(self) -> None:
        plan = self.plan_without_processes()
        self.crash_apply_at(plan, "after-run-exchange")
        journal = (
            self.repo
            / "runner-state/.six-stage-migration-transaction.json"
        )
        before = pipeline_contract.sha256_tree(self.repo)
        active = (
            (301, ("python3", "tools/run_pipeline.py", "run", RUN_ID)),
        )

        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=active,
        ):
            with self.assertRaisesRegex(
                migrate_six_stage_layout.SixStageMigrationError,
                "active pipeline process",
            ):
                migrate_six_stage_layout.recover_transaction(self.repo)

        self.assertEqual(pipeline_contract.sha256_tree(self.repo), before)
        self.assertTrue(journal.is_file())

    def test_recovery_replays_crash_after_backup_tombstone_rename(
        self,
    ) -> None:
        plan = self.plan_without_processes()
        self.crash_apply_at(plan, "after-backup-tombstone-rename")
        journal_path = (
            self.repo
            / "runner-state/.six-stage-migration-transaction.json"
        )
        journal = json.loads(journal_path.read_text())
        tombstone = Path(journal["entries"][0]["tombstone"])

        self.assertEqual(journal["phase"], "VALIDATED")
        self.assertTrue(tombstone.is_dir())
        self.assertFalse(Path(journal["entries"][0]["backup"]).exists())
        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=(),
        ):
            migrate_six_stage_layout.recover_transaction(self.repo)

        self.assertFalse(journal_path.exists())
        self.assertFalse(tombstone.exists())
        self.assertEqual(
            json.loads((self.run / "run.json").read_text())["schema_version"],
            3,
        )

    def test_recovery_replays_partial_tombstone_deletion(self) -> None:
        plan = self.plan_without_processes()
        self.crash_during_tombstone_deletion(plan)
        journal_path = (
            self.repo
            / "runner-state/.six-stage-migration-transaction.json"
        )
        journal = json.loads(journal_path.read_text())
        tombstone = Path(journal["entries"][0]["tombstone"])

        self.assertTrue(tombstone.is_dir())
        self.assertNotEqual(
            pipeline_contract.sha256_tree(tombstone),
            journal["entries"][0]["original_sha256"],
        )
        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=(),
        ):
            migrate_six_stage_layout.recover_transaction(self.repo)

        self.assertFalse(journal_path.exists())
        self.assertFalse(tombstone.exists())
        self.assertEqual(
            json.loads((self.run / "run.json").read_text())["schema_version"],
            3,
        )

    def test_recovery_fsyncs_parent_after_deleted_tombstone(self) -> None:
        plan = self.plan_without_processes()
        self.crash_apply_at(plan, "after-tombstone-deletion")
        journal_path = (
            self.repo
            / "runner-state/.six-stage-migration-transaction.json"
        )
        journal = json.loads(journal_path.read_text())
        entry = journal["entries"][0]
        backup = Path(entry["backup"])
        tombstone = Path(entry["tombstone"])
        synced: list[Path] = []
        original_fsync_directory = migrate_six_stage_layout._fsync_directory

        self.assertFalse(backup.exists())
        self.assertFalse(tombstone.exists())

        def observe_fsync_directory(path: Path) -> None:
            synced.append(path)
            original_fsync_directory(path)

        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=(),
        ), mock.patch.object(
            migrate_six_stage_layout,
            "_fsync_directory",
            side_effect=observe_fsync_directory,
        ):
            migrate_six_stage_layout.recover_transaction(self.repo)

        self.assertIn(tombstone.parent, synced)
        self.assertFalse(journal_path.exists())
        self.assertEqual(
            json.loads((self.run / "run.json").read_text())["schema_version"],
            3,
        )

    def test_recovery_finishes_validated_publication(self) -> None:
        plan = self.plan_without_processes()

        self.crash_apply_at(plan, "after-publication-validation")

        journal = (
            self.repo
            / "runner-state/.six-stage-migration-transaction.json"
        )
        self.assertTrue(journal.is_file())
        self.assertEqual(
            json.loads((self.run / "run.json").read_text())["schema_version"],
            3,
        )
        migrate_six_stage_layout.recover_transaction(self.repo)

        self.assertFalse(journal.exists())
        self.assertEqual(
            json.loads((self.run / "run.json").read_text())["schema_version"],
            3,
        )
        self.assertEqual(
            pipeline_contract._read_session_state(self.state)[
                "schema_version"
            ],
            3,
        )
        self.assertFalse(
            any(self.repo.joinpath("runs").glob(".six-stage-migration-*"))
        )
        self.assertFalse(
            any(
                self.repo.joinpath("runner-state").glob(
                    ".six-stage-migration-*"
                )
            )
        )

    def test_apply_recovers_interrupted_transaction_before_new_work(
        self,
    ) -> None:
        plan = self.plan_without_processes()
        self.crash_apply_at(plan, "after-run-exchange")

        with mock.patch.object(
            migrate_six_stage_layout,
            "_candidate_processes",
            return_value=(),
        ):
            result = migrate_six_stage_layout.apply_migration(
                self.repo,
                plan,
            )

        self.assertEqual(result["status"], "COMPLETE")
        self.assertEqual(
            json.loads((self.run / "run.json").read_text())["schema_version"],
            3,
        )
        self.assertFalse(
            (
                self.repo
                / "runner-state/.six-stage-migration-transaction.json"
            ).exists()
        )


if __name__ == "__main__":
    unittest.main()
