import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from dataclasses import fields
from pathlib import Path

from tools.k_rule_inventory import (
    KRule,
    KRuleInventoryError,
    inventory_verification,
)
from tools.lemma_discovery_contract import (
    LemmaDiscoveryContractError,
    validate_trust_boundary,
)

_OUTER_KEYWORDS = (
    "rule",
    "syntax",
    "module",
    "endmodule",
    "configuration",
    "context",
    "claim",
    "alias",
    "imports",
)


def keyword_rhs_fixture() -> tuple[
    str, str, list[tuple[str, int, int]]
]:
    module = "RHS-KEYWORDS-VERIFICATION"
    functions = {
        keyword: f"f{keyword.capitalize()}" for keyword in _OUTER_KEYWORDS
    }
    productions = " | ".join(
        f'"{keyword}" "(" ")"' for keyword in _OUTER_KEYWORDS
    )
    lines = [
        f"module {module}",
        f'  syntax Foo ::= "a" | {productions}',
        *(
            f"  syntax Foo ::= {functions[keyword]}() [function, total]"
            for keyword in _OUTER_KEYWORDS
        ),
    ]
    expected: list[tuple[str, int, int]] = []
    for keyword in _OUTER_KEYWORDS:
        start_line = len(lines) + 1
        rule_text = (
            f"  rule {functions[keyword]}() =>\n"
            f"    {keyword}()\n"
            "    [simplification]"
        )
        lines.extend(rule_text.splitlines())
        expected.append((rule_text, start_line, start_line + 2))
    lines.append("endmodule")
    return "\n".join(lines) + "\n", module, expected


def attribute_comment_fixture() -> tuple[
    str, str, list[tuple[str, list[str]]]
]:
    module = "ATTRIBUTE-COMMENTS-VERIFICATION"
    rules = [
        (
            "  rule afterComment() => a "
            "[simplification /* after */, concrete]",
            ["simplification", "concrete"],
        ),
        (
            "  rule beforeComment() => a "
            "[/* before */ simplification, concrete]",
            ["simplification", "concrete"],
        ),
        (
            "  rule commaComment() => a "
            "[/* before, comma */ simplification, concrete]",
            ["simplification", "concrete"],
        ),
        (
            "  rule apostropheLabel() => a "
            "[label(foo'bar), simplification]",
            ["label(foo'bar)", "simplification"],
        ),
    ]
    lines = [
        f"module {module}",
        '  syntax Foo ::= "a"',
        "  syntax Foo ::= afterComment() [function, total]",
        "  syntax Foo ::= beforeComment() [function, total]",
        "  syntax Foo ::= commaComment() [function, total]",
        "  syntax Foo ::= apostropheLabel() [function, total]",
        *(text for text, _attributes in rules),
        "endmodule",
    ]
    return "\n".join(lines) + "\n", module, rules


