import copy
import json
from pathlib import Path

from tests.test_klean_export import (
    KleanExportContractTests,
    write_discovery_manifest,
)
from tools import (
    klean_audit_contract,
    klean_export,
    klean_final_gate,
    pipeline_contract,
)


class KleanFinalGateTests(KleanExportContractTests):
    def test_axiom_parser_accepts_axiom_free_proof(self) -> None:
        self.assertEqual(
            klean_final_gate._parse_axioms(
                "'Proof.final' does not depend on any axioms\n"
            ),
            set(),
        )

    def test_axiom_parser_preserves_quoted_names_with_commas_and_brackets(
        self,
    ) -> None:
        self.assertEqual(
            klean_final_gate._parse_axioms(
                "'Proof.final' depends on axioms: ["
                "«Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int»,\n"
                " «_[_<-undef]»,\n"
                " Classical.choice]\n"
            ),
            {
                "«Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int»",
                "«_[_<-undef]»",
                "Classical.choice",
            },
        )

    def setUp(self) -> None:
        super().setUp()
        self.generation = self.root / "generation"
        klean_export.export_frozen(
            self.input,
            self.discovery,
            self.generation,
            problem="8-sum-product",
            toolchain_lock=self.lock,
            run_command=self.fake_runner,
        )
        self.candidate = self.root / "candidate"
        self.candidate.mkdir()
        (self.candidate / "lean-toolchain").write_text(
            "leanprover/lean4:v4.22.0\n"
        )
        (self.candidate / "lakefile.lean").write_text(
            "import Lake\n"
            "open Lake DSL\n"
            'package "proof"\n'
            'require «klean-8-sum-product» from "./Base"\n'
            "@[default_target]\n"
            "lean_lib Proof\n"
        )
        (self.candidate / "Proof.lean").write_text(
            "import Klean8SumProduct.Lemmas\n\n"
            "namespace Proof\n\n"
            "def external (value : Int) : Int := value\n\n"
            "theorem final :\n"
            "    Klean8SumProduct.Lemmas.targetStatement external := by\n"
            "  simp [Klean8SumProduct.Lemmas.targetStatement, external]\n\n"
            "end Proof\n"
        )
        self.audit_input = self.root / "audit-input.json"
        self.write_audit_input()

    def write_audit_input(
        self,
        *,
        mode: str = "CLASSIFICATION_AND_PROOF",
        discovery: Path | None = None,
        generation: Path | None = None,
        candidate: Path | None = None,
    ) -> None:
        discovery = self.discovery if discovery is None else discovery
        generation = self.generation if generation is None else generation
        candidate = (
            self.candidate
            if candidate is None and mode == "CLASSIFICATION_AND_PROOF"
            else candidate
        )
        resolution = {
            "schema_version": 3,
            "run_id": "test-run",
            "problem_id": "8-sum-product",
            "mode": mode,
            "condition": "kit-semantics",
            "semantics_mode": "SUPPLIED_SEMANTICS",
            "k_workspace": str(self.input),
            "k_audit": "/reference/k-audit",
            "discovery_manifest": str(discovery),
            "klean_generation": str(generation),
            "lean_workspace": (
                str(candidate) if candidate is not None else None
            ),
            "lean_invocation": (
                "/reference/lean-invocation"
                if candidate is not None
                else None
            ),
            "target": {"statement": "signed target"},
            "stage1_source_hashes": {
                "verification.k": "b" * 64,
            },
            "trust_inventory": str(
                generation / "trust-inventory.json"
            ),
            "selections": {
                "k_audit": {"artifact_sha256": "c" * 64},
                "klean_generation": {
                    "artifact_sha256": "d" * 64,
                },
            },
            "stage4_preflight": {"status": "PASS"},
            "stage5_result": (
                {"status": "SUCCEEDED"}
                if candidate is not None
                else None
            ),
            "hashes": {
                "k_workspace_sha256": (
                    pipeline_contract.sha256_tree(self.input)
                ),
                "stage1_export_sha256": (
                    klean_export.tree_digest(self.input)
                ),
                "discovery_manifest_sha256": (
                    pipeline_contract.sha256_file(discovery)
                ),
                "klean_generation_sha256": (
                    pipeline_contract.sha256_tree(generation)
                ),
                "lean_workspace_sha256": (
                    pipeline_contract.sha256_tree(candidate)
                    if candidate is not None
                    else None
                ),
            },
        }
        self.audit_input.write_text(
            json.dumps(
                {
                    "schema_version": 3,
                    "resolution": resolution,
                    "resolved_input_sha256": (
                        klean_audit_contract._canonical_json_sha256(
                            resolution
                        )
                    ),
                    "audit": {
                        "image_id": "sha256:test-auditor",
                        "output": "/audit-output",
                    },
                }
            )
            + "\n"
        )

    def test_signed_resolution_tampering_is_rejected_before_mechanical_work(
        self,
    ) -> None:
        original = json.loads(self.audit_input.read_text())
        mutations = {
            "condition": lambda signed: signed.__setitem__(
                "condition", "bare"
            ),
            "mode": lambda signed: signed.__setitem__(
                "mode", "CLASSIFICATION_ONLY"
            ),
            "target": lambda signed: signed.__setitem__(
                "target", {"statement": "True"}
            ),
            "source_hashes": lambda signed: signed[
                "stage1_source_hashes"
            ].__setitem__("verification.k", "d" * 64),
            "selections": lambda signed: signed[
                "selections"
            ].__setitem__(
                "k_audit", {"artifact_sha256": "e" * 64}
            ),
        }
        for label, mutate in mutations.items():
            with self.subTest(field=label):
                document = copy.deepcopy(original)
                signed = document["resolution"]
                mutate(signed)
                self.audit_input.write_text(json.dumps(document) + "\n")
                with self.assertRaisesRegex(
                    klean_final_gate.KleanFinalGateError,
                    "digest does not match signed resolution",
                ):
                    klean_final_gate.check_final(
                        self.input,
                        self.discovery,
                        self.generation,
                        self.candidate,
                        toolchain_lock=self.lock,
                        audit_input=self.audit_input,
                        run_command=self.runner,
                    )

    def test_unsigned_audit_metadata_does_not_invalidate_signature(
        self,
    ) -> None:
        document = json.loads(self.audit_input.read_text())
        document["audit"]["runtime_note"] = "launcher-owned metadata"
        self.audit_input.write_text(json.dumps(document) + "\n")

        result = klean_final_gate.check_final(
            self.input,
            self.discovery,
            self.generation,
            self.candidate,
            toolchain_lock=self.lock,
            audit_input=self.audit_input,
            run_command=self.runner,
        )

        self.assertEqual(result["status"], "PASS")

    @staticmethod
    def runner(command, *, cwd, timeout):
        if command == ["lake", "env", "lean", "AxiomAudit.lean"]:
            return 0, "'Proof.final' depends on axioms: []\n"
        return 0, f"{' '.join(command)} okay\n"

    def rewrite_generated_hash(self, generation: Path) -> None:
        manifest = generation / "generator-manifest.json"
        document = json.loads(manifest.read_text())
        document["generated_tree_sha256"] = klean_export.tree_digest(
            generation / "generated"
        )
        manifest.write_text(
            json.dumps(document, indent=2, sort_keys=True) + "\n"
        )

    def test_clean_exact_axiom_accounted_proof_passes(self) -> None:
        result = klean_final_gate.check_final(
            self.input,
            self.discovery,
            self.generation,
            self.candidate,
            toolchain_lock=self.lock,
            audit_input=self.audit_input,
            run_command=self.runner,
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["mode"], "CLASSIFICATION_AND_PROOF")
        self.assertEqual(
            result["semantic_classification"], "NOT_EVALUATED"
        )
        self.assertEqual(
            result["target"]["statement"],
            "Klean8SumProduct.Lemmas.targetStatement external",
        )
        self.assertEqual(
            [item["command"] for item in result["diagnostics"]],
            [
                ["lake", "clean"],
                ["lake", "build"],
                ["lake", "env", "lean", "AxiomAudit.lean"],
            ],
        )

    def test_trust_binding_may_be_defined_once_in_imported_candidate_file(
        self,
    ) -> None:
        proof = self.candidate / "Proof.lean"
        proof.write_text(
            proof.read_text()
            .replace(
                "import Klean8SumProduct.Lemmas",
                "import Proof.Model",
            )
            .replace(
                "def external (value : Int) : Int := value\n\n",
                "",
            )
        )
        model = self.candidate / "Proof/Model.lean"
        model.parent.mkdir()
        model.write_text(
            "import Klean8SumProduct.Lemmas\n\n"
            "namespace Proof\n\n"
            "def external (value : Int) : Int := value\n\n"
            "end Proof\n"
        )

        result = klean_final_gate.check_proof_candidate(
            self.generation,
            self.candidate,
            run_command=self.runner,
        )

        self.assertEqual(result["status"], "PASS")

    def test_trust_binding_may_have_a_lean_attribute(self) -> None:
        proof = self.candidate / "Proof.lean"
        proof.write_text(
            proof.read_text().replace(
                "def external (value : Int) : Int := value",
                "@[simp] noncomputable def external (value : Int) : Int := value",
            )
        )

        result = klean_final_gate.check_proof_candidate(
            self.generation,
            self.candidate,
            run_command=self.runner,
        )

        self.assertEqual(result["status"], "PASS")

    def test_duplicate_trust_binding_across_candidate_files_is_rejected(
        self,
    ) -> None:
        duplicate = self.candidate / "Duplicate.lean"
        duplicate.write_text(
            "namespace Proof\n"
            "def external (value : Int) : Int := value\n"
            "end Proof\n"
        )

        with self.assertRaisesRegex(
            klean_final_gate.KleanFinalGateError,
            "must define exact trust binding 'external' once",
        ):
            klean_final_gate.check_proof_candidate(
                self.generation,
                self.candidate,
                run_command=self.runner,
            )

    def test_axiom_audit_elaborates_target_in_proof_namespace(self) -> None:
        def namespace_sensitive_runner(command, *, cwd, timeout):
            if command == ["lake", "env", "lean", "AxiomAudit.lean"]:
                source = (cwd / "AxiomAudit.lean").read_text()
                if "namespace Proof" not in source:
                    return 1, (
                        "Application type mismatch: target parameter "
                        "resolved to an imported root declaration\n"
                    )
                return 0, "'Proof.final' depends on axioms: []\n"
            return 0, f"{' '.join(command)} okay\n"

        result = klean_final_gate.check_final(
            self.input,
            self.discovery,
            self.generation,
            self.candidate,
            toolchain_lock=self.lock,
            audit_input=self.audit_input,
            run_command=namespace_sensitive_runner,
        )

        self.assertEqual(result["status"], "PASS")

    def test_empty_stage5_base_mountpoint_does_not_block_audit(self) -> None:
        (self.candidate / "Base").mkdir()
        self.write_audit_input()

        result = klean_final_gate.check_final(
            self.input,
            self.discovery,
            self.generation,
            self.candidate,
            toolchain_lock=self.lock,
            audit_input=self.audit_input,
            run_command=self.runner,
        )

        self.assertEqual(result["status"], "PASS")

    def test_classification_only_checks_genuinely_empty_domain_set(
        self,
    ) -> None:
        discovery = write_discovery_manifest(
            self.input,
            self.root / "summary-only.json",
            ["DEFINITION", "DEFINITION"],
        )
        generation = self.root / "no-obligations"
        export = klean_export.export_frozen(
            self.input,
            discovery,
            generation,
            problem="8-sum-product",
            toolchain_lock=self.lock,
            run_command=self.fake_runner,
        )
        self.assertEqual(export["status"], "KLEAN_NO_OBLIGATIONS")
        self.write_audit_input(
            mode="CLASSIFICATION_ONLY",
            discovery=discovery,
            generation=generation,
            candidate=None,
        )

        result = klean_final_gate.check_final(
            self.input,
            discovery,
            generation,
            None,
            toolchain_lock=self.lock,
            audit_input=self.audit_input,
            run_command=self.runner,
        )

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["mode"], "CLASSIFICATION_ONLY")
        self.assertIsNone(result["target"])
        self.assertIsNone(result["candidate_sha256"])
        self.assertEqual(result["used_axioms"], [])
        self.assertEqual(
            result["semantic_classification"], "NOT_EVALUATED"
        )

    def test_candidate_presence_must_match_mechanical_mode(self) -> None:
        with self.assertRaisesRegex(
            klean_final_gate.KleanFinalGateError,
            "requires a Stage 5 Lean candidate",
        ):
            klean_final_gate.check_final(
                self.input,
                self.discovery,
                self.generation,
                None,
                toolchain_lock=self.lock,
                audit_input=self.audit_input,
                run_command=self.runner,
            )

        discovery = write_discovery_manifest(
            self.input,
            self.root / "empty.json",
            ["DEFINITION", "DEFINITION"],
        )
        generation = self.root / "empty-generation"
        klean_export.export_frozen(
            self.input,
            discovery,
            generation,
            problem="8-sum-product",
            toolchain_lock=self.lock,
            run_command=self.fake_runner,
        )
        self.write_audit_input(
            mode="CLASSIFICATION_ONLY",
            discovery=discovery,
            generation=generation,
            candidate=None,
        )
        with self.assertRaisesRegex(
            klean_final_gate.KleanFinalGateError,
            "must not use a Stage 5 Lean candidate",
        ):
            klean_final_gate.check_final(
                self.input,
                discovery,
                generation,
                self.candidate,
                toolchain_lock=self.lock,
                audit_input=self.audit_input,
                run_command=self.runner,
            )

    def test_manifest_bijection_is_rechecked_by_final_gate(self) -> None:
        mapping = self.generation / "generated/obligation-map.json"
        document = json.loads(mapping.read_text())
        document["obligations"] = []
        mapping.write_text(json.dumps(document) + "\n")
        self.rewrite_generated_hash(self.generation)
        self.write_audit_input()
        with self.assertRaisesRegex(
            klean_final_gate.KleanFinalGateError, "bijective"
        ):
            klean_final_gate.check_final(
                self.input,
                self.discovery,
                self.generation,
                self.candidate,
                toolchain_lock=self.lock,
                audit_input=self.audit_input,
                run_command=self.runner,
            )

    def test_candidate_holes_new_trust_and_wrong_target_are_rejected(
        self,
    ) -> None:
        proof = self.candidate / "Proof.lean"
        original = proof.read_text()
        cases = (
            ("sorry", original.replace("simp [", "sorry\n  -- ")),
            ("opaque", original.replace("def external", "opaque external")),
            (
                "target",
                original.replace(
                    "Klean8SumProduct.Lemmas.targetStatement external",
                    "True",
                ),
            ),
        )
        for label, text in cases:
            with self.subTest(label=label):
                proof.write_text(text)
                with self.assertRaises(
                    klean_final_gate.KleanFinalGateError
                ):
                    klean_final_gate.check_final(
                        self.input,
                        self.discovery,
                        self.generation,
                        self.candidate,
                        toolchain_lock=self.lock,
                        audit_input=self.audit_input,
                        run_command=self.runner,
                    )
        proof.write_text(original)

    def test_sorry_axiom_dependency_is_rejected(self) -> None:
        def sorry_runner(command, *, cwd, timeout):
            if command == ["lake", "env", "lean", "AxiomAudit.lean"]:
                return 0, (
                    "'Proof.final' depends on axioms: "
                    "[sorryAx, Classical.choice]\n"
                )
            return 0, "okay\n"

        with self.assertRaisesRegex(
            klean_final_gate.KleanFinalGateError, "sorryAx"
        ):
            klean_final_gate.check_final(
                self.input,
                self.discovery,
                self.generation,
                self.candidate,
                toolchain_lock=self.lock,
                audit_input=self.audit_input,
                run_command=sorry_runner,
            )

    def test_candidate_mutation_during_clean_build_is_rejected(self) -> None:
        original = (self.candidate / "Proof.lean").read_text()
        build_count = 0

        def mutating_runner(command, *, cwd, timeout):
            nonlocal build_count
            if command == ["lake", "build"]:
                build_count += 1
            if command == ["lake", "build"] and build_count == 2:
                (self.candidate / "Proof.lean").write_text(
                    original + "\n-- raced\n"
                )
            return self.runner(command, cwd=cwd, timeout=timeout)

        with self.assertRaisesRegex(
            klean_final_gate.KleanFinalGateError,
            "candidate changed during mechanical audit",
        ):
            klean_final_gate.check_final(
                self.input,
                self.discovery,
                self.generation,
                self.candidate,
                toolchain_lock=self.lock,
                audit_input=self.audit_input,
                run_command=mutating_runner,
            )


if __name__ == "__main__":
    import unittest

    unittest.main()
