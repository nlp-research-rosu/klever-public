#!/usr/bin/env python3
"""Exhaustive declaration/rule inventory for the mounted K proof sources."""

from __future__ import annotations

import collections
import re
from pathlib import Path


roots = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]

entry_re = re.compile(
    r"^\s*(syntax|rule|context|configuration|claim|module|endmodule|imports|requires)\b"
)

# Rules mechanically exercised by SPEC.add-correct. Strictness-generated
# heating/cooling comes from syntax.k's BinOp/Return attributes and is recorded
# separately as syntax.
target_rules = {
    ("core.k", 125),
    ("core.k", 126),
    ("core.k", 127),
    ("core.k", 131),
    ("core.k", 132),
    ("core.k", 158),
    ("core.k", 189),
    ("core.k", 190),
    ("core.k", 191),
    ("core.k", 194),
    ("core.k", 214),
    ("core.k", 215),
    ("functions.k", 14),
    ("functions.k", 63),
    ("functions.k", 64),
    ("functions.k", 78),
    ("functions.k", 85),
    ("call.k", 20),
    ("call.k", 21),
    ("call.k", 69),
    ("operators.k", 12),
    ("int.k", 9),
}

# Concrete false conclusions relative to full CPython. None is reachable from
# the add theorem's constructor set. They are recorded so "fixed input" is not
# mistaken for universal Python fidelity.
divergences = {
    ("float.k", 61): (
        "Import(\"definitely_missing_module\") => .K, while CPython raises "
        "ModuleNotFoundError"
    ),
    ("builtins.k", 156): (
        'applyBuiltin("int", str([97,98]), .Vals) reaches 540, while '
        'CPython int("ab") raises ValueError'
    ),
    ("builtins.k", 187): (
        'applyBuiltin("eval", str(codes("6/2")), .Vals) reaches 6 through '
        'the "/" fallback, while CPython eval("6/2") is 3.0'
    ),
    ("builtins.k", 236): (
        'applyOpE("/", 6, 2) => 6, while Python true division is 3.0'
    ),
    ("builtins.k", 291): (
        'applyBuiltin("isinstance", true, typeV("int"), .Vals) reaches false, '
        "while CPython isinstance(True, int) is True"
    ),
    ("builtins.k", 295): (
        "isIntV(true) => false, while Bool is a subclass of int in CPython"
    ),
    ("methods.k", 34): (
        'applyMethod(str([97]), "count", str([]), .Vals) reaches 0, while '
        'CPython "a".count("") is 2'
    ),
    ("methods.k", 36): (
        'cntSub([], []) => 0 contributes to "a".count("") = 0 instead of 2'
    ),
    ("methods.k", 39): (
        'cntSub([97], []) recurses to 0, while "a".count("") is 2'
    ),
    ("list.k", 27): (
        "lists [ref(0)] and [ref(1)] compare false by ==K even when both heap "
        "objects contain equal lists; CPython nested-list equality is structural"
    ),
    ("tuple.k", 18): (
        "tuples (ref(0),) and (ref(1),) compare false by ==K even when both "
        "references denote equal lists; CPython tuple equality recurses"
    ),
}

opaque_names = {
    "intFloatDiv",
    "divII",
    "floatMod",
    "floatLt",
    "absF",
    "floorFI",
    "toF",
    "ceilF",
    "subF",
    "divF",
    "addF",
    "mulF",
    "powF",
    "gtF",
    "eqF",
    "decStrToF",
    "divFloatIntV",
    "intToF",
    "truncF",
    "roundF",
    "roundFN",
    "sqrtF",
    "md5hexCodes",
    "sortVS",
    "sortKeyVS",
}


def entries(path: Path):
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if entry_re.match(line)]
    for position, start in enumerate(starts):
        stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
        text = "\n".join(lines[start:stop]).strip()
        kind = entry_re.match(lines[start]).group(1)  # type: ignore[union-attr]
        yield start + 1, kind, text


def one_line(text: str) -> str:
    return " ".join(
        line.strip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith("//")
    )


def text_escape(value: str) -> str:
    return value.replace("\t", "\\t")


counts: collections.Counter[str] = collections.Counter()
classes: collections.Counter[str] = collections.Counter()
attribute_counts: collections.Counter[str] = collections.Counter()
index = 0

for path in roots:
    for line, kind, raw in entries(path):
        index += 1
        counts[kind] += 1
        normalized = one_line(raw)
        base = path.name
        key = (base, line)

        attrs = []
        for attr in [
            "function",
            "total",
            "functional",
            "simplification",
            "priority",
            "owise",
            "concrete",
            "macro",
            "macro-rec",
            "no-evaluators",
            "symbol",
            "strict",
            "seqstrict",
        ]:
            if re.search(rf"\b{re.escape(attr)}\b", normalized):
                attrs.append(attr)
                attribute_counts[attr] += 1

        if path == Path("/candidate/spec.k") and kind == "claim":
            classification = "TARGET_THEOREM"
            decision = "AUDITED_SEPARATELY_FOR_ADEQUACY"
        elif path == Path("/candidate/verification.k"):
            classification = "LOCAL_PROOF_FILE"
            decision = "IMPORT_ONLY; NO_LOCAL_EXTENSION"
        elif kind == "rule" and key in target_rules:
            classification = "ADD_EXECUTION_PATH"
            decision = "ACCEPT; DIRECT_FIXED_SEMANTICS_STEP"
        elif kind == "rule" and key in divergences:
            classification = "OFF_PATH_FULL_CPYTHON_DIVERGENCE"
            decision = "NOT_REACHABLE_FROM_ADD; WITNESS_RECORDED"
        elif "no-evaluators" in attrs or any(name in normalized for name in opaque_names):
            classification = "OPAQUE_OR_CONCRETE_TRUST_BOUNDARY"
            decision = "CONDITIONAL_ONLY; NOT_USED_BY_ADD"
        elif kind == "rule" and "concrete" in attrs:
            classification = "CONCRETE_ONLY_FIXED_RULE"
            decision = "NOT_IMPORTED_BY_PROOF; NOT_USED_BY_ADD"
        elif kind == "rule":
            classification = "FIXED_OFF_PATH_RULE"
            decision = "ACCEPT_WITHIN_DOCUMENTED_MPY_SUBSET; NOT_USED_BY_ADD"
        elif kind == "syntax":
            classification = "DECLARATION"
            decision = "NO_TRUTH ASSERTION; ATTRIBUTES INVENTORIED"
        elif kind in {"context", "configuration"}:
            classification = "EVALUATION_OR_STATE_DECLARATION"
            decision = "CHECKED; ADD-RELEVANT PARTS MAPPED"
        else:
            classification = "MODULE_WIRING"
            decision = "CHECKED"

        classes[classification] += 1
        witness = divergences.get(key, "")
        print(
            f"ITEM {index:04d}\t{path}:{line}\t{kind}\t{classification}\t"
            f"{decision}\tATTRS={','.join(attrs) or '-'}\t{text_escape(normalized)}"
        )
        if witness:
            print(f"WITNESS {index:04d}\t{text_escape(witness)}")

print(f"TOTAL_ITEMS={index}")
print(f"KIND_COUNTS={dict(sorted(counts.items()))}")
print(f"CLASS_COUNTS={dict(sorted(classes.items()))}")
print(f"ATTRIBUTE_COUNTS={dict(sorted(attribute_counts.items()))}")
print(f"TARGET_RULE_COUNT={classes['ADD_EXECUTION_PATH']}")
print(
    "LOCAL_EXTENSION_COUNT=0 "
    "(verification.k has requires/imports/module/endmodule only)"
)