def outer_rule_state_fixtures() -> tuple[
    tuple[str, str, list[tuple[str, int, int]]], ...
]:
    paren_rule = "  rule(paren(X)) => X [simplification]"
    label_rule = "  rule[label]: f(X) => X [simplification]"
    module_rule = (
        "  rule moduleRhs() =>\n"
        "    module[a]\n"
        "    [simplification]"
    )
    endmodule_rule = (
        "  rule endmoduleRhs() =>\n"
        "    endmodule[a]\n"
        "    [simplification]"
    )
    next_rule = "  rule next() => a [simplification]"
    return (
        (
            "\n".join(
                (
                    "module RULE-PAREN-VERIFICATION",
                    '  syntax Foo ::= "a" | paren(Foo) [function, total]',
                    paren_rule,
                    "endmodule",
                    "",
                )
            ),
            "RULE-PAREN-VERIFICATION",
            [(paren_rule, 3, 3)],
        ),
        (
            "\n".join(
                (
                    "module RULE-LABEL-VERIFICATION",
                    '  syntax Foo ::= "a" | f(Foo) [function, total]',
                    label_rule,
                    "endmodule",
                    "",
                )
            ),
            "RULE-LABEL-VERIFICATION",
            [(label_rule, 3, 3)],
        ),
        (
            "\n".join(
                (
                    "module MODULE-BRACKET-VERIFICATION",
                    '  syntax Foo ::= "a" | "module" "[" Foo "]"',
                    "  syntax Foo ::= moduleRhs() [function, total]",
                    "  syntax Foo ::= next() [function, total]",
                    module_rule,
                    next_rule,
                    "endmodule",
                    "",
                )
            ),
            "MODULE-BRACKET-VERIFICATION",
            [(module_rule, 5, 7), (next_rule, 8, 8)],
        ),
        (
            "\n".join(
                (
                    "module ENDMODULE-BRACKET-VERIFICATION",
                    '  syntax Foo ::= "a" | "endmodule" "[" Foo "]"',
                    "  syntax Foo ::= endmoduleRhs() [function, total]",
                    "  syntax Foo ::= next() [function, total]",
                    endmodule_rule,
                    next_rule,
                    "endmodule",
                    "",
                )
            ),
            "ENDMODULE-BRACKET-VERIFICATION",
            [(endmodule_rule, 5, 7), (next_rule, 8, 8)],
        ),
    )


def nested_rule_state_fixtures() -> tuple[
    tuple[str, str, list[tuple[str, int, int]]], ...
]:
    variants = (
        (
            "NESTED-PAREN-VERIFICATION",
            (
                '  syntax Foo ::= "a" | "rule" "(" ")"'
                ' | "wrap" "(" Foo ")"'
            ),
            (
                "  rule f() =>\n"
                "    wrap(\n"
                "      /* unmatched ) ] } </cell> */\n"
                "      rule()\n"
                "    )\n"
                '    [simplification, label(")]}")]'
            ),
        ),
        (
            "NESTED-BRACKET-VERIFICATION",
            (
                '  syntax Foo ::= "a" | "module" "[" Foo "]"'
                ' | "wrap" "[" Foo "]"'
            ),
            (
                "  rule f() =>\n"
                "    wrap[\n"
                "      /* unmatched ] ) } </cell> */\n"
                "      module[a]\n"
                "    ]\n"
                '    [simplification, label("])}")]'
            ),
        ),
        (
            "NESTED-BRACE-VERIFICATION",
            (
                '  syntax Foo ::= "a" | "endmodule" "[" Foo "]"'
                ' | "wrap" "{" Foo "}"'
            ),
            (
                "  rule f() =>\n"
                "    wrap{\n"
                "      /* unmatched } ) ] </cell> */\n"
                "      endmodule[a]\n"
                "    }\n"
                '    [simplification, label("})]")]'
            ),
        ),
    )
    fixtures: list[
        tuple[str, str, list[tuple[str, int, int]]]
    ] = []
    for module, syntax, nested_rule in variants:
        next_rule = "  rule next() => a [simplification]"
        lines = [
            f"module {module}",
            syntax,
            "  syntax Foo ::= f() [function, total]",
            "  syntax Foo ::= next() [function, total]",
            *nested_rule.splitlines(),
            next_rule,
            "endmodule",
        ]
        fixtures.append(
            (
                "\n".join(lines) + "\n",
                module,
                [
                    (nested_rule, 5, 10),
                    (next_rule, 11, 11),
                ],
            )
        )
    cell_rule = (
        "  rule f() =>\n"
        "    wrap(\n"
        "      <top>\n"
        "        rule()\n"
        "      </top>\n"
        "    )\n"
        '    [simplification, label("</top>)]}")]'
    )
    cell_next_rule = "  rule next() => a [simplification]"
    fixtures.append(
        (
            "\n".join(
                (
                    "module NESTED-CELL-VERIFICATION",
                    '  syntax Foo ::= "a" | "rule" "(" ")"',
                    "  syntax KItem ::= f() [function, total]",
                    "  syntax KItem ::= wrap(KItem) [function, total]",
                    "  syntax KItem ::= next() [function, total]",
                    "  configuration <top> $PGM:Foo </top>",
                    cell_rule,
                    cell_next_rule,
                    "endmodule",
                    "",
                )
            ),
            "NESTED-CELL-VERIFICATION",
            [
                (cell_rule, 7, 13),
                (cell_next_rule, 14, 14),
            ],
        )
    )
    clause_rule = (
        "  rule f() => a\n"
        "    requires predicate(\n"
        "      module[a]\n"
        "    )\n"
        "    ensures predicate(\n"
        "      endmodule[a]\n"
        "    )\n"
        '    [simplification, label("requires)]}")]'
    )
    clause_next_rule = "  rule next() => a [simplification]"
    fixtures.append(
        (
            "\n".join(
                (
                    'requires "domains.md"',
                    "module NESTED-CLAUSE-VERIFICATION",
                    "  imports BOOL",
                    (
                        '  syntax Foo ::= "a"'
                        ' | "module" "[" Foo "]"'
                        ' | "endmodule" "[" Foo "]"'
                    ),
                    "  syntax Bool ::= predicate(Foo) [function]",
                    "  syntax Foo ::= f() [function, total]",
                    "  syntax Foo ::= next() [function, total]",
                    clause_rule,
                    clause_next_rule,
                    "endmodule",
                    "",
                )
            ),
            "NESTED-CLAUSE-VERIFICATION",
            [
                (clause_rule, 8, 15),
                (clause_next_rule, 16, 16),
            ],
        )
    )
    return tuple(fixtures)


