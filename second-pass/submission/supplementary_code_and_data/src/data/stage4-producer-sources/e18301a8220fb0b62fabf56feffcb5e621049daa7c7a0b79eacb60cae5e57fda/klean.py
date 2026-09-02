#!/usr/bin/env python3
"""Float-aware, lemma-emitting wrapper around the pinned pyk Klean generator."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Callable, TypeVar


_PRELUDE_FLOAT_ABBREV = "abbrev SortFloat        : Type := Float\n"
_PRELUDE_ANCHOR = "abbrev SortInt          : Type := Int\n"
T = TypeVar("T")


def float_literal(value: str) -> str:
    number = re.sub(r"p\d+x\d+$", "", value)
    if number in ("Infinity", "+Infinity"):
        return "(1.0 / 0.0 : Float)"
    if number == "-Infinity":
        return "(-1.0 / 0.0 : Float)"
    if number == "NaN":
        return "(0.0 / 0.0 : Float)"
    float(number)
    literal = (
        number if any(character in number for character in ".eE") else f"{number}.0"
    )
    return f"({literal} : Float)"


def emit_lemmas_or_raise(operation: Callable[[], T]) -> T:
    """Keep lemma generation on the trusted success path: never best-effort it."""

    return operation()


def make_generated_tree_owner_writable(root: Path) -> None:
    """Undo read-only template modes only inside fresh generated scratch."""

    root = Path(root)
    root_mode = os.lstat(root).st_mode
    if not stat.S_ISDIR(root_mode) or stat.S_ISLNK(root_mode):
        raise RuntimeError("generated Klean root must be a real directory")
    pending = [root]
    while pending:
        directory = pending.pop()
        mode = os.lstat(directory).st_mode
        os.chmod(
            directory,
            stat.S_IMODE(mode)
            | stat.S_IRUSR
            | stat.S_IWUSR
            | stat.S_IXUSR,
            follow_symlinks=False,
        )
        with os.scandir(directory) as children:
            for child in children:
                child_mode = child.stat(follow_symlinks=False).st_mode
                path = Path(child.path)
                if stat.S_ISDIR(child_mode):
                    pending.append(path)
                elif stat.S_ISREG(child_mode):
                    os.chmod(
                        path,
                        stat.S_IMODE(child_mode)
                        | stat.S_IRUSR
                        | stat.S_IWUSR,
                        follow_symlinks=False,
                    )
                else:
                    raise RuntimeError(
                        f"generated Klean tree contains unsafe entry: {path}"
                    )


def _install_float_support() -> None:
    try:
        from pyk.klean import k2lean4
        from pyk.klean.model import Term
    except ModuleNotFoundError as error:
        raise RuntimeError(
            "pyk is unavailable; run this wrapper in the pinned Klean environment"
        ) from error
    k2lean4._PRELUDE_SORTS = k2lean4._PRELUDE_SORTS | {"SortFloat"}
    original = k2lean4.K2Lean4._transform_dv

    def transform(instance: object, sort: str, value: str):
        if sort == "SortFloat":
            return Term(float_literal(value))
        return original(instance, sort, value)

    k2lean4.K2Lean4._transform_dv = transform


def _trust_lemma_symbols(
    definition_directory: Path,
    summary_functions: tuple[str, ...],
    source_marker: str,
) -> set[str]:
    from pyk.kore.manip import collect_symbols
    from pyk.kore.parser import KoreParser
    from pyk.kore.rule import AppRule, Rule

    definition = KoreParser(
        (definition_directory / "definition.kore").read_text()
    ).definition()
    symbols: set[str] = set()
    for axiom in (
        sentence
        for module in definition.modules
        for sentence in module.sentences
    ):
        if (
            "simplification" not in axiom.attrs_by_key
            or f"{source_marker})" not in axiom.text
            or not Rule.is_rule(axiom)
        ):
            continue
        rule = Rule.from_axiom(axiom)
        if not isinstance(rule, AppRule):
            continue
        if any(function in rule.lhs.symbol for function in summary_functions):
            continue
        symbols |= collect_symbols(rule.lhs) | collect_symbols(rule.rhs)
        requires = getattr(rule, "req", None)
        if requires is not None:
            symbols |= collect_symbols(requires)
    symbols.discard("inj")
    return symbols


def _widen_projection(definition: object, extra_symbols: set[str]) -> object:
    from pyk.kore.manip import collect_symbols
    from pyk.utils import FrozenDict

    keep = set(definition._config_symbols()) | set(
        definition._rewrite_symbols()
    )
    pending = {
        symbol for symbol in extra_symbols if symbol in definition.symbols
    }
    while pending:
        symbol = pending.pop()
        if symbol in keep:
            continue
        keep.add(symbol)
        for rule in definition.functions.get(symbol, ()):
            pending |= collect_symbols(rule.to_axiom().pattern)
        for sort in definition._symbol_sorts(symbol):
            if sort in definition.collections:
                collection = definition.collections[sort]
                pending |= {
                    collection.concat,
                    collection.element,
                    collection.unit,
                }
    symbols = FrozenDict(
        (symbol, declaration)
        for symbol, declaration in definition.symbols.items()
        if symbol in keep
    )
    return definition.let(symbols=symbols).project_to_symbols()


def _emit_lemmas(
    definition_directory: Path,
    package_directory: Path,
    library_name: str,
    summary_functions: tuple[str, ...],
    source_marker: str,
    source_rule_inventory: Path,
) -> int:
    from pyk.klean.__main__ import _load_defn
    from pyk.klean.k2lean4 import (
        K2Lean4,
        _param_sorts,
        _symbol_ident,
        _var_ident,
    )
    from pyk.kore.manip import collect_symbols
    from pyk.kore.parser import KoreParser
    from pyk.kore.rule import AppRule, Rule
    from pyk.kore.syntax import App, EVar

    definition = KoreParser(
        (definition_directory / "definition.kore").read_text()
    ).definition()
    full_definition = _load_defn(definition_directory)
    converter = K2Lean4(full_definition)

    def collect_variables(pattern: object, variables: dict[str, str]) -> None:
        if isinstance(pattern, EVar):
            variables[pattern.name] = pattern.sort.name
        elif isinstance(pattern, App):
            for argument in pattern.args:
                collect_variables(argument, variables)

    try:
        inventory_document = json.loads(source_rule_inventory.read_text())
        source_rules = inventory_document["source_rules"]
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise RuntimeError("source rule inventory is malformed") from error
    if not isinstance(source_rules, list):
        raise RuntimeError("source rule inventory must contain a rule list")
    eligible_by_line: dict[int, dict[str, object]] = {}
    for item in source_rules:
        if not isinstance(item, dict):
            raise RuntimeError("source rule inventory entry is malformed")
        if item.get("classification") != "TRUST_OBLIGATION":
            continue
        start_line = item.get("start_line")
        if not isinstance(start_line, int) or start_line in eligible_by_line:
            raise RuntimeError(
                "source trust rules must have unique integer start lines"
            )
        eligible_by_line[start_line] = item

    propositions: list[
        tuple[int, str, dict[str, object], set[str]]
    ] = []
    used_symbols: set[str] = set()
    for axiom in (
        sentence
        for module in definition.modules
        for sentence in module.sentences
    ):
        if (
            "simplification" not in axiom.attrs_by_key
            or f"{source_marker})" not in axiom.text
            or not Rule.is_rule(axiom)
        ):
            continue
        rule = Rule.from_axiom(axiom)
        if not isinstance(rule, AppRule):
            continue
        if any(function in rule.lhs.symbol for function in summary_functions):
            continue
        location = re.search(
            r"Location\((\d+),(\d+),(\d+),(\d+)\)", axiom.text
        )
        if location is None:
            raise RuntimeError("eligible KORE trust rule has no source location")
        start_line = int(location.group(1))
        source_rule = eligible_by_line.get(start_line)
        if source_rule is None:
            raise RuntimeError(
                f"KORE trust rule at line {start_line} has no source inventory entry"
            )
        lhs = converter._transform_pattern(rule.lhs, concrete=True)
        rhs = converter._transform_pattern(rule.rhs, concrete=True)
        variables: dict[str, str] = {}
        collect_variables(rule.lhs, variables)
        collect_variables(rule.rhs, variables)
        rule_symbols = collect_symbols(rule.lhs) | collect_symbols(rule.rhs)
        used_symbols |= rule_symbols
        hypothesis = ""
        requires = getattr(rule, "req", None)
        if requires is not None:
            requires_term = str(
                converter._transform_pattern(requires, concrete=True)
            )
            if requires_term not in ("true", "(true)"):
                collect_variables(requires, variables)
                required_symbols = collect_symbols(requires)
                rule_symbols |= required_symbols
                used_symbols |= required_symbols
                hypothesis = f" (h : {requires_term} = true)"
        binders = (
            " ".join(
                f"({_var_ident(name)} : {sort})"
                for name, sort in variables.items()
            )
            + hypothesis
        )
        proposition = f"{lhs} = {rhs}"
        if binders.strip():
            proposition = f"∀ {binders.strip()}, {proposition}"
        propositions.append(
            (start_line, proposition, source_rule, rule_symbols)
        )

    propositions.sort(key=lambda item: item[0])
    seen_ids = [
        str(source_rule["source_rule_id"])
        for _line, _proposition, source_rule, _symbols in propositions
    ]
    expected_ids = [
        str(item["source_rule_id"])
        for item in source_rules
        if isinstance(item, dict)
        and item.get("classification") == "TRUST_OBLIGATION"
    ]
    if seen_ids != expected_ids:
        raise RuntimeError(
            "source trust rules and generated Lean obligations are not bijective"
        )

    parameters: list[dict[str, str]] = []
    for symbol in sorted(used_symbols):
        if symbol == "inj" or symbol not in full_definition.symbols:
            continue
        declaration = full_definition.symbols[symbol]
        if "function" not in declaration.attrs_by_key:
            continue
        parameter_sorts = list(_param_sorts(declaration))
        lean_type = (
            " → ".join(parameter_sorts + [declaration.sort.name])
            if parameter_sorts
            else declaration.sort.name
        )
        binding = {
            "kore_symbol": symbol,
            "name": _symbol_ident(symbol),
            "type": lean_type,
            "source_rule_ids": [
                str(source_rule["source_rule_id"])
                for _line, _proposition, source_rule, symbols in propositions
                if symbol in symbols
            ],
        }
        binding["binding_sha256"] = hashlib.sha256(
            json.dumps(
                binding, sort_keys=True, separators=(",", ":")
            ).encode()
        ).hexdigest()
        parameters.append(binding)

    namespace = f"{library_name}.Lemmas"
    lines = [
        f"import {library_name}.Inj",
        "",
        "/- K trust-boundary goals. The second-pass agent must replace every",
        "   writable opaque stub with an honest definition and prove this",
        "   immutable proposition in the separate Proof.lean workspace. -/",
        "",
        f"namespace {namespace}",
        "",
    ]
    if propositions:
        lines.append("def targetStatement")
        for parameter in parameters:
            lines.append(
                f"    ({parameter['name']} : {parameter['type']})"
            )
        lines.extend(
            (
                "    : Prop :=",
                "    "
                + "\n    ∧ ".join(
                    f"({proposition})"
                    for _line, proposition, _source_rule, _symbols in propositions
                ),
                "",
            )
        )
    lines.append(f"end {namespace}")
    lemma_file = package_directory / library_name / "Lemmas.lean"
    lemma_file.write_text("\n".join(lines) + "\n")
    root = package_directory / f"{library_name}.lean"
    root_text = root.read_text()
    if f"{library_name}.Lemmas" not in root_text:
        root.write_text(root_text + f"import {library_name}.Lemmas\n")
    mappings = []
    for _line, proposition, source_rule, _symbols in propositions:
        mappings.append(
            {
                "source_rule_id": source_rule["source_rule_id"],
                "source_span": {
                    "start_line": source_rule["start_line"],
                    "end_line": source_rule["end_line"],
                },
                "lean_conjunct": proposition,
                "lean_conjunct_sha256": hashlib.sha256(
                    proposition.encode()
                ).hexdigest(),
            }
        )
    (package_directory / "obligation-map.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "source_rules": source_rules,
                "obligations": mappings,
                "trust_parameters": parameters,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    return len(propositions)


def _patch_prelude(package_directory: Path, library_name: str) -> None:
    prelude = package_directory / library_name / "Prelude.lean"
    text = prelude.read_text()
    if "SortFloat" in text:
        return
    if _PRELUDE_ANCHOR not in text:
        raise RuntimeError(
            "generated Prelude.lean layout changed; Float patch cannot apply"
        )
    prelude.write_text(
        text.replace(
            _PRELUDE_ANCHOR,
            _PRELUDE_FLOAT_ABBREV + _PRELUDE_ANCHOR,
        )
    )


def main() -> None:
    try:
        from pyk.klean.__main__ import _load_defn, _parse_args
        from pyk.klean.generate import generate
    except ModuleNotFoundError as error:
        raise SystemExit(
            "error: pyk is unavailable; use the pinned Klean container"
        ) from error

    _install_float_support()
    arguments = list(sys.argv)
    emit_lemmas = "--lemmas" in arguments
    arguments = [argument for argument in arguments if argument != "--lemmas"]
    summary_functions: list[str] = []
    while "--spec-func" in arguments:
        index = arguments.index("--spec-func")
        if index + 1 >= len(arguments):
            raise SystemExit("error: --spec-func requires a value")
        summary_functions.append(arguments[index + 1])
        del arguments[index : index + 2]
    source_marker = "verification.k"
    if "--lemma-source" in arguments:
        index = arguments.index("--lemma-source")
        if index + 1 >= len(arguments):
            raise SystemExit("error: --lemma-source requires a value")
        source_marker = arguments[index + 1]
        del arguments[index : index + 2]
    source_rule_inventory = None
    if "--source-rule-inventory" in arguments:
        index = arguments.index("--source-rule-inventory")
        if index + 1 >= len(arguments):
            raise SystemExit("error: --source-rule-inventory requires a value")
        source_rule_inventory = Path(arguments[index + 1])
        del arguments[index : index + 2]
    if emit_lemmas and source_rule_inventory is None:
        raise SystemExit("error: --lemmas requires --source-rule-inventory")
    sys.argv = arguments

    namespace = _parse_args(sys.argv)
    output_directory = namespace.output_dir or Path()
    package_directory = output_directory / namespace.package_name
    if package_directory.exists() or package_directory.is_symlink():
        raise SystemExit(f"error: directory exists: {package_directory}")
    definition = _load_defn(namespace.definition_dir)
    if namespace.rules:
        substrings = tuple(namespace.rules)
        rewrites = tuple(
            rewrite
            for rewrite in definition.rewrites
            if rewrite.label
            and any(value in rewrite.label for value in substrings)
        )
        definition = definition.let(rewrites=rewrites)
    lemma_symbols: set[str] = set()
    if emit_lemmas:
        lemma_symbols = _trust_lemma_symbols(
            namespace.definition_dir,
            tuple(summary_functions),
            source_marker,
        )
    if lemma_symbols:
        definition = _widen_projection(definition, lemma_symbols)
    else:
        definition = definition.project_to_rewrites()
    result_directory = generate(
        defn=definition,
        output_dir=output_directory,
        context={
            "package_name": namespace.package_name,
            "library_name": namespace.library_name,
        },
        config={
            "derive_beq": namespace.derive_beq,
            "derive_decidableeq": namespace.derive_decidableeq,
        },
    )
    make_generated_tree_owner_writable(result_directory)
    _patch_prelude(result_directory, namespace.library_name)
    if emit_lemmas:
        count = emit_lemmas_or_raise(
            lambda: _emit_lemmas(
                namespace.definition_dir,
                result_directory,
                namespace.library_name,
                tuple(summary_functions),
                source_marker,
                source_rule_inventory,
            )
        )
        print(f"lemmas: {count}", file=sys.stderr)
    print(result_directory)


if __name__ == "__main__":
    main()
