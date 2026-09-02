import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.test_klean_export import KleanExportContractTests
from tools import klean_export, klean_preflight


class KleanPreflightTests(KleanExportContractTests):
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

    @staticmethod
    def build_runner(command, *, cwd, timeout):
        return 0, f"{' '.join(command)} okay"

    def rewrite_manifest_hashes(self) -> None:
        generator = self.generation / "generator-manifest.json"
        document = json.loads(generator.read_text())
        document["generated_tree_sha256"] = klean_export.tree_digest(
            self.generation / "generated"
        )
        generator.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")

    def test_good_generation_passes_clean_build_and_exact_target_gate(self) -> None:
        result = klean_preflight.check_generation(
            self.input,
            self.discovery,
            self.generation,
            toolchain_lock=self.lock,
            run_command=self.build_runner,
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["schema_version"], 3)
        self.assertEqual(
            result["stage1_workspace_sha256"],
            klean_export.tree_digest(self.input),
        )
        self.assertEqual(
            result["stage3_discovery_manifest_sha256"],
            klean_export.sha256_text(self.discovery.read_text()),
        )
        self.assertEqual(
            result["target"]["declaration"],
            "Klean8SumProduct.Lemmas.targetStatement",
        )
        self.assertEqual(result["designated_sorry_count"], 0)
        self.assertEqual(
            [entry["command"] for entry in result["diagnostics"]],
            [["lake", "clean"], ["lake", "build"]],
        )

    def test_concrete_obligation_need_not_have_an_opaque_parameter(self) -> None:
        self.assertEqual(
            klean_preflight.validate_trust_parameter_links(
                ["rule-concrete"], []
            ),
            set(),
        )

    def test_changed_stage1_input_is_rejected(self) -> None:
        (self.input / "verification.k").write_text("changed\n")
        with self.assertRaisesRegex(
            klean_preflight.KleanPreflightError, "input hash"
        ):
            klean_preflight.check_generation(
                self.input,
                self.discovery,
                self.generation,
                toolchain_lock=self.lock,
                run_command=self.build_runner,
            )

    def test_duplicate_or_mutated_target_is_rejected(self) -> None:
        lemmas = (
            self.generation
            / "generated/Klean8SumProduct/Lemmas.lean"
        )
        original = lemmas.read_text()
        for label, text in (
            (
                "duplicate",
                original
                + "\ndef targetStatement (x : Nat) : Prop := x = x\n",
            ),
            ("mutated", original.replace("external I = I", "False")),
        ):
            with self.subTest(label=label):
                lemmas.write_text(text)
                self.rewrite_manifest_hashes()
                with self.assertRaises(klean_preflight.KleanPreflightError):
                    klean_preflight.check_generation(
                        self.input,
                        self.discovery,
                        self.generation,
                        toolchain_lock=self.lock,
                        run_command=self.build_runner,
                    )
                lemmas.write_text(original)

    def test_extra_sorry_admit_unsafe_and_new_axiom_are_rejected(self) -> None:
        helper = self.generation / "generated/Helper.lean"
        cases = (
            "theorem x : True := by sorry\n",
            "theorem x : True := by admit\n",
            "unsafe def x : Nat := 0\n",
            "axiom unexpected : False\n",
        )
        for text in cases:
            with self.subTest(text=text.strip()):
                helper.write_text(text)
                self.rewrite_manifest_hashes()
                with self.assertRaises(klean_preflight.KleanPreflightError):
                    klean_preflight.check_generation(
                        self.input,
                        self.discovery,
                        self.generation,
                        toolchain_lock=self.lock,
                        run_command=self.build_runner,
                    )
                helper.unlink()

    def test_source_obligation_omission_is_rejected(self) -> None:
        mapping = self.generation / "generated/obligation-map.json"
        document = json.loads(mapping.read_text())
        document["obligations"] = []
        mapping.write_text(json.dumps(document) + "\n")
        self.rewrite_manifest_hashes()
        with self.assertRaisesRegex(
            klean_preflight.KleanPreflightError, "bijective"
        ):
            klean_preflight.check_generation(
                self.input,
                self.discovery,
                self.generation,
                toolchain_lock=self.lock,
                run_command=self.build_runner,
            )

    def test_self_consistent_manifest_cannot_weaken_mapped_target(self) -> None:
        lemmas = (
            self.generation
            / "generated/Klean8SumProduct/Lemmas.lean"
        )
        lemmas.write_text(
            lemmas.read_text().replace("external I = I", "True")
        )
        manifest = self.generation / "generator-manifest.json"
        document = json.loads(manifest.read_text())
        document["target"] = klean_export.target_statement(
            self.generation / "generated"
        )
        document["generated_tree_sha256"] = klean_export.tree_digest(
            self.generation / "generated"
        )
        manifest.write_text(
            json.dumps(document, indent=2, sort_keys=True) + "\n"
        )
        with self.assertRaisesRegex(
            klean_preflight.KleanPreflightError, "mapped obligations"
        ):
            klean_preflight.check_generation(
                self.input,
                self.discovery,
                self.generation,
                toolchain_lock=self.lock,
                run_command=self.build_runner,
            )

    def test_self_allowlisted_prop_axiom_is_rejected_by_policy(self) -> None:
        helper = self.generation / "generated/Helper.lean"
        helper.write_text("axiom bad : False\n")
        inventory = self.generation / "trust-inventory.json"
        document = json.loads(inventory.read_text())
        document["axioms"].append("bad")
        document["allowlist"].append(
            {
                "name": "bad",
                "kind": "axiom",
                "type": "False",
                "reason": "self approved",
            }
        )
        inventory.write_text(
            json.dumps(document, indent=2, sort_keys=True) + "\n"
        )
        self.rewrite_manifest_hashes()
        with self.assertRaisesRegex(
            klean_preflight.KleanPreflightError, "proposition trust"
        ):
            klean_preflight.check_generation(
                self.input,
                self.discovery,
                self.generation,
                toolchain_lock=self.lock,
                run_command=self.build_runner,
            )

    def test_build_failure_is_a_preflight_error_and_result_is_persisted(self) -> None:
        def fail_build(command, *, cwd, timeout):
            return (0, "clean") if command == ["lake", "clean"] else (1, "bad")

        result = klean_preflight.run_preflight(
            self.input,
            self.discovery,
            self.generation,
            toolchain_lock=self.lock,
            run_command=fail_build,
        )
        self.assertEqual(result["status"], "KLEAN_PREFLIGHT_ERROR")
        self.assertEqual(result["schema_version"], 3)
        self.assertEqual(
            result["stage1_workspace_sha256"],
            klean_export.tree_digest(self.input),
        )
        self.assertEqual(
            result["stage3_discovery_manifest_sha256"],
            klean_export.sha256_text(self.discovery.read_text()),
        )
        persisted = json.loads(
            (self.generation / "preflight.json").read_text()
        )
        self.assertEqual(persisted, result)
        with self.assertRaisesRegex(
            klean_preflight.KleanPreflightError, "already exists"
        ):
            klean_preflight.run_preflight(
                self.input,
                self.discovery,
                self.generation,
                toolchain_lock=self.lock,
                run_command=self.build_runner,
            )

    def test_changed_stage3_manifest_is_rejected(self) -> None:
        self.discovery.write_text(self.discovery.read_text() + "\n")
        with self.assertRaisesRegex(
            klean_preflight.KleanPreflightError, "Stage 3"
        ):
            klean_preflight.check_generation(
                self.input,
                self.discovery,
                self.generation,
                toolchain_lock=self.lock,
                run_command=self.build_runner,
            )

    def test_self_consistent_manifest_cannot_replace_inventory_hash(
        self,
    ) -> None:
        input_manifest = self.generation / "input-manifest.json"
        input_document = json.loads(input_manifest.read_text())
        input_document["inventory_sha256"] = "0" * 64
        input_manifest.write_text(
            json.dumps(input_document, indent=2, sort_keys=True) + "\n"
        )
        generator_manifest = self.generation / "generator-manifest.json"
        generator_document = json.loads(generator_manifest.read_text())
        generator_document["provenance"]["inventory_sha256"] = "0" * 64
        generator_manifest.write_text(
            json.dumps(generator_document, indent=2, sort_keys=True) + "\n"
        )
        with self.assertRaisesRegex(
            klean_preflight.KleanPreflightError, "inventory"
        ):
            klean_preflight.check_generation(
                self.input,
                self.discovery,
                self.generation,
                toolchain_lock=self.lock,
                run_command=self.build_runner,
            )

    def test_input_mutation_during_clean_build_is_rejected(self) -> None:
        def mutating_build(command, *, cwd, timeout):
            if command == ["lake", "clean"]:
                self.discovery.write_text(
                    self.discovery.read_text() + "\n"
                )
            return 0, "okay"

        with self.assertRaisesRegex(
            klean_preflight.KleanPreflightError, "during preflight"
        ):
            klean_preflight.check_generation(
                self.input,
                self.discovery,
                self.generation,
                toolchain_lock=self.lock,
                run_command=mutating_build,
            )

    def test_export_result_binds_every_schema_v3_hash_and_count(self) -> None:
        path = self.generation / "export-result.json"
        original = path.read_text()
        document = json.loads(original)
        cases = {
            "frozen_input_sha256": "0" * 64,
            "stage3_discovery_manifest_sha256": "0" * 64,
            "generated_tree_sha256": "0" * 64,
            "trust_inventory_sha256": "0" * 64,
            "obligation_count": document["obligation_count"] + 1,
        }
        for key, value in cases.items():
            with self.subTest(key=key):
                mutated = {**document, key: value}
                path.write_text(
                    json.dumps(mutated, indent=2, sort_keys=True) + "\n"
                )
                with self.assertRaisesRegex(
                    klean_preflight.KleanPreflightError,
                    "export result",
                ):
                    klean_preflight.check_generation(
                        self.input,
                        self.discovery,
                        self.generation,
                        toolchain_lock=self.lock,
                        run_command=self.build_runner,
                    )
                path.write_text(original)

    def test_trust_inventory_bytes_are_bound_to_export_result(self) -> None:
        inventory = self.generation / "trust-inventory.json"
        inventory.write_text(inventory.read_text() + "\n")
        with self.assertRaisesRegex(
            klean_preflight.KleanPreflightError, "trust inventory"
        ):
            klean_preflight.check_generation(
                self.input,
                self.discovery,
                self.generation,
                toolchain_lock=self.lock,
                run_command=self.build_runner,
            )

    def test_generated_injection_during_clean_cannot_persist_pass(self) -> None:
        def injecting_build(command, *, cwd, timeout):
            if command == ["lake", "clean"]:
                self.generation.joinpath(
                    "generated/Injected.lean"
                ).write_text("theorem injected : True := by sorry\n")
            return 0, "okay"

        result = klean_preflight.run_preflight(
            self.input,
            self.discovery,
            self.generation,
            toolchain_lock=self.lock,
            run_command=injecting_build,
        )
        self.assertEqual(result["status"], "KLEAN_PREFLIGHT_ERROR")
        self.assertNotEqual(
            json.loads(
                (self.generation / "preflight.json").read_text()
            )["status"],
            "PASS",
        )

    def test_sidecar_mutation_during_build_is_rejected(self) -> None:
        for name in (
            "input-manifest.json",
            "generator-manifest.json",
            "trust-inventory.json",
            "export-result.json",
        ):
            with self.subTest(name=name):
                path = self.generation / name
                original = path.read_text()

                def mutating_build(command, *, cwd, timeout):
                    if command == ["lake", "clean"]:
                        path.write_text(original + "\n")
                    return 0, "okay"

                with self.assertRaisesRegex(
                    klean_preflight.KleanPreflightError,
                    "changed during preflight",
                ):
                    klean_preflight.check_generation(
                        self.input,
                        self.discovery,
                        self.generation,
                        toolchain_lock=self.lock,
                        run_command=mutating_build,
                    )
                path.write_text(original)

    def test_atomic_preflight_rechecks_after_check_generation(self) -> None:
        real_check = klean_preflight.check_generation

        def check_then_mutate(*args, **kwargs):
            result = real_check(*args, **kwargs)
            manifest = self.generation / "input-manifest.json"
            manifest.write_text(manifest.read_text() + "\n")
            return result

        with mock.patch.object(
            klean_preflight,
            "check_generation",
            side_effect=check_then_mutate,
        ):
            result = klean_preflight.run_preflight(
                self.input,
                self.discovery,
                self.generation,
                toolchain_lock=self.lock,
                run_command=self.build_runner,
            )
        self.assertEqual(result["status"], "KLEAN_PREFLIGHT_ERROR")


if __name__ == "__main__":
    unittest.main()