def flat_multiline_rule_fixture() -> tuple[
    str, str, list[tuple[str, int, int]]
]:
    module = "FLAT-MULTILINE-RULE-VERIFICATION"
    first_rule = (
        "  rule f() =>\n"
        "    pair a\n"
        "      rule()\n"
        "    [simplification]"
    )
    next_rule = "  rule next() => a [simplification]"
    source = "\n".join(
        (
            f"module {module}",
            (
                '  syntax Foo ::= "a" | "rule" "(" ")"'
                ' | "pair" Foo Foo'
            ),
            "  syntax Foo ::= f() [function, total]",
            "  syntax Foo ::= next() [function, total]",
            first_rule,
            next_rule,
            "endmodule",
            "",
        )
    )
    return source, module, [
        (first_rule, 5, 8),
        (next_rule, 9, 9),
    ]


class KRuleInventoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.workspace = Path(self.temporary_directory.name) / "workspace"
        self.workspace.mkdir()

    def write_verification(self, text: str) -> Path:
        verification = self.workspace / "verification.k"
        verification.write_text(text)
        return verification

    def assert_kompiles(self, source: str, module: str) -> None:
        kompile = shutil.which("kompile")
        if kompile is None:
            self.skipTest("kompile is unavailable")
        verification = self.write_verification(source)
        result = subprocess.run(
            [
                kompile,
                str(verification),
                "--backend",
                "haskell",
                "--main-module",
                module,
                "--output-definition",
                str(self.workspace / "kompiled"),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=120,
        )
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_exposes_the_canonical_k_rule_record(self) -> None:
        self.assertEqual(
            [field.name for field in fields(KRule)],
            [
                "source_rule_id",
                "module",
                "start_line",
                "end_line",
                "normalized_sha256",
                "attributes",
                "text",
            ],
        )

    def test_inventories_real_k_identifiers_and_non_mpy_module(self) -> None:
        verification = """
requires "semantic.k"
module FIBFIB-VERIFICATION
  imports FIBFIB
  syntax Int ::= run_spec(Int, Int) [function, total]
  rule run_spec(N, A) => A requires N <=Int 0 [simplification]
  rule X +Int 0 => X [simplification]
endmodule
"""
        self.write_verification(verification)

        inventory = inventory_verification(self.workspace)

        self.assertEqual(
            inventory["verification_module"], "FIBFIB-VERIFICATION"
        )
        self.assertEqual(
            [rule["source_rule_id"] for rule in inventory["rules"]],
            [
                "rule-"
                + hashlib.sha256(
                    (
                        "rule run_spec(N, A) => A requires N <=Int 0 "
                        "[simplification]"
                    ).encode()
                ).hexdigest(),
                "rule-"
                + hashlib.sha256(
                    "rule X +Int 0 => X [simplification]".encode()
                ).hexdigest(),
            ],
        )
        self.assertEqual(
            [rule["attributes"] for rule in inventory["rules"]],
            [["simplification"], ["simplification"]],
        )
        self.assertEqual(
            [(rule["start_line"], rule["end_line"]) for rule in inventory["rules"]],
            [(6, 6), (7, 7)],
        )
        self.assertEqual(
            inventory["verification_sha256"],
            hashlib.sha256(verification.encode()).hexdigest(),
        )
        self.assertEqual(
            inventory["inventory_sha256"],
            hashlib.sha256(
                json.dumps(
                    inventory["rules"],
                    sort_keys=True,
                    separators=(",", ":"),
                    ensure_ascii=False,
                ).encode()
            ).hexdigest(),
        )

    def test_inventories_untagged_rules_in_local_verification_closure(
        self,
    ) -> None:
        verification = """\
module SEARCH-VERIFICATION-BASE
  rule summary(N) => N [simplification]
endmodule

module SEARCH-VERIFICATION
  imports SEARCH-VERIFICATION-BASE
  rule [loop-lemma]: <k> loop(N) => N ... </k> [priority(40)]
  rule PROGRAM => Call("search")
endmodule
"""
        self.write_verification(verification)

        inventory = inventory_verification(self.workspace)

        self.assertEqual(inventory["schema_version"], 2)
        self.assertEqual(
            inventory["verification_modules"],
            ["SEARCH-VERIFICATION-BASE", "SEARCH-VERIFICATION"],
        )
        self.assertEqual(
            [rule["module"] for rule in inventory["rules"]],
            [
                "SEARCH-VERIFICATION-BASE",
                "SEARCH-VERIFICATION",
                "SEARCH-VERIFICATION",
            ],
        )
        self.assertEqual(
            [rule["attributes"] for rule in inventory["rules"]],
            [["simplification"], ["priority(40)"], []],
        )
        self.assertIn("loop-lemma", inventory["rules"][1]["text"])

    def test_does_not_inventory_unreachable_local_modules(self) -> None:
        self.write_verification(
            "module UNUSED-HELPER\n"
            "  rule hidden(X) => X [simplification]\n"
            "endmodule\n"
            "module LIVE-BASE\n"
            "  rule live(X) => X\n"
            "endmodule\n"
            "module LIVE-VERIFICATION\n"
            "  imports LIVE-BASE\n"
            "  rule finish(X) => X\n"
            "endmodule\n"
        )

        inventory = inventory_verification(self.workspace)

        self.assertEqual(
            [rule["module"] for rule in inventory["rules"]],
            ["LIVE-BASE", "LIVE-VERIFICATION"],
        )

    def test_uses_last_verification_kompile_main_module(self) -> None:
        self.write_verification(
            "module BASE-VERIFICATION\n"
            "  rule base(X) => X\n"
            "endmodule\n"
            "module FINAL-VERIFICATION\n"
            "  imports BASE-VERIFICATION\n"
            "  rule final(X) => X [priority(40)]\n"
            "endmodule\n"
        )
        (self.workspace / "prove.sh").write_text(
            "kompile verification.k --backend haskell "
            "--main-module BASE-VERIFICATION\n"
            "kprove base-spec.k\n"
            "kompile verification.k --backend haskell \\\n"
            "  --main-module FINAL-VERIFICATION\n"
            "kprove spec.k\n"
        )

        inventory = inventory_verification(self.workspace)

        self.assertEqual(
            inventory["verification_module"], "FINAL-VERIFICATION"
        )
        self.assertEqual(
            inventory["verification_modules"],
            ["BASE-VERIFICATION", "FINAL-VERIFICATION"],
        )

    def test_preserves_multiline_rule_text_and_tokenizes_attributes(self) -> None:
        verification = (
            "module CUSTOM-NAMES-VERIFICATION\n"
            "  syntax CustomSort ::= camelCase_name(CustomSort) "
            "[function, total]\n"
            "  rule camelCase_name(X:CustomSort)\n"
            "    => X\n"
            "    requires true\n"
            '    [metadata(foo, "bar,baz"), concrete, simplification]\n'
            "  rule ignored_rule(X:CustomSort) => X "
            "[simplification-helper]\n"
            "endmodule\n"
        )
        self.write_verification(verification)

        inventory = inventory_verification(self.workspace)

        self.assertEqual(len(inventory["rules"]), 2)
        rule = inventory["rules"][0]
        expected_text = (
            "  rule camelCase_name(X:CustomSort)\n"
            "    => X\n"
            "    requires true\n"
            '    [metadata(foo, "bar,baz"), concrete, simplification]'
        )
        self.assertEqual(rule["text"], expected_text)
        self.assertEqual(
            rule["attributes"],
            [
                'metadata(foo, "bar,baz")',
                "concrete",
                "simplification",
            ],
        )
        self.assertEqual((rule["start_line"], rule["end_line"]), (3, 6))
        normalized = " ".join(expected_text.split())
        self.assertEqual(
            rule["normalized_sha256"],
            hashlib.sha256(normalized.encode()).hexdigest(),
        )
        self.assertNotIn("classification", rule)
        self.assertEqual(
            inventory["rules"][1]["attributes"],
            ["simplification-helper"],
        )

    def test_bare_rule_head_starts_a_new_outer_sentence(self) -> None:
        verification = (
            "module BARE-RULE-HEAD-VERIFICATION\n"
            "  syntax Int ::= first(Int) | second(Int) [function, total]\n"
            "  rule first(N)\n"
            "    => N\n"
            "    requires N >=Int 0\n"
            "  // The next legal K rule has its body on a later line.\n"
            "  // It must not be merged into the preceding rule bubble.\n"
            "  rule\n"
            "    second(N)\n"
            "    => N\n"
            "    requires N >Int 0\n"
            "    [simplification]\n"
            "endmodule\n"
        )
        self.write_verification(verification)

        inventory = inventory_verification(self.workspace)

        self.assertEqual(len(inventory["rules"]), 2)
        self.assertEqual(
            [
                (rule["start_line"], rule["end_line"])
                for rule in inventory["rules"]
            ],
            [(3, 5), (8, 12)],
        )
        self.assertEqual(
            inventory["rules"][1]["text"],
            (
                "  rule\n"
                "    second(N)\n"
                "    => N\n"
                "    requires N >Int 0\n"
                "    [simplification]"
            ),
        )

    def test_keyword_shaped_rhs_terms_are_not_outer_sentences(self) -> None:
        source, _module, expected = keyword_rhs_fixture()
        self.write_verification(source)

        inventory = inventory_verification(self.workspace)

        self.assertEqual(len(inventory["rules"]), len(_OUTER_KEYWORDS))
        for rule, (text, start_line, end_line) in zip(
            inventory["rules"], expected, strict=True
        ):
            with self.subTest(rhs=text.splitlines()[1].strip()):
                digest = hashlib.sha256(
                    " ".join(text.split()).encode()
                ).hexdigest()
                self.assertEqual(rule["text"], text)
                self.assertEqual(
                    (rule["start_line"], rule["end_line"]),
                    (start_line, end_line),
                )
                self.assertEqual(rule["normalized_sha256"], digest)
                self.assertEqual(rule["source_rule_id"], f"rule-{digest}")

    def test_attribute_comments_and_apostrophes_are_lexical_trivia(
        self,
    ) -> None:
        source, _module, expected = attribute_comment_fixture()
        self.write_verification(source)

        inventory = inventory_verification(self.workspace)

        self.assertEqual(len(inventory["rules"]), len(expected))
        for offset, (rule, (text, attributes)) in enumerate(
            zip(inventory["rules"], expected, strict=True),
            start=7,
        ):
            with self.subTest(text=text):
                digest = hashlib.sha256(
                    " ".join(text.split()).encode()
                ).hexdigest()
                self.assertEqual(rule["text"], text)
                self.assertEqual(rule["attributes"], attributes)
                self.assertEqual(
                    (rule["start_line"], rule["end_line"]),
                    (offset, offset),
                )
                self.assertEqual(rule["normalized_sha256"], digest)
                self.assertEqual(rule["source_rule_id"], f"rule-{digest}")

    def test_outer_rule_state_ignores_keyword_terms_until_completion(
        self,
    ) -> None:
        for source, module, expected in outer_rule_state_fixtures():
            with self.subTest(module=module):
                self.write_verification(source)

                inventory = inventory_verification(self.workspace)

                self.assertEqual(len(inventory["rules"]), len(expected))
                for rule, (text, start_line, end_line) in zip(
                    inventory["rules"], expected, strict=True
                ):
                    digest = hashlib.sha256(
                        " ".join(text.split()).encode()
                    ).hexdigest()
                    self.assertEqual(rule["text"], text)
                    self.assertEqual(
                        (rule["start_line"], rule["end_line"]),
                        (start_line, end_line),
                    )
                    self.assertEqual(rule["normalized_sha256"], digest)
                    self.assertEqual(
                        rule["source_rule_id"], f"rule-{digest}"
                    )

    def test_nested_rule_state_stays_open_until_delimiters_close(
        self,
    ) -> None:
        for source, module, expected in nested_rule_state_fixtures():
            with self.subTest(module=module):
                self.write_verification(source)

                inventory = inventory_verification(self.workspace)

                self.assertEqual(len(inventory["rules"]), len(expected))
                for rule, (text, start_line, end_line) in zip(
                    inventory["rules"], expected, strict=True
                ):
                    digest = hashlib.sha256(
                        " ".join(text.split()).encode()
                    ).hexdigest()
                    self.assertEqual(rule["text"], text)
                    self.assertEqual(
                        (rule["start_line"], rule["end_line"]),
                        (start_line, end_line),
                    )
                    self.assertEqual(rule["normalized_sha256"], digest)
                    self.assertEqual(
                        rule["source_rule_id"], f"rule-{digest}"
                    )

    def test_flat_multiline_rule_call_stays_inside_candidate_bubble(
        self,
    ) -> None:
        source, _module, expected = flat_multiline_rule_fixture()
        self.write_verification(source)

        inventory = inventory_verification(self.workspace)

        self.assertEqual(len(inventory["rules"]), len(expected))
        for rule, (text, start_line, end_line) in zip(
            inventory["rules"], expected, strict=True
        ):
            digest = hashlib.sha256(
                " ".join(text.split()).encode()
            ).hexdigest()
            self.assertEqual(rule["text"], text)
            self.assertEqual(
                (rule["start_line"], rule["end_line"]),
                (start_line, end_line),
            )
            self.assertEqual(rule["normalized_sha256"], digest)
            self.assertEqual(rule["source_rule_id"], f"rule-{digest}")

    def test_adversarial_k_fixtures_compile(self) -> None:
        fixtures = (
            keyword_rhs_fixture()[:2],
            attribute_comment_fixture()[:2],
            *(
                fixture[:2] for fixture in outer_rule_state_fixtures()
            ),
            *(
                fixture[:2] for fixture in nested_rule_state_fixtures()
            ),
            flat_multiline_rule_fixture()[:2],
        )
        for source, module in fixtures:
            with self.subTest(module=module):
                self.assert_kompiles(source, module)

    def test_rejects_linked_verification_file(self) -> None:
        target = self.workspace.parent / "outside-verification.k"
        target.write_text(
            "module LINKED-VERIFICATION\n"
            "rule X => X [simplification]\n"
            "endmodule\n"
        )
        (self.workspace / "verification.k").symlink_to(target)

        with self.assertRaisesRegex(
            KRuleInventoryError, "regular verification.k"
        ):
            inventory_verification(self.workspace)

    def test_rejects_duplicate_normalized_rule_hashes(self) -> None:
        self.write_verification(
            "module DUPLICATE-VERIFICATION\n"
            "  rule X => X [simplification]\n"
            "  rule X => X [simplification]\n"
            "endmodule\n"
        )

        with self.assertRaisesRegex(KRuleInventoryError, "duplicate"):
            inventory_verification(self.workspace)

    def test_rejects_malformed_module_boundaries(self) -> None:
        malformed_sources = (
            (
                "module OPEN-VERIFICATION\n"
                "  rule X => X [simplification]\n"
            ),
            (
                "module CLOSED-VERIFICATION\n"
                "endmodule\n"
                "endmodule junk\n"
            ),
            (
                "module CLOSED-VERIFICATION\n"
                "endmodule\n"
                "module\n"
            ),
        )
        for source in malformed_sources:
            with self.subTest(source=source):
                self.write_verification(source)
                with self.assertRaisesRegex(
                    KRuleInventoryError, "module boundar"
                ):
                    inventory_verification(self.workspace)

    def test_rejects_workspace_without_regular_verification_file(self) -> None:
        with self.assertRaisesRegex(
            KRuleInventoryError, "regular verification.k"
        ):
            inventory_verification(self.workspace)

        (self.workspace / "verification.k").mkdir()
        with self.assertRaisesRegex(
            KRuleInventoryError, "regular verification.k"
        ):
            inventory_verification(self.workspace)


class LemmaDiscoveryContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.workspace = self.root / "workspace"
        self.workspace.mkdir()
        (self.workspace / "verification.k").write_text(
            "module TRUST-BOUNDARY-VERIFICATION\n"
            "  rule summary_value(N) => N [simplification]\n"
            "  rule X +Int 0 => X [simplification]\n"
            "endmodule\n"
        )
        self.inventory = inventory_verification(self.workspace)
        self.manifest = self.root / "lemma-discovery.json"

    def manifest_document(self) -> dict[str, object]:
        first, second = self.inventory["rules"]
        return {
            "schema_version": 2,
            "inventory_sha256": self.inventory["inventory_sha256"],
            "rules": [
                {
                    "source_rule_id": first["source_rule_id"],
                    "classification": "DEFINITION",
                    "rationale": "Defines the loop summary recurrence.",
                },
                {
                    "source_rule_id": second["source_rule_id"],
                    "classification": "DOMAIN_LEMMA",
                    "rationale": "Uses integer addition identity.",
                },
            ],
        }

    def write_manifest(self, document: dict[str, object]) -> None:
        self.manifest.write_text(json.dumps(document) + "\n")

    def assert_rejected(
        self, document: dict[str, object], message: str
    ) -> None:
        self.write_manifest(document)
        with self.assertRaisesRegex(LemmaDiscoveryContractError, message):
            validate_trust_boundary(self.workspace, self.manifest)

    def test_validates_exhaustive_bijection_and_returns_full_ordered_rules(
        self,
    ) -> None:
        document = self.manifest_document()
        document["rules"] = list(reversed(document["rules"]))
        self.write_manifest(document)

        validated = validate_trust_boundary(self.workspace, self.manifest)

        self.assertEqual(
            {key: validated[key] for key in self.inventory},
            self.inventory,
        )
        self.assertEqual(
            validated["definitions"],
            [
                {
                    **self.inventory["rules"][0],
                    "classification": "DEFINITION",
                    "rationale": "Defines the loop summary recurrence.",
                }
            ],
        )
        self.assertEqual(
            validated["domain_lemmas"],
            [
                {
                    **self.inventory["rules"][1],
                    "classification": "DOMAIN_LEMMA",
                    "rationale": "Uses integer addition identity.",
                }
            ],
        )

    def test_rejects_missing_rule_entry(self) -> None:
        document = self.manifest_document()
        document["rules"] = document["rules"][:-1]
        self.assert_rejected(document, "missing")

    def test_rejects_duplicated_rule_entry(self) -> None:
        document = self.manifest_document()
        document["rules"][1]["source_rule_id"] = document["rules"][0][
            "source_rule_id"
        ]
        self.assert_rejected(document, "duplicate")

    def test_rejects_unknown_rule_entry(self) -> None:
        document = self.manifest_document()
        document["rules"][1]["source_rule_id"] = "rule-" + "f" * 64
        self.assert_rejected(document, "unknown")

    def test_rejects_inventory_hash_mismatch(self) -> None:
        document = self.manifest_document()
        document["inventory_sha256"] = "0" * 64
        self.assert_rejected(document, "inventory_sha256")

    def test_rejects_third_classification(self) -> None:
        document = self.manifest_document()
        document["rules"][0]["classification"] = "TRUST_OBLIGATION"
        self.assert_rejected(document, "classification")

    def test_classifies_every_verification_rule_role(self) -> None:
        (self.workspace / "verification.k").write_text(
            "module TRUST-BOUNDARY-VERIFICATION\n"
            "  rule summary(N) => N [simplification]\n"
            "  rule <k> step(X) => X ... </k>\n"
            "  rule [proved-loop]: <k> loop(X) => X ... </k> "
            "[priority(40)]\n"
            "  rule X +Int 0 => X [simplification]\n"
            "endmodule\n"
        )
        inventory = inventory_verification(self.workspace)
        document = {
            "schema_version": 2,
            "inventory_sha256": inventory["inventory_sha256"],
            "rules": [
                {
                    "source_rule_id": rule["source_rule_id"],
                    "classification": classification,
                    "rationale": classification,
                }
                for rule, classification in zip(
                    inventory["rules"],
                    (
                        "DEFINITION",
                        "OPERATIONAL_RULE",
                        "PROVED_DERIVED_LEMMA",
                        "DOMAIN_LEMMA",
                    ),
                    strict=True,
                )
            ],
        }
        self.write_manifest(document)

        validated = validate_trust_boundary(self.workspace, self.manifest)

        self.assertEqual(len(validated["definitions"]), 1)
        self.assertEqual(len(validated["operational_rules"]), 1)
        self.assertEqual(len(validated["proved_derived_lemmas"]), 1)
        self.assertEqual(len(validated["domain_lemmas"]), 1)

    def test_rejects_simplification_as_operational_or_proved_rule(self) -> None:
        for classification in (
            "OPERATIONAL_RULE",
            "PROVED_DERIVED_LEMMA",
        ):
            with self.subTest(classification=classification):
                document = self.manifest_document()
                document["schema_version"] = 2
                document["rules"][0]["classification"] = classification
                self.assert_rejected(document, "simplification")

    def test_rejects_authored_theorem_content(self) -> None:
        for forbidden in ("theorem", "statement", "lean", "replacement"):
            with self.subTest(forbidden=forbidden):
                document = self.manifest_document()
                document["rules"][0][forbidden] = "True"
                self.assert_rejected(document, forbidden)

    def test_rejects_non_exact_manifest_shapes(self) -> None:
        cases = (
            ("schema_version", 1, "schema_version"),
            ("unexpected", "value", "unexpected"),
        )
        for key, value, message in cases:
            with self.subTest(key=key):
                document = self.manifest_document()
                document[key] = value
                self.assert_rejected(document, message)

        document = self.manifest_document()
        document["rules"][0]["rationale"] = ""
        self.assert_rejected(document, "rationale")

        document = self.manifest_document()
        document["rules"][0]["classification"] = []
        self.assert_rejected(document, "classification")


if __name__ == "__main__":
    unittest.main()
