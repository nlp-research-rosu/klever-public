import hashlib
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
from dataclasses import FrozenInstanceError
from pathlib import Path
from unittest import mock

from tools import (
    legacy_migration,
    pipeline_contract,
    run_pipeline,
    usage_accounting,
)


BARE_RUN = "codex-gpt-5.6-sol-xhigh-bare"
SEMANTICS_RUN = "codex-gpt-5.6-sol-xhigh-semantics"
BARE_SUCCESS = "0-has-close-elements"
BARE_CONCERNS = "1-separate-paren-groups"
BARE_FAIL = "2-truncate-number"
BARE_INCOMPLETE = "98-count-upper"
SEMANTICS_SUCCESS = "0-has-close-elements"
SEMANTICS_TIMEOUT = "148-bf"

SESSION_IDS = {
    (BARE_RUN, BARE_SUCCESS): "00000000-0000-4000-8000-000000000001",
    (BARE_RUN, BARE_CONCERNS): "00000000-0000-4000-8000-000000000005",
    (BARE_RUN, BARE_FAIL): "00000000-0000-4000-8000-000000000006",
    (BARE_RUN, BARE_INCOMPLETE): "00000000-0000-4000-8000-000000000002",
    (SEMANTICS_RUN, SEMANTICS_SUCCESS):
        "00000000-0000-4000-8000-000000000003",
    (SEMANTICS_RUN, SEMANTICS_TIMEOUT):
        "00000000-0000-4000-8000-000000000004",
}


class LegacyMigrationFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name)
        prompts = self.repo / "prompts"
        prompts.mkdir()
        self.instruction_prompts = {
            "bare": b"fixed bare instruction prompt\n",
            "semantics": b"fixed semantics instruction prompt\n",
        }
        (prompts / "bare.md").write_bytes(self.instruction_prompts["bare"])
        (prompts / "with-semantics.md").write_bytes(
            self.instruction_prompts["semantics"]
        )
        self.source_specs = (
            legacy_migration.LegacyRunSpec(
                run_id=BARE_RUN,
                condition="bare",
                expected_tasks=4,
                audit_run_id=BARE_RUN,
                expected_audit_distribution=(1, 1, 1),
            ),
            legacy_migration.LegacyRunSpec(
                run_id=SEMANTICS_RUN,
                condition="semantics",
                expected_tasks=2,
                audit_run_id=None,
                expected_audit_distribution=(0, 0, 0),
            ),
        )
        self.write_task(BARE_RUN, BARE_SUCCESS, condition="bare")
        self.write_task(BARE_RUN, BARE_CONCERNS, condition="bare")
        self.write_task(BARE_RUN, BARE_FAIL, condition="bare")
        self.write_task(
            BARE_RUN,
            BARE_INCOMPLETE,
            condition="bare",
            include_manifest=False,
        )
        self.write_task(
            SEMANTICS_RUN,
            SEMANTICS_SUCCESS,
            condition="semantics",
        )
        self.write_task(
            SEMANTICS_RUN,
            SEMANTICS_TIMEOUT,
            condition="semantics",
            timed_out=True,
        )
        self.write_audit(BARE_SUCCESS, verdict="PASS", legitimacy="LEGIT")
        self.write_audit(
            BARE_CONCERNS,
            verdict="CONCERNS",
            legitimacy="LEGIT",
        )
        self.write_audit(
            BARE_FAIL,
            verdict="FAIL",
            legitimacy="NOT_LEGIT",
        )

    def scan(self) -> legacy_migration.MigrationPlan:
        return legacy_migration.scan_legacy_sources(
            self.repo,
            _source_specs=self.source_specs,
        )

    def write_json(self, path: Path, document: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")

    def write_task(
        self,
        run_id: str,
        problem: str,
        *,
        condition: str,
        include_manifest: bool = True,
        timed_out: bool = False,
    ) -> Path:
        task = self.repo / "runs" / run_id / problem
        task.mkdir(parents=True)
        for relative, content in (
            ("prompt.py", "def candidate(value):\n    pass\n"),
            ("py2mpy.py", "# fixed translator\n"),
            ("solution.py", "def candidate(value):\n    return value\n"),
            ("solution.mpy", "candidate(value) { return value; }\n"),
            ("verification.k", "module VERIFICATION endmodule\n"),
            ("spec.k", "module SPEC endmodule\n"),
            ("prove.sh", "#!/bin/sh\nexit 0\n"),
            ("codex-output.log", "fixed generation transcript\n"),
        ):
            (task / relative).write_text(content)
        if condition == "bare":
            (task / "semantic.k").write_text("module SEMANTIC endmodule\n")
        else:
            semantics = task / "reference-semantics"
            semantics.mkdir()
            (semantics / "semantics.k").write_text(
                "module REFERENCE-SEMANTICS endmodule\n"
            )

        if not timed_out:
            (task / "codex-last.txt").write_text(
                "Fixed completion summary.\n\n"
                "RESULT: KPROVE_PASSED — all fixed claims closed.\n"
            )
        self.write_json(
            task / "metrics.json",
            {
                "agent": "codex",
                "model": "gpt-5.6-sol",
                "effort": "xhigh",
                "timeout_s": 3600,
                "start_epoch": 1000,
                "end_epoch": 4600 if timed_out else 1123,
                "duration_s": 3600 if timed_out else 123,
                "exit_code": 124 if timed_out else 0,
                "timed_out": timed_out,
                "mem_peak_bytes": 123456,
            },
        )
        if include_manifest:
            inputs = {
                "instruction_prompt": (
                    "bare.md" if condition == "bare" else "with-semantics.md"
                ),
                "instruction_prompt_sha256": hashlib.sha256(
                    self.instruction_prompts[condition]
                ).hexdigest(),
                "problem_prompt_sha256": "2" * 64,
                "translator_sha256": "3" * 64,
            }
            if condition == "semantics":
                inputs["reference_semantics_sha256"] = "4" * 64
            self.write_json(
                task / "run-input.json",
                {
                    "schema_version": 1,
                    "config": run_id,
                    "problem_id": problem,
                    "condition": {
                        "name": condition,
                        "kit": False,
                        "semantics": condition == "semantics",
                    },
                    "inputs": inputs,
                },
            )

        trace = task / "codex-trace/2026/07/24"
        trace.mkdir(parents=True)
        events = (
            {
                "timestamp": "2026-07-24T12:00:00.000Z",
                "type": "session_meta",
                "payload": {
                    "id": SESSION_IDS[(run_id, problem)],
                    "session_id": SESSION_IDS[(run_id, problem)],
                    "cli_version": "0.144.6",
                },
            },
            {
                "timestamp": "2026-07-24T12:01:00.000Z",
                "type": "event_msg",
                "payload": {
                    "type": "token_count",
                    "info": {
                        "total_token_usage": {
                            "input_tokens": 100,
                            "cached_input_tokens": 40,
                            "output_tokens": 25,
                            "reasoning_output_tokens": 10,
                            "total_tokens": 125,
                        }
                    },
                },
            },
        )
        (trace / "rollout.jsonl").write_text(
            "".join(json.dumps(event, sort_keys=True) + "\n" for event in events)
        )
        return task

    def write_audit(
        self,
        problem: str,
        *,
        verdict: str,
        legitimacy: str,
    ) -> Path:
        audit = self.repo / "audits" / BARE_RUN / problem
        evidence = audit / "evidence"
        trace = audit / "codex-trace/2026/07/24"
        evidence.mkdir(parents=True)
        trace.mkdir(parents=True)
        (audit / "REVIEW.md").write_text(
            "# Fixed audit\n\nAll seven audit stages completed.\n\n"
            f"VERDICT: {verdict}\n"
            f"LEGITIMACY: {legitimacy}\n"
        )
        (audit / "prompt.txt").write_text("fixed audit prompt\n")
        (audit / "codex-output.log").write_text("fixed audit transcript\n")
        (audit / "codex-last.txt").write_text("fixed audit summary\n")
        (evidence / "commands.log").write_text("kprove spec.k\n#Top\n")
        self.write_json(
            audit / "audit-input.json",
            {
                "config": BARE_RUN,
                "generation_config": BARE_RUN,
                "problem_id": problem,
                "condition": "bare",
            },
        )
        self.write_json(
            audit / "metrics.json",
            {
                "agent": "codex",
                "model": "gpt-5.6-sol",
                "effort": "xhigh",
                "timeout_s": 3600,
                "start_epoch": 2000,
                "end_epoch": 2010,
                "duration_s": 10,
                "exit_code": 0,
                "model_exit_code": 0,
                "harness_exit_code": 0,
                "timed_out": False,
                "mem_peak_bytes": 654321,
            },
        )
        self.write_json(
            audit / "verdict.json",
            {
                "audit_status": "COMPLETE",
                "error": None,
                "legitimacy": legitimacy,
                "verdict": verdict,
            },
        )
        audit_events = (
            {
                "type": "session_meta",
                "payload": {
                    "id": "00000000-0000-4000-8000-000000000011",
                    "cli_version": "0.144.6",
                },
            },
            {
                "type": "event_msg",
                "payload": {
                    "type": "token_count",
                    "info": {
                        "total_token_usage": {
                            "input_tokens": 50,
                            "cached_input_tokens": 20,
                            "output_tokens": 15,
                            "reasoning_output_tokens": 5,
                            "total_tokens": 65,
                        }
                    },
                },
            },
        )
        (trace / "rollout.jsonl").write_text(
            "".join(
                json.dumps(event, sort_keys=True) + "\n"
                for event in audit_events
            )
        )
        return audit


class LegacyMigrationStagingTests(LegacyMigrationFixture):
    def stage(self, transaction_id: str = "test-transaction"):
        plan = self.scan()
        staged = legacy_migration.stage_migration(
            self.repo,
            plan,
            transaction_id,
        )
        return plan, staged

    def test_stages_successful_task_as_compact_six_stage_run(self) -> None:
        source = self.repo / "runs" / BARE_RUN / BARE_SUCCESS
        compiled = source / "verification-kompiled/nested"
        compiled.mkdir(parents=True)
        (compiled / "cache.bin").write_bytes(b"regenerable")
        plan, staged = self.stage()

        staged_run = staged.runs_root / BARE_RUN
        task = staged_run / "tasks" / BARE_SUCCESS
        stage = task / "01-k-proof"
        invocation = stage / "invocations/001-initial"
        state = staged.state_root / BARE_RUN / BARE_SUCCESS

        self.assertEqual(
            staged_run,
            self.repo
            / f"runs/.legacy-migration-{staged.transaction_id}/{BARE_RUN}",
        )
        self.assertEqual(
            state,
            self.repo
            / (
                "runner-state/"
                f".legacy-migration-{staged.transaction_id}/"
                f"{BARE_RUN}/{BARE_SUCCESS}"
            ),
        )
        for name in pipeline_contract.STAGE_NAMES:
            self.assertTrue((task / name).is_dir(), name)
        for relative in (
            "01-k-proof/workspace",
            "01-k-proof/invocations/001-initial",
            "02-k-audit/executions",
            "03-lemma-discovery/workspace",
            "03-lemma-discovery/invocations",
            "04-klean-generation/generations",
            "05-lean-proof/workspace",
            "05-lean-proof/invocations",
            "06-lean-audit/executions",
        ):
            self.assertTrue((task / relative).is_dir(), relative)
        for relative in (
            "03-lemma-discovery/workspace",
            "03-lemma-discovery/invocations",
            "04-klean-generation/generations",
            "05-lean-proof/workspace",
            "05-lean-proof/invocations",
            "06-lean-audit/executions",
        ):
            self.assertEqual(list((task / relative).iterdir()), [])
        self.assertFalse(
            any(
                path.name.endswith("-kompiled")
                for path in staged_run.rglob("*")
            )
        )

        self.assertEqual(
            (stage / "workspace/prompt.py").read_bytes(),
            (source / "prompt.py").read_bytes(),
        )
        self.assertFalse((stage / "workspace/metrics.json").exists())
        self.assertFalse((stage / "workspace/run-input.json").exists())
        self.assertEqual(
            (invocation / "legacy-metrics.json").read_bytes(),
            (source / "metrics.json").read_bytes(),
        )
        self.assertEqual(
            (invocation / "legacy-run-input.json").read_bytes(),
            (source / "run-input.json").read_bytes(),
        )
        self.assertEqual(
            (invocation / "codex-output.log").read_bytes(),
            (source / "codex-output.log").read_bytes(),
        )
        self.assertEqual(
            (invocation / "codex-last.txt").read_bytes(),
            (source / "codex-last.txt").read_bytes(),
        )
        self.assertEqual(
            (invocation / "prompt.txt").read_bytes(),
            self.instruction_prompts["bare"],
        )

        invocation_document = json.loads(
            (invocation / "invocation.json").read_text()
        )
        self.assertEqual(invocation_document["status"], "SUCCEEDED")
        self.assertEqual(invocation_document["kind"], "initial")
        self.assertEqual(invocation_document["legacy_import"], True)
        self.assertEqual(
            invocation_document["image_id"],
            "UNKNOWN_LEGACY_IMAGE",
        )
        self.assertEqual(invocation_document["oom_killed"], "UNKNOWN")
        self.assertEqual(
            invocation_document["preflight"],
            "NOT_APPLICABLE_LEGACY",
        )
        self.assertEqual(
            invocation_document["result_marker"],
            "KPROVE_PASSED",
        )
        self.assertRegex(
            invocation_document["source_tree_sha256"],
            r"^[0-9a-f]{64}$",
        )
        self.assertEqual(
            invocation_document["retained_workspace_sha256"],
            pipeline_contract.sha256_tree(stage / "workspace"),
        )
        self.assertEqual(
            json.loads((stage / "result.json").read_text())["status"],
            "SUCCEEDED",
        )
        self.assertEqual(
            json.loads((invocation / "usage.json").read_text())["status"],
            "COMPLETE",
        )

        rollout = state / "codex-home/sessions/2026/07/24/rollout.jsonl"
        source_rollout = source / "codex-trace/2026/07/24/rollout.jsonl"
        self.assertTrue(rollout.is_file())
        self.assertEqual(rollout.read_bytes(), source_rollout.read_bytes())
        self.assertNotEqual(rollout.stat().st_ino, source_rollout.stat().st_ino)
        session = json.loads((state / "session.json").read_text())
        self.assertEqual(
            session["session_id"],
            SESSION_IDS[(BARE_RUN, BARE_SUCCESS)],
        )
        home_stat = (state / "codex-home").stat()
        self.assertEqual(session["codex_home_device"], home_stat.st_dev)
        self.assertEqual(session["codex_home_inode"], home_stat.st_ino)
        self.assertEqual(stat.S_IMODE(state.stat().st_mode), 0o700)
        self.assertEqual(
            [
                json.loads(line)["event"]
                for line in (
                    state / "stage-ledger.jsonl"
                ).read_text().splitlines()
            ],
            ["legacy_invocation_imported", "stage_output_selected"],
        )

        migration = json.loads((task / "migration.json").read_text())
        self.assertEqual(migration["status"], "SUCCEEDED")
        self.assertEqual(migration["input_provenance"], "COMPLETE")
        self.assertEqual(
            migration["retained_workspace_sha256"],
            invocation_document["retained_workspace_sha256"],
        )
        self.assertEqual(
            migration["omitted"][0]["relative_path"],
            "verification-kompiled",
        )
        validation = legacy_migration.validate_staged_migration(staged, plan)
        self.assertEqual(validation["tasks"], 6)
        self.assertEqual(validation["succeeded"], 5)

    def test_imports_complete_audit_tree_byte_identically_and_binds_usage(
        self,
    ) -> None:
        source = self.repo / "audits" / BARE_RUN / BARE_SUCCESS
        original_hashes = {
            path.relative_to(source).as_posix(): hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
            for path in source.rglob("*")
            if path.is_file()
        }

        _plan, staged = self.stage("immutable-audit")
        task = (
            staged.runs_root
            / BARE_RUN
            / "tasks"
            / BARE_SUCCESS
        )
        execution = task / "02-k-audit/executions/001"
        imported_files = {
            path.relative_to(execution).as_posix()
            for path in execution.rglob("*")
            if path.is_file()
        }

        self.assertEqual(
            imported_files,
            set(original_hashes) | {"usage.json"},
        )
        for relative, expected_hash in original_hashes.items():
            with self.subTest(relative=relative):
                imported = execution / relative
                self.assertEqual(
                    hashlib.sha256(imported.read_bytes()).hexdigest(),
                    expected_hash,
                )
                self.assertEqual(
                    imported.read_bytes(),
                    (source / relative).read_bytes(),
                )
        usage = json.loads((execution / "usage.json").read_text())
        self.assertEqual(
            usage["source_trace_sha256"],
            usage_accounting.sha256_tree(execution / "codex-trace"),
        )
        selected = json.loads(
            (task / "02-k-audit/selected.json").read_text()
        )
        self.assertEqual(selected["status"], "PASS")
        migration = json.loads((task / "migration.json").read_text())
        self.assertEqual(
            migration["audit_import"]["original_path"],
            f"audits/{BARE_RUN}/{BARE_SUCCESS}",
        )
        self.assertNotIn("migration.json", imported_files)

    def test_imported_audits_preserve_eligibility_and_blocking(self) -> None:
        plan, staged = self.stage("audit-eligibility")
        validation = legacy_migration.validate_staged_migration(
            staged,
            plan,
        )
        self.assertEqual(
            {
                key: validation[key]
                for key in (
                    "pass",
                    "concerns",
                    "fail",
                    "blocked",
                    "eligible",
                )
            },
            {
                "pass": 1,
                "concerns": 1,
                "fail": 1,
                "blocked": 1,
                "eligible": 2,
            },
        )

        (self.repo / "runs" / BARE_RUN).rename(
            self.repo / "legacy-bare-source"
        )
        (staged.runs_root / BARE_RUN).rename(
            self.repo / "runs" / BARE_RUN
        )
        (staged.state_root / BARE_RUN).rename(
            self.repo / "runner-state" / BARE_RUN
        )

        self.assertEqual(
            run_pipeline.inspect_problem(
                self.repo,
                BARE_RUN,
                BARE_SUCCESS,
            )["next_stage"],
            "03-lemma-discovery",
        )
        self.assertEqual(
            run_pipeline.inspect_problem(
                self.repo,
                BARE_RUN,
                BARE_CONCERNS,
            )["next_stage"],
            "03-lemma-discovery",
        )
        self.assertEqual(
            run_pipeline.inspect_problem(
                self.repo,
                BARE_RUN,
                BARE_FAIL,
            )["state"],
            "K_AUDIT_FAIL",
        )
        self.assertEqual(
            run_pipeline.inspect_problem(
                self.repo,
                BARE_RUN,
                BARE_INCOMPLETE,
            )["state"],
            "BLOCKED_INPUT_PROVENANCE",
        )

    def test_writes_exact_usage_summaries_and_leaves_semantics_stage2_empty(
        self,
    ) -> None:
        _plan, staged = self.stage("usage-summaries")
        bare = staged.runs_root / BARE_RUN
        bare_summary = json.loads(
            (bare / "usage-summary.json").read_text()
        )
        self.assertEqual(
            bare_summary["stage_subtotals"]["01-k-proof"]["total_tokens"],
            500,
        )
        self.assertEqual(
            bare_summary["stage_subtotals"]["02-k-audit"]["total_tokens"],
            195,
        )
        self.assertEqual(bare_summary["totals"]["total_tokens"], 695)
        self.assertEqual(
            bare_summary["task_subtotals"][BARE_SUCCESS]["total_tokens"],
            190,
        )
        self.assertEqual(
            bare_summary["runtime"]["stage_agent_seconds"]["01-k-proof"],
            492,
        )
        self.assertEqual(
            bare_summary["runtime"]["stage_agent_seconds"]["02-k-audit"],
            30,
        )

        semantics = staged.runs_root / SEMANTICS_RUN
        for task in (semantics / "tasks").iterdir():
            self.assertEqual(
                list((task / "02-k-audit/executions").iterdir()),
                [],
            )
        semantics_summary = json.loads(
            (semantics / "usage-summary.json").read_text()
        )
        self.assertEqual(
            semantics_summary["stage_subtotals"]["02-k-audit"],
            dict.fromkeys(usage_accounting.TOKEN_FIELDS, 0),
        )

    def test_run_manifest_records_current_and_legacy_cli_provenance(
        self,
    ) -> None:
        _plan, staged = self.stage("separate-cli-provenance")
        run = staged.runs_root / BARE_RUN
        run_manifest = json.loads((run / "run.json").read_text())
        invocation = json.loads(
            (
                run
                / "tasks"
                / BARE_SUCCESS
                / "01-k-proof/invocations/001-initial/invocation.json"
            ).read_text()
        )

        self.assertNotIn("runtime", run_manifest)
        self.assertEqual(
            {
                name: run_manifest["timeouts"][name]
                for name in ("lemma_initial_s", "lemma_total_s")
            },
            {
                "lemma_initial_s": 1200,
                "lemma_total_s": 1200,
            },
        )
        self.assertEqual(
            run_manifest["import_tooling"],
            {
                "current_codex_cli_version": (
                    pipeline_contract.CODEX_CLI_VERSION
                ),
                "pipeline_schema_version": pipeline_contract.SCHEMA_VERSION,
            },
        )
        self.assertEqual(invocation["codex_cli_version"], "0.144.6")
        self.assertEqual(
            invocation["codex_cli_version"],
            run_manifest["import_tooling"]["current_codex_cli_version"],
        )

    def test_hidden_staged_run_roots_match_native_private_mode(self) -> None:
        _plan, staged = self.stage("private-run-mode")

        for run_id in (BARE_RUN, SEMANTICS_RUN):
            self.assertEqual(
                stat.S_IMODE((staged.runs_root / run_id).stat().st_mode),
                0o700,
            )

    def test_stages_timeout_for_resume_and_blocks_incomplete_input(self) -> None:
        plan, staged = self.stage("timeout-and-block")

        timeout_task = (
            staged.runs_root
            / SEMANTICS_RUN
            / "tasks"
            / SEMANTICS_TIMEOUT
        )
        timeout_invocation = (
            timeout_task / "01-k-proof/invocations/001-initial"
        )
        timeout_state = (
            staged.state_root / SEMANTICS_RUN / SEMANTICS_TIMEOUT
        )
        timeout_document = json.loads(
            (timeout_invocation / "invocation.json").read_text()
        )
        self.assertEqual(timeout_document["status"], "TIMEOUT")
        self.assertEqual(timeout_document["allocation_s"], 3600)
        self.assertEqual(
            timeout_document["session_id"],
            SESSION_IDS[(SEMANTICS_RUN, SEMANTICS_TIMEOUT)],
        )
        self.assertEqual(timeout_document["resumable"], True)
        self.assertEqual(
            timeout_document["expected_absences"],
            ["codex-last.txt", "result.json"],
        )
        self.assertFalse(
            (timeout_task / "01-k-proof/result.json").exists()
        )
        self.assertFalse((timeout_invocation / "codex-last.txt").exists())
        self.assertEqual(
            pipeline_contract._read_session_state(timeout_state)["session_id"],
            timeout_document["session_id"],
        )

        incomplete = (
            staged.runs_root / BARE_RUN / "tasks" / BARE_INCOMPLETE
        )
        incomplete_manifest = json.loads(
            (incomplete / "task.json").read_text()
        )
        self.assertEqual(
            {
                key: incomplete_manifest[key]
                for key in ("input_provenance", "pipeline_block")
            },
            {
                "input_provenance": "INCOMPLETE",
                "pipeline_block": "INPUT_PROVENANCE_INCOMPLETE",
            },
        )
        incomplete_invocation = (
            incomplete / "01-k-proof/invocations/001-initial"
        )
        self.assertFalse(
            (incomplete_invocation / "legacy-run-input.json").exists()
        )
        self.assertFalse((incomplete_invocation / "prompt.txt").exists())
        migration = json.loads((incomplete / "migration.json").read_text())
        self.assertEqual(
            {
                key: migration[key]
                for key in ("input_provenance", "pipeline_block")
            },
            {
                "input_provenance": "INCOMPLETE",
                "pipeline_block": "INPUT_PROVENANCE_INCOMPLETE",
            },
        )

        validation = legacy_migration.validate_staged_migration(staged, plan)
        self.assertEqual(validation["timeout"], 1)
        self.assertEqual(validation["blocked"], 1)

    def test_validation_rejects_tampered_normalized_metrics(self) -> None:
        plan, staged = self.stage("tampered-metrics")
        metrics_path = (
            staged.runs_root
            / BARE_RUN
            / "tasks"
            / BARE_SUCCESS
            / "01-k-proof/invocations/001-initial/metrics.json"
        )
        metrics = json.loads(metrics_path.read_text())
        metrics["duration_s"] += 1
        self.write_json(metrics_path, metrics)

        with self.assertRaisesRegex(
            legacy_migration.LegacyMigrationError,
            "normalized legacy metrics",
        ):
            legacy_migration.validate_staged_migration(staged, plan)

    def test_validation_rejects_non_import_ledger_event(self) -> None:
        plan, staged = self.stage("tampered-ledger")
        ledger_path = (
            staged.state_root
            / BARE_RUN
            / BARE_SUCCESS
            / "stage-ledger.jsonl"
        )
        ledger = [
            json.loads(line)
            for line in ledger_path.read_text().splitlines()
        ]
        ledger[0]["event"] = "invocation_finalized"
        ledger_path.write_text(
            "".join(json.dumps(event) + "\n" for event in ledger)
        )

        with self.assertRaisesRegex(
            legacy_migration.LegacyMigrationError,
            "stage ledger",
        ):
            legacy_migration.validate_staged_migration(staged, plan)

    def test_validation_requires_exact_normalized_documents(self) -> None:
        plan, staged = self.stage("exact-documents")
        task = staged.runs_root / BARE_RUN / "tasks" / BARE_SUCCESS
        state = staged.state_root / BARE_RUN / BARE_SUCCESS
        cases = (
            (
                "result",
                task / "01-k-proof/result.json",
                lambda document: document.update({"unexpected": True}),
                "Stage 1 result",
            ),
            (
                "task",
                task / "task.json",
                lambda document: document["condition"].update(
                    {"name": "semantics"}
                ),
                "task manifest",
            ),
            (
                "session",
                state / "session.json",
                lambda document: document.update(
                    {"source": "01-k-proof/002-timeout-resume"}
                ),
                "session state",
            ),
            (
                "migration",
                task / "migration.json",
                lambda document: document.update(
                    {"stage": "02-k-audit"}
                ),
                "migration manifest",
            ),
        )

        for name, path, mutate, pattern in cases:
            with self.subTest(document=name):
                original = path.read_bytes()
                document = json.loads(original)
                mutate(document)
                path.write_text(json.dumps(document, sort_keys=True) + "\n")
                try:
                    with self.assertRaisesRegex(
                        legacy_migration.LegacyMigrationError,
                        pattern,
                    ):
                        legacy_migration.validate_staged_migration(
                            staged,
                            plan,
                        )
                finally:
                    path.write_bytes(original)


class LegacyMigrationTransactionTests(LegacyMigrationFixture):
    def source_hashes(self) -> dict[str, str]:
        paths = (
            self.repo / "runs" / BARE_RUN,
            self.repo / "runs" / SEMANTICS_RUN,
            self.repo / "audits" / BARE_RUN,
        )
        return {
            path.relative_to(self.repo).as_posix():
                pipeline_contract.sha256_tree(path)
            for path in paths
        }

    def stage(self, transaction_id: str):
        plan = self.scan()
        return plan, legacy_migration.stage_migration(
            self.repo,
            plan,
            transaction_id,
        )

    def expand_fixed_scope_fixture(self) -> None:
        shutil.rmtree(self.repo / "runs")
        shutil.rmtree(self.repo / "audits")
        required = {
            BARE_SUCCESS,
            BARE_CONCERNS,
            BARE_FAIL,
            BARE_INCOMPLETE,
            "136-largest-smallest-integers",
            "117-select-words",
            SEMANTICS_TIMEOUT,
            "151-double-the-difference",
            "156-int-to-mini-roman",
            "162-string-to-md5",
        }
        problem_ids = sorted(
            required
            | {
                f"900-fixture-{index:03d}"
                for index in range(164 - len(required))
            }
        )
        questions = self.repo / "data/questions"
        for problem in problem_ids:
            (questions / problem).mkdir(parents=True)
        incomplete = legacy_migration.PROVENANCE_INCOMPLETE
        timeouts = legacy_migration.EXPECTED_TIMEOUTS
        session_number = 1000
        for run_id, condition in (
            (BARE_RUN, "bare"),
            (SEMANTICS_RUN, "semantics"),
        ):
            for problem in problem_ids:
                SESSION_IDS[(run_id, problem)] = str(
                    uuid.UUID(int=session_number)
                )
                session_number += 1
                self.write_task(
                    run_id,
                    problem,
                    condition=condition,
                    include_manifest=(run_id, problem) not in incomplete,
                    timed_out=(run_id, problem) in timeouts,
                )
                if (
                    run_id == SEMANTICS_RUN
                    and problem
                    in {"151-double-the-difference", "162-string-to-md5"}
                ):
                    (self.repo / "runs" / run_id / problem / "prove.sh").unlink()
        audited = [
            problem
            for problem in problem_ids
            if (BARE_RUN, problem) not in incomplete
        ]
        for index, problem in enumerate(audited):
            if index < 10:
                verdict, legitimacy = "PASS", "LEGIT"
            elif index < 91:
                verdict, legitimacy = "CONCERNS", "LEGIT"
            else:
                verdict, legitimacy = "FAIL", "NOT_LEGIT"
            self.write_audit(
                problem,
                verdict=verdict,
                legitimacy=legitimacy,
            )

    def test_publish_makes_both_runs_visible_as_one_valid_transaction(
        self,
    ) -> None:
        plan, staged = self.stage("publish-success")

        legacy_migration.publish_migration(self.repo, staged, plan)

        self.assertFalse((self.repo / "audits" / BARE_RUN).exists())
        self.assertFalse(
            (self.repo / "runner-state/.legacy-migration-transaction.json")
            .exists()
        )
        self.assertEqual(
            run_pipeline.inspect_problem(
                self.repo, SEMANTICS_RUN, SEMANTICS_SUCCESS
            )["state"],
            "PENDING_K_AUDIT",
        )
        self.assertEqual(
            run_pipeline.inspect_problem(
                self.repo, SEMANTICS_RUN, SEMANTICS_TIMEOUT
            )["state"],
            "PENDING_K_PROOF",
        )
        self.assertEqual(
            run_pipeline.inspect_problem(
                self.repo, BARE_RUN, BARE_INCOMPLETE
            )["state"],
            "BLOCKED_INPUT_PROVENANCE",
        )
        invocation = pipeline_contract.prepare_invocation(
            self.repo,
            SEMANTICS_RUN,
            SEMANTICS_TIMEOUT,
            "01-k-proof",
        )
        self.assertEqual(invocation.name, "002-timeout-resume")
        self.assertEqual(
            invocation.session_id,
            SESSION_IDS[(SEMANTICS_RUN, SEMANTICS_TIMEOUT)],
        )

    def test_failure_at_each_publication_boundary_rolls_back_exactly(
        self,
    ) -> None:
        boundaries = (
            "after-run-quarantine",
            "after-audit-quarantine",
            "after-run-publish",
            "after-state-publish",
            "after-post-publish-validation",
        )
        for index, boundary in enumerate(boundaries):
            with self.subTest(boundary=boundary):
                if index:
                    legacy_migration.recover_transaction(self.repo)
                original_hashes = self.source_hashes()
                plan, staged = self.stage(f"rollback-{index}")

                def fail(observed: str) -> None:
                    if observed == boundary:
                        raise RuntimeError(f"injected at {boundary}")

                with mock.patch.object(
                    legacy_migration,
                    "_publication_boundary",
                    side_effect=fail,
                ):
                    with self.assertRaisesRegex(RuntimeError, boundary):
                        legacy_migration.publish_migration(
                            self.repo, staged, plan
                        )

                self.assertEqual(self.source_hashes(), original_hashes)
                for run_id in (BARE_RUN, SEMANTICS_RUN):
                    self.assertFalse(
                        (self.repo / "runs" / run_id / "run.json").exists()
                    )
                    self.assertFalse(
                        (self.repo / "runner-state" / run_id).exists()
                    )
                journal = json.loads(
                    (
                        self.repo
                        / "runner-state/.legacy-migration-transaction.json"
                    ).read_text()
                )
                self.assertEqual(journal["phase"], "ROLLBACK_SUCCEEDED")
                self.assertEqual(
                    journal["rollback"],
                    {"attempted": True, "succeeded": True},
                )

    def test_refuses_active_container_or_pipeline_process(self) -> None:
        plan = self.scan()
        source = self.repo / "runs" / BARE_RUN / BARE_SUCCESS
        with mock.patch.object(
            legacy_migration,
            "_docker_bind_mount_sources",
            return_value=(source,),
        ), mock.patch.object(
            legacy_migration,
            "_pipeline_processes",
            return_value=(),
        ):
            with self.assertRaisesRegex(
                legacy_migration.LegacyMigrationError,
                "container",
            ):
                legacy_migration.assert_sources_idle(self.repo, plan)

        with mock.patch.object(
            legacy_migration,
            "_docker_bind_mount_sources",
            return_value=(),
        ), mock.patch.object(
            legacy_migration,
            "_pipeline_processes",
            return_value=(
                (
                    999999,
                    (
                        "python3",
                        "tools/run_pipeline.py",
                        "run",
                        SEMANTICS_RUN,
                    ),
                ),
            ),
        ):
            with self.assertRaisesRegex(
                legacy_migration.LegacyMigrationError,
                "process",
            ):
                legacy_migration.assert_sources_idle(self.repo, plan)

    def test_recovery_removes_unpublished_staging(self) -> None:
        plan, staged = self.stage("recover-staging")
        legacy_migration._begin_transaction(self.repo, staged, plan)

        legacy_migration.recover_transaction(self.repo)

        self.assertFalse(staged.runs_root.exists())
        self.assertFalse(staged.state_root.exists())
        self.assertFalse(
            (self.repo / "runner-state/.legacy-migration-transaction.json")
            .exists()
        )

    def test_recovery_rolls_back_an_interrupted_quarantine(self) -> None:
        original_hashes = self.source_hashes()
        plan, staged = self.stage("recover-quarantine")
        journal = legacy_migration._begin_transaction(
            self.repo, staged, plan
        )
        run = journal["paths"]["runs"][0]
        legacy_migration._transaction_rename(
            self.repo,
            journal,
            Path(run["source"]),
            Path(run["quarantine"]),
            "run-quarantine",
        )

        legacy_migration.recover_transaction(self.repo)

        self.assertEqual(self.source_hashes(), original_hashes)
        self.assertFalse(staged.runs_root.exists())
        self.assertFalse(staged.state_root.exists())
        self.assertFalse(
            (self.repo / "runner-state/.legacy-migration-transaction.json")
            .exists()
        )

    def test_recovery_finishes_a_validated_transaction(self) -> None:
        plan, staged = self.stage("recover-validated")
        with mock.patch.object(
            legacy_migration,
            "_remove_validated_quarantines",
            side_effect=OSError("injected validated interruption"),
        ):
            with self.assertRaisesRegex(OSError, "validated interruption"):
                legacy_migration.publish_migration(self.repo, staged, plan)
        journal = json.loads(
            (
                self.repo
                / "runner-state/.legacy-migration-transaction.json"
            ).read_text()
        )
        self.assertEqual(journal["phase"], "VALIDATED")

        legacy_migration.recover_transaction(self.repo)

        self.assertFalse((self.repo / "audits" / BARE_RUN).exists())
        self.assertTrue((self.repo / "runs" / BARE_RUN / "run.json").is_file())
        self.assertTrue(
            (self.repo / "runner-state" / SEMANTICS_RUN).is_dir()
        )
        self.assertFalse(
            (self.repo / "runner-state/.legacy-migration-transaction.json")
            .exists()
        )

    def test_apply_cli_reports_validated_recovery_without_rescanning(
        self,
    ) -> None:
        plan, staged = self.stage("recover-cli")
        with mock.patch.object(
            legacy_migration,
            "_remove_validated_quarantines",
            side_effect=OSError("injected validated interruption"),
        ):
            with self.assertRaisesRegex(OSError, "validated interruption"):
                legacy_migration.publish_migration(self.repo, staged, plan)

        fixture_tools = self.repo / "tools"
        fixture_tools.mkdir()
        script = Path(legacy_migration.__file__).parent / "migrate_legacy_runs.py"
        shutil.copy2(script, fixture_tools / script.name)
        environment = dict(os.environ)
        environment["PYTHONPATH"] = str(script.parent.parent)
        report = self.repo / "recovered-completion.json"
        result = subprocess.run(
            [
                sys.executable,
                str(fixture_tools / script.name),
                "--repo",
                str(self.repo),
                "--apply",
                "--report",
                str(report),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            env=environment,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        expected = {
            "mode": "apply",
            "phase": "COMPLETE",
            "recovered": True,
            "transaction_id": "recover-cli",
        }
        self.assertEqual(json.loads(result.stdout), expected)
        self.assertEqual(json.loads(report.read_text()), expected)
        self.assertFalse(
            (self.repo / "runner-state/.legacy-migration-transaction.json")
            .exists()
        )
        self.assertTrue((self.repo / "runs" / BARE_RUN / "run.json").is_file())

    def test_apply_cli_reports_complete_journal_recovery_without_rescanning(
        self,
    ) -> None:
        plan, staged = self.stage("recover-complete")
        with mock.patch.object(
            legacy_migration,
            "_remove_journal",
            side_effect=OSError("injected journal unlink interruption"),
        ):
            with self.assertRaisesRegex(OSError, "journal unlink interruption"):
                legacy_migration.publish_migration(self.repo, staged, plan)
        journal_path = (
            self.repo / "runner-state/.legacy-migration-transaction.json"
        )
        self.assertEqual(
            json.loads(journal_path.read_text())["phase"],
            "COMPLETE",
        )

        fixture_tools = self.repo / "tools"
        fixture_tools.mkdir()
        script = Path(legacy_migration.__file__).parent / "migrate_legacy_runs.py"
        shutil.copy2(script, fixture_tools / script.name)
        environment = dict(os.environ)
        environment["PYTHONPATH"] = str(script.parent.parent)
        report = self.repo / "recovered-complete.json"
        result = subprocess.run(
            [
                sys.executable,
                str(fixture_tools / script.name),
                "--repo",
                str(self.repo),
                "--apply",
                "--report",
                str(report),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            env=environment,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        expected = {
            "mode": "apply",
            "phase": "COMPLETE",
            "recovered": True,
            "transaction_id": "recover-complete",
        }
        self.assertEqual(json.loads(result.stdout), expected)
        self.assertEqual(json.loads(report.read_text()), expected)
        self.assertFalse(journal_path.exists())
        self.assertTrue((self.repo / "runs" / BARE_RUN / "run.json").is_file())

    def test_migration_lock_does_not_relabel_body_oserrors(self) -> None:
        with self.assertRaisesRegex(OSError, "body failure"):
            with legacy_migration.migration_lock(self.repo):
                raise OSError("body failure")

    def test_dry_run_cli_reports_exact_plan_without_changing_sources(
        self,
    ) -> None:
        self.expand_fixed_scope_fixture()
        original_hashes = self.source_hashes()
        fixture_tools = self.repo / "tools"
        fixture_tools.mkdir()
        script = Path(legacy_migration.__file__).parent / "migrate_legacy_runs.py"
        shutil.copy2(script, fixture_tools / script.name)
        environment = dict(os.environ)
        environment["PYTHONPATH"] = str(script.parent.parent)
        result = subprocess.run(
            [
                sys.executable,
                str(fixture_tools / script.name),
                "--repo",
                str(self.repo),
                "--dry-run",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            env=environment,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        document = json.loads(result.stdout)
        self.assertEqual(
            document["totals"],
            {
                "runs": 2,
                "tasks": 328,
                "sessions": 328,
                "succeeded": 324,
                "timeout": 4,
                "provenance_incomplete": 3,
                "pass": 10,
                "concerns": 81,
                "fail": 71,
                "omitted_roots": 0,
                "omitted_files": 0,
                "omitted_bytes": 0,
            },
        )
        self.assertIn(
            document["activity"]["docker"]["status"],
            {"AVAILABLE", "UNAVAILABLE"},
        )
        self.assertEqual(self.source_hashes(), original_hashes)
        self.assertFalse(any((self.repo / "runs").glob(".legacy-migration-*")))
        state_root = self.repo / "runner-state"
        self.assertTrue(
            not state_root.exists()
            or not any(
                path.name in (BARE_RUN, SEMANTICS_RUN)
                for path in state_root.iterdir()
            )
        )

    def test_cli_rejects_selectors_and_maps_rollback_failure_to_exit_three(
        self,
    ) -> None:
        from tools import migrate_legacy_runs

        script = (
            Path(legacy_migration.__file__).parent / "migrate_legacy_runs.py"
        )
        usage = subprocess.run(
            [sys.executable, str(script), "--all"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        self.assertEqual(usage.returncode, 2)

        error_output = io.StringIO()
        with mock.patch.object(
            legacy_migration,
            "recover_transaction",
            side_effect=legacy_migration.LegacyMigrationRollbackError(
                "fixture rollback failure"
            ),
        ), redirect_stderr(error_output):
            status = migrate_legacy_runs.main(
                ["--repo", str(self.repo), "--apply"]
            )
        self.assertEqual(status, 3)
        self.assertIn("fixture rollback failure", error_output.getvalue())


class LegacyMigrationClassificationTests(LegacyMigrationFixture):
    def test_scans_exact_configs_and_classifies_tasks(self) -> None:
        plan = self.scan()

        self.assertEqual(
            [run.run_id for run in plan.runs],
            [BARE_RUN, SEMANTICS_RUN],
        )
        bare = plan.runs[0]
        self.assertEqual(bare.counts["succeeded"], 4)
        self.assertEqual(bare.counts["provenance_incomplete"], 1)
        self.assertEqual(bare.counts["pass"], 1)
        self.assertEqual(bare.counts["concerns"], 1)
        self.assertEqual(bare.counts["fail"], 1)
        semantics = plan.runs[1]
        self.assertEqual(semantics.counts["succeeded"], 1)
        self.assertEqual(semantics.counts["timeout"], 1)

    def test_records_only_suffix_kompiled_roots(self) -> None:
        task = self.repo / "runs" / BARE_RUN / BARE_SUCCESS
        omitted = task / "verification-kompiled"
        nested = omitted / "nested-kompiled"
        nested.mkdir(parents=True)
        (omitted / "one.bin").write_bytes(b"abc")
        (nested / "two.bin").write_bytes(b"defg")
        (task / "not-kompiled.txt").write_text("retained\n")

        plan = self.scan()
        task_plan = plan.runs[0].tasks[0]

        self.assertEqual(
            [item.relative_path for item in task_plan.omitted],
            ["verification-kompiled"],
        )
        self.assertEqual(task_plan.omitted[0].file_count, 2)
        self.assertEqual(task_plan.omitted[0].total_bytes, 7)
        self.assertIn(
            "not-kompiled.txt",
            dict(task_plan.retained_files),
        )

    def test_preserves_session_identity_cli_version_and_audit_verdict(self) -> None:
        task = self.scan().runs[0].tasks[0]

        self.assertEqual(task.session_id, SESSION_IDS[(BARE_RUN, BARE_SUCCESS)])
        self.assertEqual(task.codex_cli_version, "0.144.6")
        self.assertEqual(task.result_marker, "KPROVE_PASSED")
        self.assertEqual(task.audit_verdict, "PASS")
        self.assertEqual(task.audit_legitimacy, "LEGIT")

    def test_plan_document_has_stable_exact_totals(self) -> None:
        document = legacy_migration.plan_document(self.scan())

        self.assertEqual(
            document["totals"],
            {
                "runs": 2,
                "tasks": 6,
                "sessions": 6,
                "succeeded": 5,
                "timeout": 1,
                "provenance_incomplete": 1,
                "pass": 1,
                "concerns": 1,
                "fail": 1,
                "omitted_roots": 0,
                "omitted_files": 0,
                "omitted_bytes": 0,
            },
        )
        self.assertEqual(
            [run["run_id"] for run in document["runs"]],
            [BARE_RUN, SEMANTICS_RUN],
        )


class LegacyMigrationRejectionTests(LegacyMigrationFixture):
    def assert_scan_rejected(self, pattern: str) -> None:
        with self.assertRaisesRegex(
            legacy_migration.LegacyMigrationError,
            pattern,
        ):
            self.scan()

    def test_rejects_malformed_json(self) -> None:
        metrics = self.repo / "runs" / BARE_RUN / BARE_SUCCESS / "metrics.json"
        metrics.write_text("{not JSON}\n")

        self.assert_scan_rejected("malformed JSON")

    def test_rejects_duplicate_rollouts(self) -> None:
        trace = self.repo / "runs" / BARE_RUN / BARE_SUCCESS / "codex-trace"
        second = trace / "2026/07/25/duplicate.jsonl"
        second.parent.mkdir(parents=True)
        second.write_text(
            json.dumps(
                {
                    "type": "session_meta",
                    "payload": {
                        "id": SESSION_IDS[(BARE_RUN, BARE_SUCCESS)],
                        "cli_version": "0.144.6",
                    },
                }
            )
            + "\n"
        )

        self.assert_scan_rejected("exactly one rollout JSONL")

    def test_rejects_unexpected_missing_manifest(self) -> None:
        manifest = (
            self.repo / "runs" / BARE_RUN / BARE_SUCCESS / "run-input.json"
        )
        manifest.unlink()

        self.assert_scan_rejected("unexpected missing")

    def test_rejects_unexpected_present_manifest(self) -> None:
        manifest = (
            self.repo / "runs" / BARE_RUN / BARE_INCOMPLETE / "run-input.json"
        )
        self.write_json(
            manifest,
            {
                "schema_version": 1,
                "config": BARE_RUN,
                "problem_id": BARE_INCOMPLETE,
                "condition": {
                    "name": "bare",
                    "kit": False,
                    "semantics": False,
                },
                "inputs": {
                    "instruction_prompt": "bare.md",
                    "instruction_prompt_sha256": "1" * 64,
                    "problem_prompt_sha256": "2" * 64,
                    "translator_sha256": "3" * 64,
                },
            },
        )

        self.assert_scan_rejected("expected incomplete-provenance")

    def test_rejects_unexpected_timeout(self) -> None:
        metrics_path = (
            self.repo / "runs" / BARE_RUN / BARE_SUCCESS / "metrics.json"
        )
        metrics = json.loads(metrics_path.read_text())
        metrics.update(
            {
                "end_epoch": 4600,
                "duration_s": 3600,
                "exit_code": 124,
                "timed_out": True,
            }
        )
        self.write_json(metrics_path, metrics)

        self.assert_scan_rejected("expected success")

    def test_rejects_unsupported_source_entry(self) -> None:
        fifo = self.repo / "runs" / BARE_RUN / BARE_SUCCESS / "unsafe.fifo"
        os.mkfifo(fifo)

        self.assert_scan_rejected("unsupported entry")

    def test_rejects_incomplete_supposedly_complete_audit(self) -> None:
        verdict_path = (
            self.repo / "audits" / BARE_RUN / BARE_SUCCESS / "verdict.json"
        )
        verdict = json.loads(verdict_path.read_text())
        verdict["audit_status"] = "AUDIT_ERROR"
        verdict["error"] = "injected"
        self.write_json(verdict_path, verdict)

        self.assert_scan_rejected("not complete")

    def test_rejects_invalid_audit_verdict_pair(self) -> None:
        verdict_path = (
            self.repo / "audits" / BARE_RUN / BARE_SUCCESS / "verdict.json"
        )
        verdict = json.loads(verdict_path.read_text())
        verdict["legitimacy"] = "NOT_LEGIT"
        self.write_json(verdict_path, verdict)

        self.assert_scan_rejected("verdict/legitimacy pair")

    def test_rejects_mismatched_declared_audit_distribution(self) -> None:
        audit = self.repo / "audits" / BARE_RUN / BARE_SUCCESS
        verdict = json.loads((audit / "verdict.json").read_text())
        verdict.update({"verdict": "CONCERNS", "legitimacy": "LEGIT"})
        self.write_json(audit / "verdict.json", verdict)
        (audit / "REVIEW.md").write_text(
            "# Fixed audit\n\nAll seven audit stages completed.\n\n"
            "VERDICT: CONCERNS\n"
            "LEGITIMACY: LEGIT\n"
        )

        self.assert_scan_rejected("audit distribution mismatch")

    def test_rejects_extra_task(self) -> None:
        extra = self.repo / "runs" / BARE_RUN / "999-extra"
        extra.mkdir()

        self.assert_scan_rejected("has 5 tasks; expected 4")

    def test_rejects_missing_task(self) -> None:
        missing = self.repo / "runs" / BARE_RUN / BARE_SUCCESS
        shutil.rmtree(missing)

        self.assert_scan_rejected("has 3 tasks; expected 4")

    def test_rejects_semantics_audit_source(self) -> None:
        unexpected = self.repo / "audits" / SEMANTICS_RUN
        unexpected.mkdir()

        self.assert_scan_rejected("must not have an audit tree")

    def test_plan_dataclasses_and_counts_are_immutable(self) -> None:
        plan = self.scan()

        with self.assertRaises(FrozenInstanceError):
            plan.runs = ()
        with self.assertRaises(TypeError):
            plan.runs[0].counts["tasks"] = 0


if __name__ == "__main__":
    unittest.main()
