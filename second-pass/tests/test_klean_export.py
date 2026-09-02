import json
import os
import stat
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from tools import klean, klean_export
from tools import k_rule_inventory
from tools.k_rule_inventory import inventory_verification


def write_discovery_manifest(
    workspace: Path,
    destination: Path,
    classifications: list[str],
) -> Path:
    inventory = inventory_verification(workspace)
    if len(classifications) != len(inventory["rules"]):
        raise AssertionError("classification count differs from rule inventory")
    destination.write_text(
        json.dumps(
            {
                "schema_version": 2,
                "inventory_sha256": inventory["inventory_sha256"],
                "rules": [
                    {
                        "source_rule_id": rule["source_rule_id"],
                        "classification": classification,
                        "rationale": f"Test classification: {classification}.",
                    }
                    for rule, classification in zip(
                        inventory["rules"], classifications, strict=True
                    )
                ],
            }
        )
        + "\n"
    )
    return destination


class KleanTransformTests(unittest.TestCase):
    def test_generated_wildcard_constraint_substitutes_across_rule(self) -> None:
        @dataclass(frozen=True)
        class Var:
            name: str
            sort: str = "SortBool"

            @property
            def patterns(self):
                return ()

            def bottom_up(self, transform):
                return transform(self)

        @dataclass(frozen=True)
        class Term:
            name: str
            patterns: tuple[object, ...] = ()

            def bottom_up(self, transform):
                return transform(
                    Term(
                        self.name,
                        tuple(
                            child.bottom_up(transform)
                            for child in self.patterns
                        ),
                    )
                )

        @dataclass(frozen=True)
        class And(Term):
            @property
            def ops(self):
                return self.patterns

            def bottom_up(self, transform):
                return transform(
                    And(
                        self.name,
                        tuple(
                            child.bottom_up(transform)
                            for child in self.patterns
                        ),
                    )
                )

        false = Term("false")
        wildcard = Var("Var'Unds'Gen0")
        lhs = Term("firstAfter", (And("and", (false, wildcard)),))

        normalized_lhs, normalized_rhs = (
            klean.normalize_generated_wildcards(
                (lhs, wildcard),
                evar_type=Var,
                and_type=And,
            )
        )

        self.assertEqual(normalized_lhs, Term("firstAfter", (false,)))
        self.assertEqual(normalized_rhs, false)

    def test_top_cell_obligation_is_rewrite_not_equality(self) -> None:
        self.assertEqual(
            klean.lean_rule_relation(
                "left", "right", "SortGeneratedTopCell"
            ),
            "Rewrites left right",
        )
        self.assertEqual(
            klean.lean_rule_relation("left", "right", "SortBool"),
            "(left : SortBool) = (right : SortBool)",
        )

    def test_only_top_cell_trust_rules_are_removed_from_rewrites(self) -> None:
        self.assertEqual(
            klean.operational_trust_rewrite_uid(
                "top-rule", "SortGeneratedTopCell"
            ),
            "top-rule",
        )
        self.assertIsNone(
            klean.operational_trust_rewrite_uid(
                "function-rule", "SortValSeq"
            )
        )

    def test_rhs_only_variables_are_existential_inside_rule_inputs(self) -> None:
        self.assertEqual(
            klean.lean_quantified_obligation(
                "Rewrites left right",
                universal_binders=("(x : SortInt)",),
                existential_binders=("(result : SortInt)",),
                hypotheses=("(h : condition = true)",),
            ),
            "∀ (x : SortInt) (h : condition = true), "
            "∃ (result : SortInt), Rewrites left right",
        )

    def test_k_equality_requires_becomes_lean_equality(self) -> None:
        render = getattr(
            klean,
            "lean_requires_proposition",
            lambda term: f"({term}) = true",
        )
        self.assertEqual(
            render("«_==K_» (left x) (right y)"),
            "(left x) = (right y)",
        )
        self.assertEqual(
            render("predicate x"),
            "(predicate x) = true",
        )
        is_k_equality = getattr(
            klean, "is_k_equality_identifier", lambda _identifier: False
        )
        self.assertTrue(is_k_equality("«_==K_»"))

    def test_klean_dependency_order_is_canonical(self) -> None:
        left = {
            "rule-b": frozenset({"func-b"}),
            "func-a": frozenset({"rule-a"}),
            "rule-a": frozenset(),
            "func-b": frozenset({"rule-b"}),
        }
        right = dict(reversed(tuple(left.items())))

        self.assertEqual(
            klean.deterministic_ordered_sccs(left),
            klean.deterministic_ordered_sccs(right),
        )
        self.assertEqual(
            klean.deterministic_subsort_pairs(
                {
                    "SortKItem": frozenset({"SortString", "SortInt"}),
                    "SortInt": frozenset({"SortNat"}),
                }
            ),
            (
                ("SortNat", "SortInt"),
                ("SortInt", "SortKItem"),
                ("SortString", "SortKItem"),
            ),
        )

    def test_canonicalizes_nested_explicit_subsort_injections(self) -> None:
        subsorts = {
            "SortVal": frozenset({"SortInt"}),
            "SortKItem": frozenset({"SortVal"}),
        }
        self.assertEqual(
            klean.canonicalize_lean_injection_chains(
                "SortKItem.inj_SortVal (SortVal.inj_SortInt SECOND)",
                subsorts,
            ),
            "SortKItem.inj_SortInt SECOND",
        )
        self.assertEqual(
            klean.canonicalize_lean_injection_chains(
                "f (SortKItem.inj_SortVal "
                "(SortVal.inj_SortInt (g SECOND))) CONT",
                subsorts,
            ),
            "f (SortKItem.inj_SortInt (g SECOND)) CONT",
        )

    def test_does_not_collapse_unrelated_explicit_injections(self) -> None:
        text = "SortKItem.inj_SortVal (SortVal.inj_SortInt SECOND)"
        self.assertEqual(
            klean.canonicalize_lean_injection_chains(
                text,
                {"SortVal": frozenset({"SortInt"})},
            ),
            text,
        )

    def test_uses_dynamic_injection_for_nonleaf_subsort_values(self) -> None:
        subsorts = {
            "SortVal": frozenset({"SortInt", "SortString"}),
            "SortKItem": frozenset({"SortVal"}),
        }
        self.assertEqual(
            klean.canonicalize_lean_injection_chains(
                "SortKItem.inj_SortVal (nsScan INPUT S N C)",
                subsorts,
            ),
            "(@inj SortVal SortKItem) (nsScan INPUT S N C)",
        )

    def test_parses_verification_module_and_summary_functions(self) -> None:
        module, functions = klean_export.parse_verification(
            """
module FOO-VERIFICATION
  syntax Int ::= count ( List , Int ) [function, total]
  syntax Bool ::= opaque() [function]
  syntax Int ::= ignored(Int) [constructor]
endmodule
"""
        )
        self.assertEqual(module, "FOO-VERIFICATION")
        self.assertEqual(
            [(item.name, item.ret, item.args) for item in functions],
            [
                ("count", "Int", ["List", "Int"]),
                ("opaque", "Bool", []),
            ],
        )

    def test_parses_every_multiline_syntax_alternative(self) -> None:
        module, functions = klean_export.parse_verification(
            """
module FOO-VERIFICATION
  syntax Int ::= sumFold(IntSeq, Int) [function, total]
               | productFold(IntSeq, Int) [function, total]
               | lastInt(IntSeq, Int) [function, total]
  syntax Bool ::= ignored(Int) [constructor]
endmodule
"""
        )
        self.assertEqual(module, "FOO-VERIFICATION")
        self.assertEqual(
            [item.name for item in functions],
            ["sumFold", "productFold", "lastInt"],
        )

    def test_desimplifies_only_exact_classified_rule_ids(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            verification = workspace / "verification.k"
            source = (
                "module FOO-VERIFICATION\n"
                "  syntax Int ::= summary(Int) [function]\n"
                '  rule summary(I) => token("rule", I) '
                "[simplification] // DOMAIN_LEMMA despite its head\n"
                "  // rule summary(J) => J [simplification]\n"
                '  rule bridge("rule", summary(I))\n'
                "    => ruleTerm(I)\n"
                "    [concrete,\n"
                "     simplification] // DEFINITION despite its head\n"
                "  rule other(I) => summary(I) [simplification]\n"
                "endmodule\n"
            )
            verification.write_text(source)
            inventory = inventory_verification(workspace)
            domain_head, summary_bridge, domain_rhs = inventory["rules"]

            result = k_rule_inventory.desimplify_rule_ids(
                verification.read_text(),
                [summary_bridge["source_rule_id"]],
            )

        self.assertEqual(result.count("\n"), source.count("\n"))
        self.assertIn(
            'rule summary(I) => token("rule", I) [simplification]',
            result,
        )
        self.assertIn(
            "rule other(I) => summary(I) [simplification]",
            result,
        )
        self.assertIn("// rule summary(J) => J [simplification]", result)
        self.assertNotIn(
            "simplification] // DEFINITION",
            result,
        )
        self.assertIn("[concrete", result)
        self.assertEqual(
            {
                domain_head["source_rule_id"],
                domain_rhs["source_rule_id"],
            },
            {
                rule["source_rule_id"]
                for rule in inventory["rules"]
                if "[simplification]" in rule["text"]
            },
        )

    def test_exact_rule_transform_rejects_unknown_or_duplicate_ids(self) -> None:
        source = (
            "module FOO-VERIFICATION\n"
            "  rule X => X [simplification]\n"
            "endmodule\n"
        )
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            (workspace / "verification.k").write_text(source)
            rule_id = inventory_verification(workspace)["rules"][0][
                "source_rule_id"
            ]
        for selected, message in (
            ([rule_id, rule_id], "duplicate"),
            (["rule-" + "0" * 64], "unknown"),
        ):
            with self.subTest(selected=selected):
                with self.assertRaisesRegex(
                    k_rule_inventory.KRuleInventoryError,
                    message,
                ):
                    k_rule_inventory.desimplify_rule_ids(source, selected)

    def test_klean_input_contains_only_exact_discovered_domain_lemmas(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            (workspace / "verification.k").write_text(
                "module FOO-VERIFICATION\n"
                "  imports FOO-SYNTAX\n"
                "  syntax Int ::= summary(Int) [function]\n"
                "  syntax Int ::= other(Int) [function]\n"
                "  rule summary(I) => I [simplification]\n"
                "  rule other(I) => I [simplification]\n"
                "endmodule\n"
            )
            (workspace / "syntax.k").write_text(
                "module FOO-SYNTAX\nendmodule\n"
            )
            destination = workspace / "destination"
            destination.mkdir()
            discovery = write_discovery_manifest(
                workspace,
                workspace / "validated-trust-boundary.json",
                [
                    "DOMAIN_LEMMA",
                    "DEFINITION",
                ],
            )
            canonical = inventory_verification(workspace)["rules"][0]
            lock = workspace / "lock.json"
            lock.write_text(
                json.dumps(
                    {
                        "runtimeverification_k_commit": "k-commit",
                        "pyk_project": "pyk",
                        "lean_toolchain": "leanprover/lean4:v4.22.0",
                    }
                )
                + "\n"
            )
            captured: dict[str, object] = {}

            def runner(command, *, cwd, timeout, env, shell=False):
                if command[0] == "kompile":
                    captured["export_text"] = Path(command[1]).read_text()
                    captured["verification_text"] = (
                        Path(cwd) / "definition-source/verification.k"
                    ).read_text()
                    captured["syntax_module"] = command[
                        command.index("--syntax-module") + 1
                    ]
                    definition = Path(
                        command[command.index("--output-definition") + 1]
                    )
                    definition.mkdir()
                    (definition / "definition.kore").write_text("[]\n")
                    return 0, "kompiled"
                if "--source-rule-inventory" in command:
                    inventory_path = Path(
                        command[
                            command.index("--source-rule-inventory") + 1
                        ]
                    )
                    captured.update(json.loads(inventory_path.read_text()))
                    return 1, "stop after capturing inventory"
                raise AssertionError(command)

            with self.assertRaisesRegex(
                klean_export.KleanExportError, "klean failed"
            ):
                klean_export.export_frozen(
                    workspace,
                    discovery,
                    destination / "export",
                    problem="example",
                    toolchain_lock=lock,
                    run_command=runner,
                )

        source_rules = captured["source_rules"]
        self.assertEqual(captured["syntax_module"], "FOO-SYNTAX")
        export_text = str(captured["export_text"])
        self.assertIn("definition-source/verification.k", export_text)
        verification_text = str(captured["verification_text"])
        self.assertIn(
            "rule summary(I) => I [simplification]",
            verification_text,
        )
        self.assertIn(
            "rule other(I) => I [simplification]",
            verification_text,
        )
        self.assertEqual(
            [item["classification"] for item in source_rules],
            ["TRUST_OBLIGATION"],
        )
        self.assertEqual(
            source_rules[0]["start_line"],
            canonical["start_line"],
        )
        self.assertEqual(
            [set(item) for item in source_rules],
            [
                {
                    "source_rule_id",
                    "start_line",
                    "end_line",
                    "normalized_sha256",
                    "classification",
                }
            ],
        )
        for item in source_rules:
            self.assertEqual(
                item["source_rule_id"],
                "rule-" + item["normalized_sha256"],
            )

    def test_untagged_domain_lemma_reaches_exact_source_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            (workspace / "verification.k").write_text(
                "module FOO-SYNTAX\nendmodule\n"
                "module FOO-VERIFICATION\n"
                "  imports FOO-SYNTAX\n"
                "  syntax Int ::= summary(Int) [function]\n"
                "  rule X +Int 0 => X\n"
                "endmodule\n"
            )
            discovery = write_discovery_manifest(
                workspace,
                workspace / "validated-trust-boundary.json",
                ["DOMAIN_LEMMA"],
            )
            lock = workspace / "lock.json"
            lock.write_text(
                json.dumps(
                    {
                        "runtimeverification_k_commit": "k-commit",
                        "pyk_project": "pyk",
                        "lean_toolchain": "leanprover/lean4:v4.22.0",
                    }
                )
                + "\n"
            )
            destination = workspace / "destination"
            destination.mkdir()

            captured: dict[str, object] = {}

            def runner(command, *, cwd, timeout, env, shell=False):
                if command[0] == "kompile":
                    definition = Path(
                        command[command.index("--output-definition") + 1]
                    )
                    definition.mkdir()
                    (definition / "definition.kore").write_text("[]\n")
                    return 0, "kompiled"
                if "--source-rule-inventory" in command:
                    inventory_path = Path(
                        command[
                            command.index("--source-rule-inventory") + 1
                        ]
                    )
                    captured.update(json.loads(inventory_path.read_text()))
                    return 1, "stop after capturing inventory"
                raise AssertionError(command)

            with self.assertRaisesRegex(
                klean_export.KleanExportError, "klean failed"
            ):
                klean_export.export_frozen(
                    workspace,
                    discovery,
                    destination / "export",
                    problem="example",
                    toolchain_lock=lock,
                    run_command=runner,
                )

        self.assertEqual(
            [item["classification"] for item in captured["source_rules"]],
            ["TRUST_OBLIGATION"],
        )

    def test_referenced_structural_definition_is_exported_as_function(self) -> None:
        """Catch loss of nested K reduction for a selected domain lemma."""

        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            (workspace / "verification.k").write_text(
                "module FOO-SYNTAX\n"
                "  syntax Seq ::= empty | cons(Int, Seq)\n"
                "  syntax Seq ::= snoc(Seq, Int)\n"
                "  syntax Int ::= last(Seq)\n"
                "endmodule\n"
                "module FOO-VERIFICATION\n"
                "  imports FOO-SYNTAX\n"
                "  rule snoc(empty, V:Int) => cons(V, empty)\n"
                "  rule snoc(cons(H:Int, T:Seq), V:Int)\n"
                "    => cons(H, snoc(T, V))\n"
                "  rule last(cons(H:Int, snoc(T:Seq, V:Int))) => V "
                "[priority(40)]\n"
                "endmodule\n"
            )
            discovery = write_discovery_manifest(
                workspace,
                workspace / "validated-trust-boundary.json",
                ["DEFINITION", "DEFINITION", "DOMAIN_LEMMA"],
            )
            lock = workspace / "lock.json"
            lock.write_text(
                json.dumps(
                    {
                        "runtimeverification_k_commit": "k-commit",
                        "pyk_project": "pyk",
                        "lean_toolchain": "leanprover/lean4:v4.22.0",
                    }
                )
                + "\n"
            )
            destination = workspace / "destination"
            destination.mkdir()
            captured: dict[str, str] = {}

            def runner(command, *, cwd, timeout, env, shell=False):
                if command[0] == "kompile":
                    captured["verification"] = (
                        Path(cwd) / "definition-source/verification.k"
                    ).read_text()
                    definition = Path(
                        command[command.index("--output-definition") + 1]
                    )
                    definition.mkdir()
                    (definition / "definition.kore").write_text("[]\n")
                    return 0, "kompiled"
                if "--source-rule-inventory" in command:
                    return 1, "stop after capturing transformed definition"
                raise AssertionError(command)

            with self.assertRaisesRegex(
                klean_export.KleanExportError, "klean failed"
            ):
                klean_export.export_frozen(
                    workspace,
                    discovery,
                    destination / "export",
                    problem="example",
                    toolchain_lock=lock,
                    run_command=runner,
                )

        self.assertIn(
            "syntax Seq ::= snoc(Seq, Int) [function, total]",
            captured["verification"],
        )
        self.assertIn(
            "syntax Int ::= last(Seq)", captured["verification"]
        )
        self.assertNotIn(
            "syntax Int ::= last(Seq) [function, total]",
            captured["verification"],
        )
        self.assertIn(
            "rule last(cons(H:Int, KleanDef0:Seq)) => V "
            "requires KleanDef0 ==K snoc(T:Seq, V:Int) [priority(40)]",
            captured["verification"],
        )

    def test_nullary_operational_template_is_not_promoted_as_function(self) -> None:
        verification = (
            "module FOO-VERIFICATION\n"
            "  syntax Stmt ::= addLoopBody\n"
            "  rule addLoopBody => done\n"
            "  rule run(addLoopBody) => done [priority(40)]\n"
            "endmodule\n"
        )
        definitions = [{"text": "  rule addLoopBody => done"}]
        lemmas = [
            {"text": "  rule run(addLoopBody) => done [priority(40)]"}
        ]

        transformed, promoted = (
            klean_export.promote_referenced_structural_definitions(
                verification, definitions, lemmas
            )
        )

        self.assertEqual(transformed, verification)
        self.assertEqual(promoted, ())

    def test_builds_export_module_and_absolutizes_existing_requires(self) -> None:
        functions = [klean_export.Func("count", "Int", ["List", "Int"])]
        exported = klean_export.export_module("FOO-VERIFICATION", functions)
        self.assertIn("module FOO-KLEAN-EXPORT", exported)
        self.assertIn("#kxExport0", exported)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "semantics.k").write_text("module S endmodule\n")
            source = 'requires "semantics.k"\nrequires "builtin.md"\n'
            result = klean_export.absolutize_requires(source, root)
            self.assertIn(str((root / "semantics.k").resolve()), result)
            self.assertIn('requires "builtin.md"', result)

    def test_resolves_verification_and_syntax_modules_from_workspace_closure(
        self,
    ) -> None:
        cases = {
            "mpy": ("MPY-VERIFICATION", "MPY-SYNTAX"),
            "fibfib": ("FIBFIB-VERIFICATION", "FIBFIB-SYNTAX"),
            "semantic_import_without_requires": (
                "MPY-VERIFICATION",
                "MPY-SYNTAX",
            ),
        }
        for fixture, expected in cases.items():
            with self.subTest(fixture=fixture), tempfile.TemporaryDirectory() as tmp:
                workspace = Path(tmp)
                if fixture == "fibfib":
                    (workspace / "verification.k").write_text(
                        "requires \"fibfib.k\"\n"
                        "module FIBFIB-VERIFICATION\n"
                        "  imports FIBFIB\n"
                        "endmodule\n"
                    )
                    (workspace / "fibfib.k").write_text(
                        "module FIBFIB-SYNTAX\nendmodule\n"
                        "module FIBFIB\n"
                        "  imports FIBFIB-SYNTAX\n"
                        "endmodule\n"
                    )
                else:
                    (workspace / "verification.k").write_text(
                        "module MPY-VERIFICATION\n"
                        "  imports MPY\n"
                        "endmodule\n"
                    )
                    (workspace / "semantics.k").write_text(
                        "module MPY-SYNTAX\nendmodule\n"
                        "module MPY\n"
                        "  imports MPY-SYNTAX\n"
                        "endmodule\n"
                    )
                resolution = klean_export.resolve_definition_closure(workspace)
                self.assertEqual(
                    (
                        resolution.verification_module,
                        resolution.syntax_module,
                    ),
                    expected,
                )
                self.assertEqual(
                    resolution.required_files,
                    tuple(
                        sorted(
                            (path.resolve() for path in workspace.glob("*.k")),
                            key=str,
                        )
                    ),
                )

    def test_definition_resolution_uses_last_verification_kompile(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            (workspace / "verification.k").write_text(
                "module FOO-SYNTAX\nendmodule\n"
                "module BASE-VERIFICATION\n"
                "  imports FOO-SYNTAX\n"
                "endmodule\n"
                "module FINAL-VERIFICATION\n"
                "  imports BASE-VERIFICATION\n"
                "endmodule\n"
            )
            (workspace / "prove.sh").write_text(
                "kompile verification.k --main-module BASE-VERIFICATION\n"
                "kompile verification.k --main-module FINAL-VERIFICATION\n"
            )

            resolution = klean_export.resolve_definition_closure(workspace)

        self.assertEqual(
            resolution.verification_module, "FINAL-VERIFICATION"
        )
        self.assertEqual(resolution.syntax_module, "FOO-SYNTAX")

    def test_resolver_accepts_plain_verification_module(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            (workspace / "verification.k").write_text(
                "module VERIFICATION\n"
                "  imports SEMANTIC\n"
                "endmodule\n"
            )
            (workspace / "semantic.k").write_text(
                "module MPY-SYNTAX\nendmodule\n"
                "module SEMANTIC\n"
                "  imports MPY-SYNTAX\n"
                "endmodule\n"
            )

            resolution = klean_export.resolve_definition_closure(workspace)

            self.assertEqual(resolution.verification_module, "VERIFICATION")
            self.assertEqual(resolution.syntax_module, "MPY-SYNTAX")

    def test_resolver_uses_stage1_compilation_root_for_reverse_require(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            (workspace / "verification.k").write_text(
                "module VERIFICATION\n"
                "  imports INT\n"
                "endmodule\n"
            )
            (workspace / "semantic.k").write_text(
                'requires "verification.k"\n'
                "module MPY-SYNTAX\nendmodule\n"
                "module SEMANTIC\n"
                "  imports MPY-SYNTAX\n"
                "  imports VERIFICATION\n"
                "endmodule\n"
            )
            (workspace / "prove.sh").write_text(
                "kompile semantic.k --backend haskell "
                "--main-module SEMANTIC --syntax-module MPY-SYNTAX\n"
            )

            resolution = klean_export.resolve_definition_closure(workspace)

        self.assertEqual(resolution.syntax_module, "MPY-SYNTAX")
        self.assertEqual(
            [path.name for path in resolution.entry_files],
            ["semantic.k"],
        )
        self.assertEqual(
            [path.name for path in resolution.required_files],
            ["semantic.k", "verification.k"],
        )

    def test_staged_driver_does_not_duplicate_cyclic_verification_module(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "workspace"
            workspace.mkdir()
            verification = workspace / "verification.k"
            verification.write_text(
                "module VERIFICATION\n"
                "  imports MPY-SYNTAX\n"
                "endmodule\n"
            )
            semantic = workspace / "semantic.k"
            semantic.write_text(
                'requires "verification.k"\n'
                "module MPY-SYNTAX\nendmodule\n"
            )
            resolution = klean_export.DefinitionResolution(
                verification_file=verification.resolve(),
                verification_module="VERIFICATION",
                syntax_module="MPY-SYNTAX",
                required_files=(semantic.resolve(), verification.resolve()),
                entry_files=(semantic.resolve(),),
            )
            scratch = Path(temporary) / "scratch"
            scratch.mkdir()

            driver = klean_export.stage_definition_driver(
                scratch,
                workspace.resolve(),
                resolution,
                verification.read_text(),
                "module VERIFICATION-KLEAN-EXPORT\n"
                "  imports VERIFICATION\n"
                "endmodule\n",
            )

            driver_text = driver.read_text()
            staged_semantic = scratch / "definition-source/semantic.k"
            staged_verification = scratch / "definition-source/verification.k"
            self.assertIn(str(staged_semantic), driver_text)
            self.assertNotIn(str(staged_verification), driver_text)
            self.assertEqual(
                staged_semantic.read_text().count('requires "verification.k"'),
                1,
            )
            self.assertEqual(
                staged_verification.read_text().count("module VERIFICATION"),
                1,
            )

    def test_generated_lean_quotes_reserved_k_identifier(self) -> None:
        source = (
            "inductive return where\n"
            "namespace return\n"
            "def x : return := by sorry\n"
            "end return\n"
        )
        self.assertEqual(
            klean.quote_reserved_lean_identifiers(source, {"return"}),
            "inductive «return» where\n"
            "namespace «return»\n"
            "def x : «return» := by sorry\n"
            "end «return»\n",
        )
        definition = SimpleNamespace(
            sorts={"SortReturnCell": object()}, symbols={}
        )
        self.assertEqual(
            klean._definition_reserved_identifiers(definition, str),
            {"return"},
        )

        definition = SimpleNamespace(
            sorts={"SortPrefixCell": object()}, symbols={}
        )
        self.assertEqual(
            klean._definition_reserved_identifiers(definition, str),
            {"prefix"},
        )

    def test_predicate_equalities_are_rendered_as_equivalence(self) -> None:
        self.assertEqual(
            klean.lean_predicate_equivalence("left = right", "x = y"),
            "(left = right) ↔ (x = y)",
        )

    def test_pattern_sort_dependencies_include_variable_sorts(self) -> None:
        scope = SimpleNamespace(name="SortScope")
        integer = SimpleNamespace(name="SortInt")
        pattern = SimpleNamespace(
            sort=integer,
            patterns=(SimpleNamespace(sort=scope, patterns=()),),
        )
        self.assertEqual(
            klean._pattern_sort_names(pattern),
            {"SortInt", "SortScope"},
        )

    def test_lean_equality_gives_structure_literals_an_expected_type(
        self,
    ) -> None:
        self.assertEqual(
            klean.lean_typed_equality("{ k := lhs }", "{ k := rhs }", "Top"),
            "({ k := lhs } : Top) = ({ k := rhs } : Top)",
        )

    def test_kore_location_inside_multiline_rule_binds_to_rule_start(self) -> None:
        source_rule = {
            "source_rule_id": "rule-fixture",
            "start_line": 44,
            "end_line": 79,
        }
        axiom = SimpleNamespace(
            text="Source(/tmp/verification.k) Location(45,5,79,18)"
        )
        self.assertEqual(
            klean._source_rule_for_axiom(
                axiom, "verification.k", {44: source_rule}
            ),
            (44, source_rule),
        )

    def test_resolver_ignores_external_builtin_syntax_imports(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            (workspace / "verification.k").write_text(
                "module VERIFICATION\n"
                "  imports SEMANTIC\n"
                "endmodule\n"
            )
            (workspace / "semantic.k").write_text(
                "module MPY-SYNTAX\n"
                "  imports INT-SYNTAX\n"
                "  imports BOOL-SYNTAX\n"
                "endmodule\n"
                "module SEMANTIC\n"
                "  imports MPY-SYNTAX\n"
                "  imports STRING-SYNTAX\n"
                "endmodule\n"
            )

            resolution = klean_export.resolve_definition_closure(workspace)

            self.assertEqual(resolution.syntax_module, "MPY-SYNTAX")

    def test_resolver_supports_k_identifiers_and_rejects_duplicate_modules(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            (workspace / "verification.k").write_text(
                "module FOO_BAR'-VERIFICATION\n"
                "  imports FOO_BAR'\n"
                "endmodule\n"
            )
            (workspace / "one.k").write_text(
                "module FOO_BAR'\n"
                "  imports FOO_BAR'-SYNTAX\n"
                "endmodule\n"
                "module FOO_BAR'-SYNTAX\nendmodule\n"
            )
            resolution = klean_export.resolve_definition_closure(workspace)
            self.assertEqual(
                resolution.syntax_module, "FOO_BAR'-SYNTAX"
            )
            (workspace / "two.k").write_text(
                "module FOO_BAR'\nendmodule\n"
            )
            with self.assertRaisesRegex(
                klean_export.KleanExportError, "duplicate module"
            ):
                klean_export.resolve_definition_closure(workspace)

    def test_resolver_ignores_mutation_byproduct_duplicate_modules(
        self,
    ) -> None:
        """prove.sh mutation/bridge byproducts that reuse VERIFICATION/SPEC are
        excluded from the closure instead of aborting resolution."""

        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            (workspace / "verification.k").write_text(
                'requires "semantics.k"\n'
                "module VERIFICATION\n"
                "  imports SEMANTICS\n"
                "endmodule\n"
            )
            (workspace / "semantics.k").write_text(
                "module MPY-SYNTAX\nendmodule\n"
                "module SEMANTICS\n"
                "  imports MPY-SYNTAX\n"
                "endmodule\n"
            )
            # kprove target — declares SPEC, never a kompile source.
            (workspace / "spec.k").write_text(
                'requires "verification.k"\n'
                "module SPEC\nendmodule\n"
            )
            # Byproducts reuse the canonical VERIFICATION/SPEC module names.
            (workspace / "verification-mutant.k").write_text(
                'requires "semantics.k"\n'
                "module VERIFICATION\n"
                "  imports SEMANTICS\n"
                "endmodule\n"
            )
            (workspace / "spec-mutant.k").write_text(
                'requires "verification-mutant.k"\n'
                "module SPEC\nendmodule\n"
            )
            (workspace / "prove.sh").write_text(
                "kompile --backend haskell verification.k "
                "--main-module VERIFICATION --syntax-module MPY-SYNTAX\n"
                "kompile --backend haskell verification-mutant.k "
                "--main-module VERIFICATION --syntax-module MPY-SYNTAX\n"
            )

            resolution = klean_export.resolve_definition_closure(workspace)

            self.assertEqual(resolution.verification_module, "VERIFICATION")
            self.assertEqual(resolution.syntax_module, "MPY-SYNTAX")
            self.assertEqual(
                sorted(path.name for path in resolution.required_files),
                ["semantics.k", "verification.k"],
            )
            self.assertEqual(
                [path.name for path in resolution.entry_files],
                ["verification.k"],
            )

    def test_resolver_fails_on_reached_duplicate_module(self) -> None:
        """A module declared by two files both reached from the export target
        still fails closed as an ambiguous target definition."""

        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            (workspace / "verification.k").write_text(
                'requires "one.k"\n'
                'requires "two.k"\n'
                "module VERIFICATION\n"
                "  imports SHARED\n"
                "endmodule\n"
            )
            (workspace / "one.k").write_text(
                "module SHARED\n"
                "  imports SHARED-SYNTAX\n"
                "endmodule\n"
                "module SHARED-SYNTAX\nendmodule\n"
            )
            (workspace / "two.k").write_text("module SHARED\nendmodule\n")
            with self.assertRaisesRegex(
                klean_export.KleanExportError, "duplicate module"
            ):
                klean_export.resolve_definition_closure(workspace)

    def test_polymorphic_lemma_hook_is_modeled_and_fails_closed(self) -> None:
        """Sort-polymorphic hooks (K ite) are modeled by a total Lean
        definition, monomorphic symbols keep opaque bindings, and an unmodeled
        polymorphic symbol fails closed."""

        class _SortApp:
            def __init__(self, name: str) -> None:
                self.name = name

        class _SortVar:
            def __init__(self, name: str) -> None:
                self.name = name

        def symbol_ident(symbol: str) -> str:
            return {"Lblite": "kite"}.get(symbol, symbol)

        monomorphic = SimpleNamespace(
            param_sorts=(_SortApp("SortInt"), _SortApp("SortInt")),
            sort=_SortApp("SortInt"),
        )
        self.assertIsNone(
            klean._polymorphic_lemma_hook_definition(
                monomorphic,
                "Lbl'UndsPlus'Int'Unds'",
                symbol_ident,
                _SortApp,
            )
        )

        ite = SimpleNamespace(
            param_sorts=(
                _SortApp("SortBool"),
                _SortVar("SortSort"),
                _SortVar("SortSort"),
            ),
            sort=_SortVar("SortSort"),
        )
        self.assertEqual(
            klean._polymorphic_lemma_hook_definition(
                ite, "Lblite", symbol_ident, _SortApp
            ),
            "def kite {α : Type} (c : SortBool) (t e : α) : α := cond c t e",
        )

        unmodeled = SimpleNamespace(
            param_sorts=(_SortVar("SortSort"),),
            sort=_SortVar("SortSort"),
        )
        with self.assertRaisesRegex(RuntimeError, "without a Lean model"):
            klean._polymorphic_lemma_hook_definition(
                unmodeled, "Lblmystery", symbol_ident, _SortApp
            )

    def test_resolver_rejects_symlink_root_and_unsafe_k_requires(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "workspace"
            workspace.mkdir()
            (workspace / "verification.k").write_text(
                "module FOO-VERIFICATION\n"
                "  imports FOO-SYNTAX\n"
                "endmodule\n"
            )
            (workspace / "syntax.k").write_text(
                "module FOO-SYNTAX\nendmodule\n"
            )
            linked = root / "linked-workspace"
            linked.symlink_to(workspace, target_is_directory=True)
            with self.assertRaisesRegex(
                klean_export.KleanExportError, "real directory"
            ):
                klean_export.resolve_definition_closure(linked)

            verification = workspace / "verification.k"
            for required, message in (
                ("../missing-escape.k", "outside"),
                ("missing-local.k", "missing"),
            ):
                with self.subTest(required=required):
                    verification.write_text(
                        f'requires "{required}"\n'
                        "module FOO-VERIFICATION\n"
                        "  imports FOO-SYNTAX\n"
                        "endmodule\n"
                    )
                    with self.assertRaisesRegex(
                        klean_export.KleanExportError, message
                    ):
                        klean_export.resolve_definition_closure(workspace)

    def test_float_domain_values_are_validated_and_rendered(self) -> None:
        self.assertEqual(klean.float_literal("3p53x11"), "(3.0 : Float)")
        self.assertEqual(klean.float_literal("-Infinity"), "(-1.0 / 0.0 : Float)")
        with self.assertRaises(ValueError):
            klean.float_literal("not-a-float")

    def test_termination_and_noncomputable_repairs_are_deterministic(self) -> None:
        output = """
fail to show termination for
  «foo.bar»
Call from «foo.bar» to helper
"""
        self.assertEqual(
            klean_export.termination_failures(output),
            {"«foo.bar»", "helper"},
        )
        source = "def helper (x : Nat) : Nat := helper x\ndef okay : Nat := 0\n"
        repaired = klean_export.axiomatize(source, {"helper"})
        self.assertIn("axiom helper (x : Nat) : Nat", repaired)
        self.assertIn("def okay", repaired)
        self.assertTrue(
            klean_export.needs_noncomputable(
                "consider marking definition as 'noncomputable'"
            )
        )
        self.assertIn(
            "noncomputable def okay",
            klean_export.mark_all_noncomputable("def okay : Nat := 0"),
        )

    def test_collection_hook_axioms_are_replaced_by_executable_models(self) -> None:
        source = (
            "axiom «.List» : Option SortList\n\n"
            "axiom «.Map» : Option SortMap\n\n"
            "axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList\n\n"
            "axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap\n\n"
            "axiom «_in_keys(_)_MAP_Bool_KItem_Map» "
            "(x0 : SortKItem) (x1 : SortMap) : Option SortBool\n\n"
            "axiom «_[_<-undef]» (x0 : SortMap) (x1 : SortKItem) "
            ": Option SortMap\n\n"
            "axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) "
            ": Option SortMap\n\n"
            "axiom ListItem (x0 : SortKItem) : Option SortList\n\n"
            "axiom «Map:lookup» (x0 : SortMap) (x1 : SortKItem) "
            ": Option SortKItem\n\n"
            "axiom «Map:update» (x0 : SortMap) (x1 : SortKItem) "
            "(x2 : SortKItem) : Option SortMap\n"
        )

        repaired, names = klean_export.model_collection_hooks(source)

        self.assertEqual(
            names,
            (
                ".List",
                ".Map",
                "ListItem",
                "Map:lookup",
                "Map:update",
                "_List_",
                "_Map_",
                "_in_keys(_)_MAP_Bool_KItem_Map",
                "_[_<-undef]",
                "_|->_",
            ),
        )
        self.assertNotIn("axiom «.Map»", repaired)
        self.assertNotIn("axiom «Map:lookup»", repaired)
        self.assertIn("Classical.typeDecidableEq SortKItem", repaired)
        self.assertIn("noncomputable def «Map:lookup»", repaired)
        self.assertIn("if candidate = key then some value", repaired)
        self.assertIn("some ⟨x0.coll ++ x1.coll⟩", repaired)

    def test_collection_hook_constructor_subset_is_modeled(self) -> None:
        source = (
            "import Fixture.Inj\n\n"
            "axiom «.List» : Option SortList\n\n"
            "axiom «.Map» : Option SortMap\n\n"
            "axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList\n\n"
            "axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap\n\n"
            "axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) "
            ": Option SortMap\n\n"
            "axiom ListItem (x0 : SortKItem) : Option SortList\n"
        )

        repaired, names = klean_export.model_collection_hooks(source)

        self.assertEqual(
            names,
            (".List", ".Map", "ListItem", "_List_", "_Map_", "_|->_"),
        )
        for absent in (
            "axiom «.List»",
            "axiom «.Map»",
            "axiom _List_",
            "axiom _Map_",
            "axiom «_|->_»",
            "axiom ListItem",
        ):
            self.assertNotIn(absent, repaired)
        self.assertIn("Classical.typeDecidableEq SortKItem", repaired)
        self.assertIn("noncomputable def _Map_", repaired)
        # Helpers must be emitted before the first model that uses them.
        self.assertLess(
            repaired.index("private noncomputable def kleanMapDisjointModel"),
            repaired.index("noncomputable def _Map_"),
        )

    def test_partial_collection_hook_family_is_modeled_as_subset(self) -> None:
        # pyk emits an axiom only for the hooks a definition references, so a
        # partially referenced family is normal.  Every present hook is modeled
        # and no hook axiom survives; absent members are simply skipped.
        source = (
            "axiom «.Map» : Option SortMap\n"
            "axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap\n"
            "axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) "
            ": Option SortMap\n"
            "axiom «Map:lookup» (x0 : SortMap) (x1 : SortKItem) "
            ": Option SortKItem\n"
        )

        repaired, names = klean_export.model_collection_hooks(source)

        self.assertEqual(names, (".Map", "Map:lookup", "_Map_", "_|->_"))
        for absent in (
            "axiom «.Map»",
            "axiom _Map_",
            "axiom «_|->_»",
            "axiom «Map:lookup»",
        ):
            self.assertNotIn(absent, repaired)
        self.assertIn("Classical.typeDecidableEq SortKItem", repaired)
        self.assertIn("noncomputable def «Map:lookup»", repaired)
        self.assertIn("noncomputable def _Map_", repaired)
        # No hook axiom survives the subset modeling.
        self.assertEqual(klean_export._unmodeled_hook_axioms(repaired), [])

    def test_unmodeled_hook_axiom_fails_closed(self) -> None:
        # An unregistered collection/K-sequence builtin the exporter left as an
        # axiom must be caught by the net and fail closed, listed verbatim.
        clean = "noncomputable def foo : SortInt := some 0\n"
        self.assertEqual(klean_export._unmodeled_hook_axioms(clean), [])
        klean_export._assert_no_unmodeled_hook_axioms(clean)

        unregistered = (
            "axiom «Set:in» (x0 : SortKItem) (x1 : SortSet) : Option SortBool"
        )
        modeled = clean + unregistered + "\n"
        self.assertEqual(
            klean_export._unmodeled_hook_axioms(modeled), [unregistered]
        )
        with self.assertRaisesRegex(
            klean_export.KleanExportError, "unmodeled hook axiom remains"
        ) as caught:
            klean_export._assert_no_unmodeled_hook_axioms(modeled)
        self.assertIn(unregistered, str(caught.exception))

    def test_every_registered_hook_axiom_is_caught_when_unmodeled(self) -> None:
        # Design guarantee: if any currently registered hook is left unmodeled,
        # the net flags its axiom verbatim.
        for signature in (
            *klean_export._COLLECTION_HOOK_MODELS,
            *klean_export._CORE_OPERATIONAL_HOOK_MODELS,
        ):
            with self.subTest(signature=signature):
                self.assertEqual(
                    klean_export._unmodeled_hook_axioms(signature + "\n"),
                    [signature],
                )

    def test_recursive_build_is_axioms_get_fuel_bounded_k_model(self) -> None:
        source = (
            "axiom _5bd0f09 : SortIntSeq → SortInt → SortInt → "
            "SortInt → Option SortIntSeq\n"
            "axiom «buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int» "
            "(x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) "
            "(x3 : SortInt) : Option SortIntSeq\n"
        )

        repaired, names = klean_export.model_recursive_build_is(source)

        self.assertEqual(
            names,
            (
                "_5bd0f09",
                "buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int",
            ),
        )
        self.assertNotIn("axiom _5bd0f09", repaired)
        self.assertNotIn("axiom «buildIS", repaired)
        self.assertIn("private def kleanIntSeqLengthModel", repaired)
        self.assertIn("private def kleanBuildISFuelModel", repaired)
        self.assertIn("kleanIntSeqLengthModel x0 + 1", repaired)

    def test_recursive_build_is_mutual_defs_get_fuel_bounded_k_model(self) -> None:
        source = (
            "def _2928123 : SortIntSeq → SortInt → SortInt → "
            "SortInt → Option SortIntSeq\n"
            "  | _Gen0, I, STOP, STEP => some _Gen0\n\n"
            "mutual\n"
            "  def _5bd0f09 : SortIntSeq → SortInt → SortInt → "
            "SortInt → Option SortIntSeq\n"
            "    | IS, I, STOP, STEP => do\n"
            "      let next <- "
            "«buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int» "
            "IS I STOP STEP\n"
            "      return next\n\n"
            "  def "
            "«buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int» "
            "(x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) "
            "(x3 : SortInt) : Option SortIntSeq := "
            "(_2928123 x0 x1 x2 x3) <|> (_5bd0f09 x0 x1 x2 x3)\n"
            "end\n"
        )

        repaired, names = klean_export.model_recursive_build_is(source)

        self.assertEqual(
            names,
            (
                "_5bd0f09",
                "buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int",
            ),
        )
        self.assertNotIn("mutual\n  def _5bd0f09", repaired)
        self.assertIn("private def kleanBuildISFuelModel", repaired)
        self.assertIn("noncomputable def _5bd0f09", repaired)
        self.assertIn("noncomputable def «buildIS", repaired)

    def test_core_operational_hooks_get_exact_models(self) -> None:
        source = (
            "axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : "
            "Option SortInt\n"
            "axiom append (x0 : SortK) (x1 : SortK) : Option SortK\n"
        )

        repaired, names = klean_export.model_core_operational_hooks(source)

        self.assertEqual(names, ("_%Int_", "append"))
        self.assertNotIn("axiom «_%Int_»", repaired)
        self.assertNotIn("axiom append", repaired)
        self.assertIn("Int.tmod x0 x1", repaired)
        self.assertIn("if x1 = 0 then none", repaired)
        self.assertIn("noncomputable def append", repaired)
        self.assertIn("SortK.kseq item modeledRest", repaired)
        self.assertEqual(klean_export._unmodeled_hook_axioms(repaired), [])

    def test_core_operational_hook_subset_is_modeled(self) -> None:
        # Task 24-largest-divisor references «_%Int_» but not append; the
        # present hook is modeled and the absent registration is skipped.
        remainder_only = (
            "axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt\n"
        )
        repaired, names = klean_export.model_core_operational_hooks(
            remainder_only
        )
        self.assertEqual(names, ("_%Int_",))
        self.assertNotIn("axiom «_%Int_»", repaired)
        self.assertIn("Int.tmod x0 x1", repaired)
        self.assertEqual(klean_export._unmodeled_hook_axioms(repaired), [])

        append_only = "axiom append (x0 : SortK) (x1 : SortK) : Option SortK\n"
        repaired, names = klean_export.model_core_operational_hooks(
            append_only
        )
        self.assertEqual(names, ("append",))
        self.assertNotIn("axiom append", repaired)
        self.assertIn("SortK.kseq item modeledRest", repaired)
        self.assertEqual(klean_export._unmodeled_hook_axioms(repaired), [])

    def test_generated_function_elaboration_failures_are_deterministic(
        self,
    ) -> None:
        source = (
            "mutual\n"
            "  def helper : Nat → Option Nat\n"
            "    | x => some missing\n"
            "\n"
            "  def caller : Nat → Option Nat := helper\n"
            "end\n"
        )
        output = (
            "error: Fixture/Func.lean:3:17: unknown identifier 'missing'\n"
            "error: Fixture/Func.lean:5:34: Application type mismatch\n"
        )
        self.assertEqual(
            klean_export.elaboration_failures(source, output),
            {"helper", "caller"},
        )

    def test_generated_lake_build_has_deterministic_large_lean_stack(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary)
            lakefile = package / "lakefile.toml"
            lakefile.write_text(
                'name = "fixture"\n'
                'weakLeanArgs = ["-D maxHeartbeats=10000000"]\n\n'
                "[[lean_lib]]\n"
                'name = "Fixture"\n'
            )

            klean_export._patch_lake_build_directory(package)

            text = lakefile.read_text()
            self.assertIn('buildDir = "/tmp/klean-generated-build"', text)
            self.assertIn(
                'moreLeanArgs = ["-D maxRecDepth=100000", "-s", "65536"]',
                text,
            )

    def test_zero_obligations_is_explicit_and_has_no_fake_true_target(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            generated = Path(temporary)
            (generated / "obligation-map.json").write_text(
                json.dumps(
                    {
                        "source_rules": [],
                        "obligations": [],
                        "trust_parameters": [],
                    }
                )
                + "\n"
            )
            (generated / "Lemmas.lean").write_text("-- no obligations\n")
            self.assertIsNone(klean_export.target_statement(generated))
            (generated / "Lemmas.lean").write_text(
                "def targetStatement : Prop := True\n"
            )
            with self.assertRaisesRegex(
                klean_export.KleanExportError, "zero obligations"
            ):
                klean_export.target_statement(generated)

    def test_lemma_emission_failure_is_fatal(self) -> None:
        def broken() -> int:
            raise RuntimeError("lemma failure")

        with self.assertRaisesRegex(RuntimeError, "lemma failure"):
            klean.emit_lemmas_or_raise(broken)

    def test_fresh_read_only_template_copy_is_made_safely_writable(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "generated"
            nested = root / "Library"
            nested.mkdir(parents=True)
            source = nested / "Prelude.lean"
            source.write_text("def x := 1\n")
            os.chmod(source, 0o444)
            os.chmod(nested, 0o555)
            os.chmod(root, 0o555)
            klean.make_generated_tree_owner_writable(root)
            self.assertTrue(os.stat(root).st_mode & stat.S_IWUSR)
            self.assertTrue(os.stat(nested).st_mode & stat.S_IWUSR)
            self.assertTrue(os.stat(source).st_mode & stat.S_IWUSR)
            source.write_text("def x := 2\n")

    def test_generated_tree_rejects_links_instead_of_chmodding_targets(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "generated"
            root.mkdir()
            target = Path(temporary) / "outside"
            target.write_text("keep\n")
            (root / "linked").symlink_to(target)
            with self.assertRaisesRegex(RuntimeError, "unsafe entry"):
                klean.make_generated_tree_owner_writable(root)
            self.assertEqual(target.read_text(), "keep\n")

    def test_lean_trust_inventory_uses_qualified_declaration_identity(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "Prelude.lean"
            source.write_text(
                "namespace First\n"
                "axiom unitAx : List Nat\n"
                "end First\n"
                "namespace Second\n"
                "axiom unitAx (x : Nat) : Option Nat\n"
                "end Second\n"
            )
            declarations = klean_export.lean_trust_declarations(source)
            self.assertEqual(
                [item["name"] for item in declarations],
                ["First.unitAx", "Second.unitAx"],
            )
            self.assertEqual(
                declarations[1]["type"], "(x : Nat) : Option Nat"
            )


class KleanExportContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.input = self.root / "frozen-k"
        self.input.mkdir()
        (self.input / "verification.k").write_text(
            """
module FOO-VERIFICATION
  imports MPY-SYNTAX
  syntax Int ::= summary(Int) [function]
  rule external(summary(I)) => I [simplification]
  rule summary(I) => I [simplification]
endmodule
"""
        )
        (self.input / "reference-semantics").mkdir()
        (self.input / "reference-semantics/semantics.k").write_text(
            "module MPY-SYNTAX endmodule\n"
        )
        self.discovery = write_discovery_manifest(
            self.input,
            self.root / "validated-trust-boundary.json",
            ["DOMAIN_LEMMA", "DEFINITION"],
        )
        self.lock = self.root / "lock.json"
        self.lock.write_text(
            json.dumps(
                {
                    "runtimeverification_k_commit": "k-commit",
                    "pyk_project": "pyk",
                    "lean_toolchain": "leanprover/lean4:v4.22.0",
                }
            )
            + "\n"
        )

    def fake_runner(self, command, *, cwd, timeout, env, shell=False):
        command_text = command if isinstance(command, str) else " ".join(command)
        if command[0] == "kompile":
            output_index = command.index("--output-definition")
            definition = Path(command[output_index + 1])
            definition.mkdir(parents=True)
            (definition / "definition.kore").write_text("[]\n")
            return 0, "kompiled"
        if "klean.py" in command_text:
            output_index = command.index("-o")
            lean_output = Path(command[output_index + 1])
            package = command[command.index(str(lean_output)) - 2]
            package_root = lean_output / package
            library = klean_export.lib_name(package)
            (package_root / library).mkdir(parents=True)
            (package_root / "lakefile.toml").write_text(
                f'name = "{package}"\n'
            )
            (package_root / f"{library}.lean").write_text(
                f"import {library}.Lemmas\n"
            )
            (package_root / library / "Func.lean").write_text(
                "axiom trusted : Nat\n"
            )
            inventory_path = Path(
                command[command.index("--source-rule-inventory") + 1]
            )
            source_rules = json.loads(inventory_path.read_text())[
                "source_rules"
            ]
            eligible = [
                item
                for item in source_rules
                if item["classification"] == "TRUST_OBLIGATION"
            ]
            obligations = []
            parameters = []
            if eligible:
                (package_root / library / "Lemmas.lean").write_text(
                    "def targetStatement\n"
                    "    (external : Int → Int)\n"
                    "    : Prop :=\n"
                    "    (∀ (I : Int), external I = I)\n"
                    f"\nend {library}.Lemmas\n"
                )
                binding = {
                    "kore_symbol": "external",
                    "name": "external",
                    "type": "Int → Int",
                    "source_rule_ids": [eligible[0]["source_rule_id"]],
                }
                binding["binding_sha256"] = klean_export.sha256_text(
                    json.dumps(
                        binding, sort_keys=True, separators=(",", ":")
                    )
                )
                obligations.append(
                    {
                        "source_rule_id": eligible[0]["source_rule_id"],
                        "source_span": {
                            "start_line": eligible[0]["start_line"],
                            "end_line": eligible[0]["end_line"],
                        },
                        "lean_conjunct": (
                            "∀ (I : Int), external I = I"
                        ),
                        "lean_conjunct_sha256": klean_export.sha256_text(
                            "∀ (I : Int), external I = I"
                        ),
                    }
                )
                parameters.append(binding)
            else:
                (package_root / library / "Lemmas.lean").write_text(
                    f"-- no domain lemmas\n\nend {library}.Lemmas\n"
                )
            (package_root / "obligation-map.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "source_rules": source_rules,
                        "obligations": obligations,
                        "trust_parameters": parameters,
                    }
                )
                + "\n"
            )
            return 0, "generated"
        if command[:2] == ["lake", "build"]:
            return 0, "built"
        raise AssertionError(command)

    def test_export_is_fresh_provenanced_and_stable(self) -> None:
        first = self.root / "first"
        second = self.root / "second"
        one = klean_export.export_frozen(
            self.input,
            self.discovery,
            first,
            problem="8-sum-product",
            toolchain_lock=self.lock,
            run_command=self.fake_runner,
        )
        two = klean_export.export_frozen(
            self.input,
            self.discovery,
            second,
            problem="8-sum-product",
            toolchain_lock=self.lock,
            run_command=self.fake_runner,
        )
        self.assertEqual(one["status"], "OK")
        self.assertEqual(one, two)
        self.assertTrue((first / "generated/lean-toolchain").is_file())
        self.assertTrue((first / "input-manifest.json").is_file())
        self.assertTrue((first / "generator-manifest.json").is_file())
        manifest = json.loads(
            (first / "generator-manifest.json").read_text()
        )
        self.assertNotEqual(manifest["target"]["statement"], "True")
        self.assertEqual(manifest["obligation_count"], 1)
        self.assertEqual(
            manifest["target"]["declaration"],
            "Klean8SumProduct.Lemmas.targetStatement",
        )
        parameter = manifest["target"]["parameters"][0]
        self.assertEqual(parameter["kore_symbol"], "external")
        self.assertEqual(
            parameter["source_rule_ids"],
            [
                json.loads(
                    (
                        first / "generated/obligation-map.json"
                    ).read_text()
                )["obligations"][0]["source_rule_id"]
            ],
        )
        mapping = json.loads(
            (first / "generated/obligation-map.json").read_text()
        )
        inventory = inventory_verification(self.input)
        domain_rule_id = inventory["rules"][0]["source_rule_id"]
        summary_rule_id = inventory["rules"][1]["source_rule_id"]
        self.assertEqual(
            [item["source_rule_id"] for item in mapping["obligations"]],
            [domain_rule_id],
        )
        self.assertNotIn(
            summary_rule_id,
            {
                item["source_rule_id"]
                for item in mapping["obligations"]
            },
        )
        obligation = mapping["obligations"][0]
        self.assertEqual(
            obligation["normalized_sha256"],
            inventory["rules"][0]["normalized_sha256"],
        )
        self.assertEqual(
            obligation["inventory_sha256"], inventory["inventory_sha256"]
        )
        self.assertEqual(
            obligation["discovery_manifest_sha256"],
            klean_export.sha256_text(self.discovery.read_text()),
        )
        inventory = json.loads((first / "trust-inventory.json").read_text())
        self.assertEqual(inventory["axioms"], ["trusted"])
        self.assertEqual(inventory["designated_sorries"], 0)
        self.assertEqual(
            (first / "generated").read_bytes()
            if (first / "generated").is_file()
            else klean_export.tree_digest(first / "generated"),
            klean_export.tree_digest(second / "generated"),
        )

    def test_existing_destination_is_never_deleted_or_reused(self) -> None:
        destination = self.root / "existing"
        destination.mkdir()
        sentinel = destination / "sentinel"
        sentinel.write_text("keep\n")
        with self.assertRaisesRegex(klean_export.KleanExportError, "exists"):
            klean_export.export_frozen(
                self.input,
                self.discovery,
                destination,
                problem="8-sum-product",
                toolchain_lock=self.lock,
                run_command=self.fake_runner,
            )
        self.assertEqual(sentinel.read_text(), "keep\n")

    def test_input_mutation_aborts_without_publishing_destination(self) -> None:
        def mutating_runner(command, **kwargs):
            self.input.joinpath("verification.k").write_text("changed\n")
            return 1, "failed"

        destination = self.root / "mutated"
        with self.assertRaises(klean_export.KleanExportError):
            klean_export.export_frozen(
                self.input,
                self.discovery,
                destination,
                problem="8-sum-product",
                toolchain_lock=self.lock,
                run_command=mutating_runner,
            )
        self.assertFalse(destination.exists())

    def test_stage3_discovery_and_image_are_bound_into_manifests(
        self,
    ) -> None:
        destination = self.root / "provenanced"
        klean_export.export_frozen(
            self.input,
            self.discovery,
            destination,
            problem="8-sum-product",
            toolchain_lock=self.lock,
            generator_image_id="sha256:generator",
            run_command=self.fake_runner,
        )
        input_manifest = json.loads(
            (destination / "input-manifest.json").read_text()
        )
        generator_manifest = json.loads(
            (destination / "generator-manifest.json").read_text()
        )
        discovery_hash = klean_export.sha256_text(self.discovery.read_text())
        self.assertEqual(input_manifest["schema_version"], 3)
        self.assertEqual(generator_manifest["schema_version"], 3)
        self.assertEqual(
            input_manifest["stage3_discovery_manifest_sha256"],
            discovery_hash,
        )
        self.assertEqual(
            generator_manifest["provenance"][
                "stage3_discovery_manifest_sha256"
            ],
            discovery_hash,
        )
        self.assertEqual(
            generator_manifest["provenance"]["generator_image_id"],
            "sha256:generator",
        )

    def test_domain_obligation_does_not_require_summary_function_scope(
        self,
    ) -> None:
        (self.input / "verification.k").write_text(
            "module FOO-VERIFICATION\n"
            "  imports MPY-SYNTAX\n"
            "  rule X +Int 0 => X [simplification]\n"
            "endmodule\n"
        )
        discovery = write_discovery_manifest(
            self.input,
            self.root / "no-summary-trust-boundary.json",
            ["DOMAIN_LEMMA"],
        )
        result = klean_export.export_frozen(
            self.input,
            discovery,
            self.root / "missing-functions",
            problem="8-sum-product",
            toolchain_lock=self.lock,
            run_command=self.fake_runner,
        )
        self.assertEqual(result["status"], "OK")

    def test_empty_domain_set_does_not_require_summary_function_scope(
        self,
    ) -> None:
        (self.input / "verification.k").write_text(
            "module FOO-VERIFICATION\n"
            "  imports MPY-SYNTAX\n"
            "endmodule\n"
        )
        discovery = write_discovery_manifest(
            self.input,
            self.root / "empty-trust-boundary.json",
            [],
        )
        result = klean_export.export_frozen(
            self.input,
            discovery,
            self.root / "empty-no-summary",
            problem="8-sum-product",
            toolchain_lock=self.lock,
            run_command=self.fake_runner,
        )
        self.assertEqual(result["status"], "KLEAN_NO_OBLIGATIONS")

    def test_zero_domain_rules_has_no_target_and_is_terminally_eligible(
        self,
    ) -> None:
        discovery = write_discovery_manifest(
            self.input,
            self.root / "summary-only-trust-boundary.json",
            ["DEFINITION", "DEFINITION"],
        )
        destination = self.root / "no-obligations"
        result = klean_export.export_frozen(
            self.input,
            discovery,
            destination,
            problem="8-sum-product",
            toolchain_lock=self.lock,
            run_command=self.fake_runner,
        )
        self.assertEqual(result["status"], "KLEAN_NO_OBLIGATIONS")
        mapping = json.loads(
            (destination / "generated/obligation-map.json").read_text()
        )
        self.assertEqual(mapping["obligations"], [])
        self.assertEqual(mapping["trust_parameters"], [])
        self.assertIsNone(klean_export.target_statement(destination / "generated"))

    def test_export_rejects_discovery_for_a_different_stage1_inventory(
        self,
    ) -> None:
        (self.input / "verification.k").write_text(
            (self.input / "verification.k")
            .read_text()
            .replace("external(summary(I)) => I", "external(summary(I)) => I +Int 0")
        )
        with self.assertRaisesRegex(
            klean_export.KleanExportError, "inventory_sha256"
        ):
            klean_export.export_frozen(
                self.input,
                self.discovery,
                self.root / "mismatch",
                problem="8-sum-product",
                toolchain_lock=self.lock,
                run_command=self.fake_runner,
            )

    def test_stage1_mutation_during_discovery_validation_is_rejected(
        self,
    ) -> None:
        real_validate = (
            klean_export.lemma_discovery_contract.validate_trust_boundary
        )

        def validate_then_mutate(workspace, manifest):
            result = real_validate(workspace, manifest)
            verification = Path(workspace) / "verification.k"
            verification.write_text(
                verification.read_text().replace(
                    "external(summary(I)) => I",
                    "external(summary(I)) => I +Int 0",
                )
            )
            return result

        with (
            mock.patch.object(
                klean_export.lemma_discovery_contract,
                "validate_trust_boundary",
                side_effect=validate_then_mutate,
            ),
            self.assertRaisesRegex(
                klean_export.KleanExportError, "frozen input changed"
            ),
        ):
            klean_export.export_frozen(
                self.input,
                self.discovery,
                self.root / "validation-race",
                problem="8-sum-product",
                toolchain_lock=self.lock,
                run_command=self.fake_runner,
            )


if __name__ == "__main__":
    unittest.main()
