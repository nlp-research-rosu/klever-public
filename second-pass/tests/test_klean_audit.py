import json
import shutil
import uuid
from pathlib import Path
from unittest import mock

from tests.test_klean_export import (
    KleanExportContractTests,
    write_discovery_manifest,
)
from tests.test_pipeline_layout import PipelineLayoutFixture
from tools import (
    audit_contract,
    klean_audit_contract,
    klean_export,
    klean_preflight,
    pipeline_contract,
    stage5_runner,
    usage_accounting,
)


class KleanAuditTests(PipelineLayoutFixture):
    PROOF_CASE = "proof-case"
    EMPTY_CASE = "empty-case"

    def setUp(self) -> None:
        super().setUp()
        self.make_problem(self.PROOF_CASE)
        self.make_problem(self.EMPTY_CASE)
        self.run_id = "stage6-run"
        pipeline_contract.create_run(
            self.repo,
            run_id=self.run_id,
            config="codex-gpt-audited-xhigh-kit-semantics",
            problem_ids=[self.PROOF_CASE, self.EMPTY_CASE],
        )
        self.cases = {
            self.PROOF_CASE: self._complete_case(
                self.PROOF_CASE,
                classifications=["DOMAIN_LEMMA", "DEFINITION"],
                with_proof=True,
            ),
            self.EMPTY_CASE: self._complete_case(
                self.EMPTY_CASE,
                classifications=[
                    "DEFINITION",
                    "DEFINITION",
                ],
                with_proof=False,
            ),
        }

    @staticmethod
    def _build_runner(command, *, cwd, timeout):
        return 0, f"{' '.join(command)} okay\n"

    @staticmethod
    def _export_runner(command, *, cwd, timeout, env, shell=False):
        return KleanExportContractTests.fake_runner(
            None,
            command,
            cwd=cwd,
            timeout=timeout,
            env=env,
            shell=shell,
        )

    def _complete_case(
        self,
        problem: str,
        *,
        classifications: list[str],
        with_proof: bool,
    ) -> dict[str, Path]:
        task = self.repo / f"runs/{self.run_id}/tasks/{problem}"
        workspace = task / "01-k-proof/workspace"
        for name, text in {
            "solution.py": "def solve(value):\n    return value\n",
            "solution.mpy": "def solve(value):\n    return value\n",
            "spec.k": "module TEST-SPEC endmodule\n",
            "prove.sh": "#!/usr/bin/env bash\nexit 0\n",
            "PROOF.md": "Proof evidence.\n",
        }.items():
            (workspace / name).write_text(text)
        if classifications:
            verification = (
                "module TEST-VERIFICATION\n"
                "  imports TEST-SYNTAX\n"
                "  syntax Int ::= summary(Int) [function]\n"
                "  rule external(summary(I)) => I [simplification]\n"
                "  rule summary(I) => I [simplification]\n"
                "endmodule\n"
            )
        else:
            verification = (
                "module TEST-VERIFICATION\n"
                "  imports TEST-SYNTAX\n"
                "endmodule\n"
            )
        (workspace / "verification.k").write_text(verification)
        (workspace / "syntax.k").write_text(
            "module TEST-SYNTAX endmodule\n"
        )

        session_id = str(uuid.uuid4())
        stage1 = pipeline_contract.prepare_invocation(
            self.repo, self.run_id, problem, "01-k-proof"
        )
        (stage1.path / "prompt.txt").write_text("K proof prompt\n")
        (stage1.path / "codex-output.log").write_text("K proof\n")
        (stage1.path / "codex-last.txt").write_text("K proof complete\n")
        stage1_trace = stage1.path / "codex-trace"
        stage1_trace.mkdir()
        (stage1_trace / "rollout.jsonl").write_text(
            json.dumps(
                {
                    "type": "session_meta",
                    "payload": {"id": session_id},
                }
            )
            + "\n"
        )
        pipeline_contract.finalize_invocation(
            self.repo,
            self.run_id,
            problem,
            "01-k-proof",
            stage1.name,
            exit_code=0,
            duration_s=10,
            timeout_marker=False,
            oom_killed=False,
            image_id="sha256:k-proof",
        )
        (stage1.path / "runtime-metrics.json").write_text(
            (stage1.path / "metrics.json").read_text()
        )

        stage2 = audit_contract.prepare_stage2_execution(
            self.repo, self.run_id, problem
        )
        self._complete_model_audit(stage2, "PASS")
        pipeline_contract.select_stage_output(
            self.repo,
            self.run_id,
            problem,
            "02-k-audit",
            stage2.name,
        )

        stage3 = pipeline_contract.prepare_invocation(
            self.repo, self.run_id, problem, "03-lemma-discovery"
        )
        discovery = write_discovery_manifest(
            workspace,
            stage3.path / "validated-trust-boundary.json",
            classifications,
        )
        (stage3.path / "codex-output.log").write_text("discovery\n")
        (stage3.path / "codex-last.txt").write_text(
            "RESULT: LEMMA_DISCOVERY_COMPLETE — classified inventory\n"
        )
        stage3_trace = stage3.path / "codex-trace"
        stage3_trace.mkdir()
        (stage3_trace / "rollout.jsonl").write_text(
            json.dumps(
                {
                    "type": "session_meta",
                    "payload": {"id": session_id},
                }
            )
            + "\n"
        )
        discovery_hash = pipeline_contract.sha256_file(discovery)
        pipeline_contract.finalize_invocation(
            self.repo,
            self.run_id,
            problem,
            "03-lemma-discovery",
            stage3.name,
            exit_code=0,
            duration_s=10,
            timeout_marker=False,
            oom_killed=False,
            image_id="sha256:discovery",
            result_metadata={
                "trust_boundary_sha256": discovery_hash,
                "trust_boundary_artifact": (
                    f"invocations/{stage3.name}/"
                    "validated-trust-boundary.json"
                ),
            },
            expected_evidence={
                "validated-trust-boundary.json": discovery_hash,
            },
        )

        generation = (
            task / "04-klean-generation/generations/001"
        )
        klean_export.export_frozen(
            workspace,
            discovery,
            generation,
            problem=problem,
            toolchain_lock=self.repo / "data/klean-toolchain.lock.json",
            generator_image_id="sha256:klean",
            run_command=self._export_runner,
        )
        generator_manifest = json.loads(
            (generation / "generator-manifest.json").read_text()
        )
        generator_image_id = generator_manifest["provenance"][
            "generator_image_id"
        ]
        producer_sources = (
            self.repo
            / "data/stage4-producer-sources"
            / generator_image_id.removeprefix("sha256:")
        )
        producer_sources.mkdir(parents=True, exist_ok=True)
        source_files = {
            "klean_export.py": generator_manifest["exporter_sha256"],
            "klean.py": generator_manifest["klean_py_sha256"],
        }
        for name in source_files:
            shutil.copy2(
                Path(klean_export.__file__).resolve().parent / name,
                producer_sources / name,
            )
        (producer_sources / "source-manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "generator_image_id": generator_image_id,
                    "files": source_files,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )
        (generation / "export.log").write_text("exported\n")
        klean_preflight.run_preflight(
            workspace,
            discovery,
            generation,
            toolchain_lock=self.repo / "data/klean-toolchain.lock.json",
            run_command=self._build_runner,
        )
        (generation / "preflight.log").write_text("preflight\n")
        pipeline_contract.select_stage_output(
            self.repo,
            self.run_id,
            problem,
            "04-klean-generation",
            generation.name,
            expected_candidate_sha256=pipeline_contract.sha256_tree(
                generation
            ),
        )

        lean_workspace = task / "05-lean-proof/workspace"
        if with_proof:
            generator_manifest = json.loads(
                (generation / "generator-manifest.json").read_text()
            )
            stage5_runner._initialize_workspace(
                lean_workspace, generator_manifest, problem
            )
            proof = lean_workspace / "Proof.lean"
            proof.write_text(
                proof.read_text()
                .replace(
                    "axiom external : Int → Int",
                    "def external (value : Int) : Int := value",
                )
                .replace(
                    "  sorry",
                    "  simp "
                    "[KleanProofCase.Lemmas.targetStatement, external]",
                )
            )
            stage5 = pipeline_contract.prepare_invocation(
                self.repo, self.run_id, problem, "05-lean-proof"
            )
            (stage5.path / "codex-output.log").write_text("Lean proof\n")
            (stage5.path / "codex-last.txt").write_text(
                "RESULT: LEAN_PROOF_COMPLETE — proved fixed target\n"
            )
            stage5_trace = stage5.path / "codex-trace"
            stage5_trace.mkdir()
            (stage5_trace / "rollout.jsonl").write_text(
                json.dumps(
                    {
                        "type": "session_meta",
                        "payload": {"id": session_id},
                    }
                )
                + "\n"
            )
            pipeline_contract.finalize_invocation(
                self.repo,
                self.run_id,
                problem,
                "05-lean-proof",
                stage5.name,
                exit_code=0,
                duration_s=10,
                timeout_marker=False,
                oom_killed=False,
                image_id="sha256:lean-proof",
            )
        return {
            "task": task,
            "stage1": workspace,
            "stage2": stage2,
            "stage3": discovery,
            "stage4": generation,
            "stage5": lean_workspace,
        }

    @staticmethod
    def _complete_model_audit(execution: Path, status: str) -> None:
        for name in (
            "audit-input.json",
            "metrics.json",
            "codex-output.log",
            "codex-last.txt",
            "REVIEW.md",
        ):
            path = execution / name
            if name != "audit-input.json" or not path.exists():
                path.write_text("{}\n")
        trace = execution / "codex-trace"
        trace.mkdir()
        (trace / "rollout.jsonl").write_text(
            json.dumps(
                {
                    "type": "event_msg",
                    "payload": {
                        "type": "token_count",
                        "info": {
                            "total_token_usage": {
                                "input_tokens": 120,
                                "cached_input_tokens": 30,
                                "output_tokens": 30,
                                "reasoning_output_tokens": 10,
                                "total_tokens": 150,
                            }
                        },
                    },
                }
            )
            + "\n"
        )
        evidence = execution / "evidence"
        evidence.mkdir(exist_ok=True)
        (evidence / "checks.txt").write_text("checked\n")
        if status == "AUDIT_ERROR":
            verdict = {
                "audit_status": "AUDIT_ERROR",
                "verdict": None,
                "legitimacy": None,
                "error": "infrastructure",
            }
        else:
            verdict = {
                "audit_status": "COMPLETE",
                "verdict": status,
                "legitimacy": (
                    "LEGIT" if status != "FAIL" else "NOT_LEGIT"
                ),
                "error": None,
            }
            (execution / "mechanical-check.json").write_text(
                json.dumps({"status": "PASS"}) + "\n"
            )
        (execution / "verdict.json").write_text(
            json.dumps(verdict) + "\n"
        )
        usage_accounting.write_trace_usage(
            trace, execution / "usage.json"
        )

    def _resolution(self, problem: str) -> dict[str, object]:
        return klean_audit_contract.resolve_stage6_audit(
            self.repo, self.run_id, problem
        )

    def _prepare(self, problem: str) -> tuple[Path, dict[str, object]]:
        resolution = self._resolution(problem)
        execution = klean_audit_contract.prepare_stage6_execution(
            self.repo,
            self.run_id,
            problem,
            expected_resolved_input_sha256=resolution[
                "resolved_input_sha256"
            ],
        )
        (execution / "audit-input.json").write_text(
            json.dumps(
                {
                    **resolution,
                    "audit": {
                        "image_id": "sha256:test-auditor",
                        "output": str(execution),
                    },
                }
            )
            + "\n"
        )
        return execution, resolution

    def test_resolves_proof_bearing_and_no_obligation_modes(self) -> None:
        proof_case = klean_audit_contract.resolve_stage6_audit(
            self.repo, self.run_id, self.PROOF_CASE
        )
        proof_resolution = proof_case["resolution"]
        self.assertEqual(
            proof_resolution["mode"], "CLASSIFICATION_AND_PROOF"
        )
        self.assertIsNotNone(proof_resolution["lean_workspace"])
        proof_manifest = json.loads(
            (
                self.cases[self.PROOF_CASE]["stage4"]
                / "generator-manifest.json"
            ).read_text()
        )
        self.assertEqual(proof_manifest["obligation_count"], 1)
        self.assertTrue(proof_manifest["target"]["statement"])
        self.assertTrue(
            (
                self.cases[self.PROOF_CASE]["task"]
                / "05-lean-proof/result.json"
            ).is_file()
        )

        empty_case = klean_audit_contract.resolve_stage6_audit(
            self.repo, self.run_id, self.EMPTY_CASE
        )
        empty_resolution = empty_case["resolution"]
        self.assertEqual(
            empty_resolution["mode"], "CLASSIFICATION_ONLY"
        )
        self.assertIsNone(empty_resolution["lean_workspace"])
        empty_discovery = json.loads(
            Path(empty_resolution["discovery_manifest"]).read_text()
        )
        self.assertEqual(
            [
                record["classification"]
                for record in empty_discovery["rules"]
            ],
            ["DEFINITION", "DEFINITION"],
        )
        empty_preflight = json.loads(
            (
                self.cases[self.EMPTY_CASE]["stage4"] / "preflight.json"
            ).read_text()
        )
        self.assertEqual(
            empty_preflight["status"], "KLEAN_NO_OBLIGATIONS"
        )
        self.assertFalse(
            (
                self.cases[self.EMPTY_CASE]["task"]
                / "05-lean-proof/result.json"
            ).exists()
        )

        for problem, resolved in (
            (self.PROOF_CASE, proof_case),
            (self.EMPTY_CASE, empty_case),
        ):
            case = self.cases[problem]
            signed = resolved["resolution"]
            self.assertEqual(
                Path(signed["discovery_manifest"]), case["stage3"]
            )
            self.assertEqual(
                Path(signed["klean_generation"]), case["stage4"]
            )
            self.assertEqual(
                signed["hashes"]["discovery_manifest_sha256"],
                pipeline_contract.sha256_file(case["stage3"]),
            )
            self.assertEqual(
                signed["stage1_source_hashes"]["verification.k"],
                pipeline_contract.sha256_file(
                    case["stage1"] / "verification.k"
                ),
            )
            self.assertIn(
                "solution.py", signed["stage1_source_hashes"]
            )
            self.assertIn("generation_producer_sources", signed)
            producer_sources = Path(signed["generation_producer_sources"])
            self.assertTrue(producer_sources.is_dir())
            self.assertEqual(
                signed["hashes"][
                    "generation_producer_sources_sha256"
                ],
                pipeline_contract.sha256_tree(producer_sources),
            )
            self.assertRegex(
                resolved["resolved_input_sha256"], r"^[0-9a-f]{64}$"
            )

    def test_missing_or_mutated_generation_producer_sources_block_stage6(
        self,
    ) -> None:
        generation = self.cases[self.PROOF_CASE]["stage4"]
        generator_manifest = json.loads(
            (generation / "generator-manifest.json").read_text()
        )
        producer_sources = (
            self.repo
            / "data/stage4-producer-sources"
            / generator_manifest["provenance"]["generator_image_id"].removeprefix(
                "sha256:"
            )
        )
        exporter = producer_sources / "klean_export.py"
        original = exporter.read_text()
        exporter.write_text(original + "\n# changed\n")
        with self.assertRaisesRegex(
            klean_audit_contract.KleanAuditContractError,
            "producer source.*SHA-256",
        ):
            self._resolution(self.PROOF_CASE)
        exporter.write_text(original)
        shutil.rmtree(producer_sources)
        with self.assertRaisesRegex(
            klean_audit_contract.KleanAuditContractError,
            "producer source bundle",
        ):
            self._resolution(self.PROOF_CASE)

    def test_resolution_uses_an_exact_signed_nested_projection(
        self,
    ) -> None:
        audit_input = self._resolution(self.PROOF_CASE)

        self.assertEqual(
            set(audit_input),
            {"schema_version", "resolution", "resolved_input_sha256"},
        )
        self.assertNotIn("mode", audit_input)
        self.assertEqual(
            set(audit_input["resolution"]),
            klean_audit_contract._STAGE6_RESOLUTION_KEYS,
        )
        self.assertEqual(
            audit_input["resolved_input_sha256"],
            klean_audit_contract._canonical_json_sha256(
                audit_input["resolution"]
            ),
        )

    def test_pass_generation_requires_successful_stage5_result(self) -> None:
        result = (
            self.cases[self.PROOF_CASE]["task"]
            / "05-lean-proof/result.json"
        )
        result.unlink()
        with self.assertRaisesRegex(
            klean_audit_contract.KleanAuditContractError,
            "Stage 5",
        ):
            klean_audit_contract.resolve_stage6_audit(
                self.repo, self.run_id, self.PROOF_CASE
            )

    def test_no_obligations_requires_no_stage5_result(self) -> None:
        result = (
            self.cases[self.EMPTY_CASE]["task"]
            / "05-lean-proof/result.json"
        )
        result.write_text('{"status": "SUCCEEDED"}\n')
        with self.assertRaisesRegex(
            klean_audit_contract.KleanAuditContractError,
            "must not have a Stage 5 result",
        ):
            klean_audit_contract.resolve_stage6_audit(
                self.repo, self.run_id, self.EMPTY_CASE
            )

    def test_incomplete_input_provenance_blocks_stage6_resolution(
        self,
    ) -> None:
        task_manifest = (
            self.cases[self.PROOF_CASE]["task"] / "task.json"
        )
        document = json.loads(task_manifest.read_text())
        document.update(
            {
                "input_provenance": "INCOMPLETE",
                "pipeline_block": "INPUT_PROVENANCE_INCOMPLETE",
            }
        )
        task_manifest.write_text(json.dumps(document) + "\n")
        with self.assertRaisesRegex(
            klean_audit_contract.KleanAuditContractError,
            "INPUT_PROVENANCE_INCOMPLETE",
        ):
            klean_audit_contract.resolve_stage6_audit(
                self.repo, self.run_id, self.PROOF_CASE
            )

    def test_mutated_generation_or_lean_proof_is_rejected(self) -> None:
        proof = self.cases[self.PROOF_CASE]["stage5"] / "Proof.lean"
        original_proof = proof.read_text()
        proof.write_text(original_proof + "\n-- changed\n")
        with self.assertRaisesRegex(
            klean_audit_contract.KleanAuditContractError,
            "Lean workspace changed",
        ):
            klean_audit_contract.resolve_stage6_audit(
                self.repo, self.run_id, self.PROOF_CASE
            )
        proof.write_text(original_proof)

        generated = (
            self.cases[self.PROOF_CASE]["stage4"]
            / "generated/KleanProofCase/Lemmas.lean"
        )
        generated.write_text(generated.read_text() + "\n-- changed\n")
        with self.assertRaisesRegex(
            klean_audit_contract.KleanAuditContractError,
            "generation changed",
        ):
            klean_audit_contract.resolve_stage6_audit(
                self.repo, self.run_id, self.PROOF_CASE
            )

    def test_mutated_stage5_invocation_evidence_is_rejected(self) -> None:
        result = json.loads(
            (
                self.cases[self.PROOF_CASE]["task"]
                / "05-lean-proof/result.json"
            ).read_text()
        )
        codex_last = (
            self.cases[self.PROOF_CASE]["task"]
            / "05-lean-proof/invocations"
            / result["invocation"]
            / "codex-last.txt"
        )
        codex_last.write_text("changed after Stage 5 success\n")

        with self.assertRaisesRegex(
            klean_audit_contract.KleanAuditContractError,
            "Stage 5 invocation evidence changed",
        ):
            klean_audit_contract.resolve_stage6_audit(
                self.repo, self.run_id, self.PROOF_CASE
            )

    def test_second_execution_is_allowed_only_after_audit_error(
        self,
    ) -> None:
        first, _first_resolution = self._prepare(self.PROOF_CASE)
        self.assertEqual(first.name, "001")
        self._complete_model_audit(first, "AUDIT_ERROR")
        (first / "usage.json").unlink()
        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError, "usage.json"
        ):
            pipeline_contract.select_stage_output(
                self.repo,
                self.run_id,
                self.PROOF_CASE,
                "06-lean-audit",
                first.name,
            )
        usage_accounting.write_trace_usage(
            first / "codex-trace",
            first / "usage.json",
        )
        pipeline_contract.select_stage_output(
            self.repo,
            self.run_id,
            self.PROOF_CASE,
            "06-lean-audit",
            first.name,
        )
        second, _second_resolution = self._prepare(self.PROOF_CASE)
        self.assertEqual(second.name, "002")
        self._complete_model_audit(second, "PASS")
        pipeline_contract.select_stage_output(
            self.repo,
            self.run_id,
            self.PROOF_CASE,
            "06-lean-audit",
            second.name,
        )
        with self.assertRaisesRegex(
            klean_audit_contract.KleanAuditContractError, "terminal"
        ):
            self._prepare(self.PROOF_CASE)

    def test_explicit_replacement_preserves_terminal_stage6_audit(
        self,
    ) -> None:
        first, first_resolution = self._prepare(self.PROOF_CASE)
        self._complete_model_audit(first, "PASS")
        signed = first_resolution["resolution"]
        (first / "mechanical-check.json").write_text(
            json.dumps(
                {
                    "status": "PASS",
                    "mode": signed["mode"],
                    "resolved_input_sha256": first_resolution[
                        "resolved_input_sha256"
                    ],
                    "input_hashes": signed["hashes"],
                }
            )
            + "\n"
        )
        original = klean_audit_contract.publish_stage6_execution(
            self.repo,
            self.run_id,
            self.PROOF_CASE,
            first.name,
            expected_resolved_input_sha256=first_resolution[
                "resolved_input_sha256"
            ],
            expected_candidate_sha256=pipeline_contract.sha256_tree(first),
        )

        next_resolution = self._resolution(self.PROOF_CASE)
        second = klean_audit_contract.prepare_stage6_execution(
            self.repo,
            self.run_id,
            self.PROOF_CASE,
            expected_resolved_input_sha256=next_resolution[
                "resolved_input_sha256"
            ],
            replace_selected=True,
        )

        self.assertEqual(second.name, "002")
        selected_path = (
            self.cases[self.PROOF_CASE]["task"]
            / "06-lean-audit/selected.json"
        )
        self.assertEqual(json.loads(selected_path.read_text()), original)
        self._complete_model_audit(second, "CONCERNS")
        (second / "audit-input.json").write_text(
            json.dumps(next_resolution) + "\n"
        )
        next_signed = next_resolution["resolution"]
        (second / "mechanical-check.json").write_text(
            json.dumps(
                {
                    "status": "PASS",
                    "mode": next_signed["mode"],
                    "resolved_input_sha256": next_resolution[
                        "resolved_input_sha256"
                    ],
                    "input_hashes": next_signed["hashes"],
                }
            )
            + "\n"
        )
        replacement = klean_audit_contract.publish_stage6_execution(
            self.repo,
            self.run_id,
            self.PROOF_CASE,
            second.name,
            expected_resolved_input_sha256=next_resolution[
                "resolved_input_sha256"
            ],
            expected_candidate_sha256=pipeline_contract.sha256_tree(second),
            replace_selected=True,
        )

        self.assertEqual(replacement["relative_path"], "executions/002")
        self.assertEqual(replacement["replaces"], "executions/001")
        self.assertTrue(first.is_dir())
        self.assertEqual(
            json.loads((first / "verdict.json").read_text())["verdict"],
            "PASS",
        )

    def test_minimal_stage6_infrastructure_error_is_retryable(self) -> None:
        first, _first_resolution = self._prepare(self.EMPTY_CASE)
        (first / "verdict.json").write_text(
            json.dumps(
                {
                    "audit_status": "AUDIT_ERROR",
                    "verdict": None,
                    "legitimacy": None,
                    "error": "container unavailable",
                }
            )
            + "\n"
        )
        pipeline_contract.select_stage_output(
            self.repo,
            self.run_id,
            self.EMPTY_CASE,
            "06-lean-audit",
            first.name,
        )
        self.assertEqual(
            self._prepare(self.EMPTY_CASE)[0].name,
            "002",
        )

    def test_prompt_and_launcher_enforce_fresh_independent_audit(
        self,
    ) -> None:
        root = Path(__file__).resolve().parent.parent
        prompt = (root / "prompts/klean-audit.md").read_text()
        for required in (
            "UNTRUSTED EVIDENCE",
            "reconstruct every rule in the local verification-module",
            "omitted or duplicated",
            "reject a `DOMAIN_LEMMA` mislabeled as any",
            "`PROVED_DERIVED_LEMMA` is valid only when Stage 1 first proves",
            "irrelevant or weakened obligations",
            "`KLEAN_NO_OBLIGATIONS`",
            "genuinely empty domain set",
            "lake clean",
            "lake build",
            "#print axioms",
            "In proof mode, for every `target.parameters` entry",
            "sorry",
            "admit",
            "unsafe",
            "VERDICT:",
            "LEGITIMACY:",
            "/reference/generation-tools",
            "generation-time producer",
        ):
            self.assertIn(required, prompt)
        launcher = (root / "docker/klean-audit/run_task.sh").read_text()
        for target in (
            "/reference/k-proof,readonly",
            "/reference/k-audit,readonly",
            "/reference/lemma-discovery.json,readonly",
            "/reference/klean-generation,readonly",
            "/reference/generation-tools,readonly",
            "/candidate,readonly",
        ):
            self.assertIn(target, launcher)
        self.assertIn("CLASSIFICATION_AND_PROOF", launcher)
        self.assertIn("CLASSIFICATION_ONLY", launcher)
        self.assertIn("--discovery-manifest", launcher)
        self.assertNotIn("runner-state", launcher)
        self.assertNotIn("codex exec resume", launcher)
        self.assertIn("mechanical-check.json", launcher)
        self.assertIn("resolved_input_sha256", launcher)
        self.assertIn("expected-resolved-input-sha256", launcher)
        self.assertIn("--audit-input", launcher)
        self.assertIn("expected-candidate-sha256", launcher)
        self.assertIn("06-lean-audit", launcher)
        self.assertNotIn('"05-lean-audit"', launcher)
        entrypoint = (root / "docker/klean-audit/entrypoint.sh").read_text()
        self.assertIn("/independent-audit-entrypoint.sh", entrypoint)

    def test_failed_mechanical_gate_forces_terminal_not_legit(
        self,
    ) -> None:
        execution, resolution = self._prepare(self.PROOF_CASE)
        self._complete_model_audit(execution, "PASS")
        signed = resolution["resolution"]
        (execution / "mechanical-check.json").write_text(
            json.dumps(
                {
                    "status": "FAIL",
                    "error": "sorryAx",
                    "mode": signed["mode"],
                    "resolved_input_sha256": resolution[
                        "resolved_input_sha256"
                    ],
                    "input_hashes": signed["hashes"],
                }
            )
            + "\n"
        )
        reconciled = klean_audit_contract.reconcile_mechanical_verdict(
            execution / "verdict.json",
            execution / "mechanical-check.json",
            execution / "audit-input.json",
        )
        self.assertEqual(reconciled["verdict"], "FAIL")
        self.assertEqual(reconciled["legitimacy"], "NOT_LEGIT")

    def test_prepare_rejects_inputs_mutated_after_initial_resolution(
        self,
    ) -> None:
        resolution = self._resolution(self.PROOF_CASE)
        proof = self.cases[self.PROOF_CASE]["stage5"] / "Proof.lean"
        proof.write_text(proof.read_text() + "\n-- changed\n")

        with self.assertRaisesRegex(
            klean_audit_contract.KleanAuditContractError,
            "resolved inputs changed before Stage 6 allocation",
        ):
            klean_audit_contract.prepare_stage6_execution(
                self.repo,
                self.run_id,
                self.PROOF_CASE,
                expected_resolved_input_sha256=resolution[
                    "resolved_input_sha256"
                ],
            )

    def test_reconcile_rejects_mechanical_digest_mode_or_hash_mismatch(
        self,
    ) -> None:
        for field, value in (
            ("resolved_input_sha256", "b" * 64),
            ("mode", "CLASSIFICATION_ONLY"),
            ("input_hashes", {}),
        ):
            with self.subTest(field=field):
                execution, resolution = self._prepare(self.PROOF_CASE)
                self._complete_model_audit(execution, "PASS")
                signed = resolution["resolution"]
                mechanical = {
                    "status": "PASS",
                    "mode": signed["mode"],
                    "resolved_input_sha256": resolution[
                        "resolved_input_sha256"
                    ],
                    "input_hashes": signed["hashes"],
                }
                mechanical[field] = value
                (execution / "mechanical-check.json").write_text(
                    json.dumps(mechanical) + "\n"
                )
                reconciled = (
                    klean_audit_contract.reconcile_mechanical_verdict(
                        execution / "verdict.json",
                        execution / "mechanical-check.json",
                        execution / "audit-input.json",
                    )
                )
                self.assertEqual(reconciled["verdict"], "FAIL")
                self.assertEqual(reconciled["legitimacy"], "NOT_LEGIT")
                if (execution.parent.parent / "selected.json").exists():
                    (execution.parent.parent / "selected.json").unlink()
                for child in execution.parent.iterdir():
                    if child != execution:
                        continue
                    for path in sorted(child.rglob("*"), reverse=True):
                        if path.is_file():
                            path.unlink()
                        elif path.is_dir():
                            path.rmdir()
                    child.rmdir()

    def test_reconcile_rejects_signed_payload_tampering_with_retained_digest(
        self,
    ) -> None:
        execution, resolution = self._prepare(self.PROOF_CASE)
        self._complete_model_audit(execution, "PASS")
        signed = resolution["resolution"]
        (execution / "mechanical-check.json").write_text(
            json.dumps(
                {
                    "status": "PASS",
                    "mode": signed["mode"],
                    "resolved_input_sha256": resolution[
                        "resolved_input_sha256"
                    ],
                    "input_hashes": signed["hashes"],
                }
            )
            + "\n"
        )
        audit_input = json.loads(
            (execution / "audit-input.json").read_text()
        )
        stored = audit_input["resolution"]
        stored["target"] = {"statement": "True"}
        (execution / "audit-input.json").write_text(
            json.dumps(audit_input) + "\n"
        )

        with self.assertRaisesRegex(
            klean_audit_contract.KleanAuditContractError,
            "digest does not match signed resolution",
        ):
            klean_audit_contract.reconcile_mechanical_verdict(
                execution / "verdict.json",
                execution / "mechanical-check.json",
                execution / "audit-input.json",
            )

    def test_publication_rejects_stored_signed_resolution_tampering(
        self,
    ) -> None:
        execution, resolution = self._prepare(self.PROOF_CASE)
        self._complete_model_audit(execution, "PASS")
        signed = resolution["resolution"]
        (execution / "mechanical-check.json").write_text(
            json.dumps(
                {
                    "status": "PASS",
                    "mode": signed["mode"],
                    "resolved_input_sha256": resolution[
                        "resolved_input_sha256"
                    ],
                    "input_hashes": signed["hashes"],
                }
            )
            + "\n"
        )
        audit_input = json.loads(
            (execution / "audit-input.json").read_text()
        )
        stored = audit_input["resolution"]
        stored["stage1_source_hashes"]["verification.k"] = "f" * 64
        (execution / "audit-input.json").write_text(
            json.dumps(audit_input) + "\n"
        )

        with self.assertRaisesRegex(
            klean_audit_contract.KleanAuditContractError,
            "digest does not match signed resolution",
        ):
            klean_audit_contract.publish_stage6_execution(
                self.repo,
                self.run_id,
                self.PROOF_CASE,
                execution.name,
                expected_resolved_input_sha256=resolution[
                    "resolved_input_sha256"
                ],
                expected_candidate_sha256=(
                    pipeline_contract.sha256_tree(execution)
                ),
            )

    def test_publication_structurally_compares_fresh_signed_resolution(
        self,
    ) -> None:
        execution, resolution = self._prepare(self.PROOF_CASE)
        self._complete_model_audit(execution, "PASS")
        signed = resolution["resolution"]
        (execution / "mechanical-check.json").write_text(
            json.dumps(
                {
                    "status": "PASS",
                    "mode": signed["mode"],
                    "resolved_input_sha256": resolution[
                        "resolved_input_sha256"
                    ],
                    "input_hashes": signed["hashes"],
                }
            )
            + "\n"
        )
        audit_input = json.loads(
            (execution / "audit-input.json").read_text()
        )
        stored = audit_input["resolution"]
        stored["selections"]["k_audit"]["status"] = "FORGED"
        forged_digest = klean_audit_contract._canonical_json_sha256(
            stored
        )
        audit_input["resolved_input_sha256"] = forged_digest
        (execution / "audit-input.json").write_text(
            json.dumps(audit_input) + "\n"
        )
        mechanical = json.loads(
            (execution / "mechanical-check.json").read_text()
        )
        mechanical["resolved_input_sha256"] = forged_digest
        mechanical["input_hashes"] = stored["hashes"]
        (execution / "mechanical-check.json").write_text(
            json.dumps(mechanical) + "\n"
        )

        with self.assertRaisesRegex(
            klean_audit_contract.KleanAuditContractError,
            "stored signed resolution differs from fresh resolution",
        ):
            klean_audit_contract.publish_stage6_execution(
                self.repo,
                self.run_id,
                self.PROOF_CASE,
                execution.name,
                expected_resolved_input_sha256=forged_digest,
                expected_candidate_sha256=(
                    pipeline_contract.sha256_tree(execution)
                ),
            )

    def test_publication_re_resolves_inputs_and_guards_candidate_tree(
        self,
    ) -> None:
        execution, resolution = self._prepare(self.PROOF_CASE)
        self._complete_model_audit(execution, "PASS")
        signed = resolution["resolution"]
        (execution / "mechanical-check.json").write_text(
            json.dumps(
                {
                    "status": "PASS",
                    "mode": signed["mode"],
                    "resolved_input_sha256": resolution[
                        "resolved_input_sha256"
                    ],
                    "input_hashes": signed["hashes"],
                }
            )
            + "\n"
        )
        klean_audit_contract.reconcile_mechanical_verdict(
            execution / "verdict.json",
            execution / "mechanical-check.json",
            execution / "audit-input.json",
        )

        proof = self.cases[self.PROOF_CASE]["stage5"] / "Proof.lean"
        original = proof.read_text()
        proof.write_text(original + "\n-- changed upstream\n")
        with self.assertRaisesRegex(
            klean_audit_contract.KleanAuditContractError,
            "resolved inputs changed before Stage 6 publication",
        ):
            klean_audit_contract.publish_stage6_execution(
                self.repo,
                self.run_id,
                self.PROOF_CASE,
                execution.name,
                expected_resolved_input_sha256=resolution[
                    "resolved_input_sha256"
                ],
                expected_candidate_sha256=(
                    pipeline_contract.sha256_tree(execution)
                ),
            )
        proof.write_text(original)

        real_select = pipeline_contract.select_stage_output

        def mutate_then_select(*args, **kwargs):
            (execution / "REVIEW.md").write_text("changed before select\n")
            return real_select(*args, **kwargs)

        with mock.patch.object(
            pipeline_contract,
            "select_stage_output",
            side_effect=mutate_then_select,
        ), self.assertRaisesRegex(
            pipeline_contract.PipelineContractError,
            "candidate changed before selection",
        ):
            klean_audit_contract.publish_stage6_execution(
                self.repo,
                self.run_id,
                self.PROOF_CASE,
                execution.name,
                expected_resolved_input_sha256=resolution[
                    "resolved_input_sha256"
                ],
                expected_candidate_sha256=(
                    pipeline_contract.sha256_tree(execution)
                ),
            )


if __name__ == "__main__":
    import unittest

    unittest.main()
