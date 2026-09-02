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

_LEAN_RESERVED_WORDS = frozenset(
    {
        "as",
        "by",
        "class",
        "def",
        "deriving",
        "do",
        "else",
        "end",
        "export",
        "extends",
        "extern",
        "false",
        "for",
        "forall",
        "from",
        "fun",
        "if",
        "import",
        "in",
        "inductive",
        "infix",
        "infixl",
        "infixr",
        "instance",
        "let",
        "macro",
        "match",
        "mutual",
        "namespace",
        "opaque",
        "open",
        "partial",
        "private",
        "protected",
        "return",
        "section",
        "structure",
        "syntax",
        "then",
        "theorem",
        "true",
        "universe",
        "unsafe",
        "variable",
        "where",
        "while",
        "with",
    }
)


def quote_reserved_lean_identifiers(
    text: str, identifiers: set[str]
) -> str:
    """Quote bare K identifiers which Lean parses as reserved words."""

    for identifier in sorted(identifiers & _LEAN_RESERVED_WORDS):
        text = re.sub(
            rf"(?<![«A-Za-z0-9_?!'])(?:{re.escape(identifier)})"
            rf"(?![»A-Za-z0-9_?!'])",
            f"«{identifier}»",
            text,
        )
    return text


def _quoted_identifier(identifier: str) -> str:
    if identifier in _LEAN_RESERVED_WORDS:
        return f"«{identifier}»"
    return identifier


def lean_typed_equality(left: str, right: str, lean_type: str) -> str:
    return f"({left} : {lean_type}) = ({right} : {lean_type})"


def _definition_reserved_identifiers(
    definition: object, symbol_ident: Callable[[str], str]
) -> set[str]:
    sorts = getattr(definition, "sorts", {})
    identifiers = {
        name
        for name in sorts
        if name in _LEAN_RESERVED_WORDS
    }
    for sort in sorts:
        if sort.startswith("Sort") and sort.endswith("Cell"):
            stem = sort[4:-4]
            if stem:
                field = stem[0].lower() + stem[1:]
                if field in _LEAN_RESERVED_WORDS:
                    identifiers.add(field)
    identifiers.update(
        identifier
        for symbol in getattr(definition, "symbols", {})
        if (identifier := symbol_ident(symbol)) in _LEAN_RESERVED_WORDS
    )
    return identifiers


def _quote_generated_tree(root: Path, identifiers: set[str]) -> None:
    if not identifiers:
        return
    for path in Path(root).rglob("*.lean"):
        path.write_text(
            quote_reserved_lean_identifiers(path.read_text(), identifiers)
        )


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


def _source_rule_lines(source_rule_inventory: Path) -> dict[int, dict[str, object]]:
    try:
        document = json.loads(source_rule_inventory.read_text())
        source_rules = document["source_rules"]
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
    return eligible_by_line


def _source_rule_for_axiom(
    axiom: object,
    source_marker: str,
    eligible_by_line: dict[int, dict[str, object]],
) -> tuple[int, dict[str, object]] | None:
    text = str(getattr(axiom, "text", ""))
    if f"{source_marker})" not in text:
        return None
    location = re.search(r"Location\((\d+),(\d+),(\d+),(\d+)\)", text)
    if location is None:
        return None
    start_line = int(location.group(1))
    source_rule = eligible_by_line.get(start_line)
    if source_rule is None:
        return None
    return start_line, source_rule


def _trust_lemma_symbols(
    definition_directory: Path,
    summary_functions: tuple[str, ...],
    source_marker: str,
    source_rule_inventory: Path,
) -> set[str]:
    from pyk.kore.manip import collect_symbols
    from pyk.kore.parser import KoreParser
    from pyk.kore.rule import AppRule, Rule

    definition = KoreParser(
        (definition_directory / "definition.kore").read_text()
    ).definition()
    eligible_by_line = _source_rule_lines(source_rule_inventory)
    symbols: set[str] = set()
    seen_lines: list[int] = []
    for axiom in (
        sentence
        for module in definition.modules
        for sentence in module.sentences
    ):
        selected = _source_rule_for_axiom(
            axiom, source_marker, eligible_by_line
        )
        if selected is None or not Rule.is_rule(axiom):
            continue
        rule = Rule.from_axiom(axiom)
        start_line, _source_rule = selected
        seen_lines.append(start_line)
        symbols |= collect_symbols(rule.lhs) | collect_symbols(rule.rhs)
        requires = getattr(rule, "req", None)
        if requires is not None:
            symbols |= collect_symbols(requires)
        ensures = getattr(rule, "ens", None)
        if ensures is not None:
            symbols |= collect_symbols(ensures)
    if sorted(seen_lines) != sorted(eligible_by_line):
        raise RuntimeError(
            "source trust rules and KORE rules are not bijective: "
            f"expected lines {list(eligible_by_line)}, observed {seen_lines}"
        )
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
    from pyk.kore.rule import Rule
    from pyk.kore.syntax import And, DV, EVar, Equals, SortApp, String

    definition = KoreParser(
        (definition_directory / "definition.kore").read_text()
    ).definition()
    full_definition = _load_defn(definition_directory)
    converter = K2Lean4(full_definition)

    def is_generated_wildcard(pattern: object) -> bool:
        return isinstance(pattern, EVar) and re.fullmatch(
            r"Var'Unds'Gen\d+", pattern.name
        ) is not None

    def normalize_pattern(pattern: object) -> object:
        def normalize(current: object) -> object:
            if isinstance(current, And) and len(current.ops) == 2:
                left, right = current.ops
                if is_generated_wildcard(left):
                    return right
                if is_generated_wildcard(right):
                    return left
            return current

        return pattern.bottom_up(normalize)

    def is_true(pattern: object) -> bool:
        return (
            isinstance(pattern, DV)
            and isinstance(pattern.sort, SortApp)
            and pattern.sort.name == "SortBool"
            and isinstance(pattern.value, String)
            and pattern.value.value == "true"
        )

    def conclusion(rule: object) -> str:
        lhs = normalize_pattern(rule.lhs)
        rhs = normalize_pattern(rule.rhs)
        if isinstance(lhs, Equals) and is_true(rhs):
            left = converter._transform_pattern(
                normalize_pattern(lhs.left), concrete=True
            )
            right = converter._transform_pattern(
                normalize_pattern(lhs.right), concrete=True
            )
            return f"{left} = {right}"
        left = converter._transform_pattern(lhs, concrete=True)
        right = converter._transform_pattern(rhs, concrete=True)
        return lean_typed_equality(
            str(left), str(right), rule.sort.name
        )

    def collect_variables(pattern: object, variables: dict[str, str]) -> None:
        pending = [pattern]
        while pending:
            current = pending.pop()
            if isinstance(current, EVar):
                variables[current.name] = current.sort.name
            pending.extend(getattr(current, "patterns", ()))

    eligible_by_line = _source_rule_lines(source_rule_inventory)
    source_rules = list(eligible_by_line.values())
    reserved_identifiers = _definition_reserved_identifiers(
        full_definition, _symbol_ident
    )

    propositions: list[
        tuple[int, str, dict[str, object], set[str]]
    ] = []
    used_symbols: set[str] = set()
    for axiom in (
        sentence
        for module in definition.modules
        for sentence in module.sentences
    ):
        selected = _source_rule_for_axiom(
            axiom, source_marker, eligible_by_line
        )
        if selected is None or not Rule.is_rule(axiom):
            continue
        rule = Rule.from_axiom(axiom)
        start_line, source_rule = selected
        normalized_lhs = normalize_pattern(rule.lhs)
        normalized_rhs = normalize_pattern(rule.rhs)
        variables: dict[str, str] = {}
        collect_variables(normalized_lhs, variables)
        collect_variables(normalized_rhs, variables)
        rule_symbols = collect_symbols(normalized_lhs) | collect_symbols(
            normalized_rhs
        )
        used_symbols |= rule_symbols
        hypothesis = ""
        requires = getattr(rule, "req", None)
        if requires is not None:
            requires = normalize_pattern(requires)
            requires_term = str(
                converter._transform_pattern(requires, concrete=True)
            )
            if requires_term not in ("true", "(true)"):
                collect_variables(requires, variables)
                required_symbols = collect_symbols(requires)
                rule_symbols |= required_symbols
                used_symbols |= required_symbols
                hypothesis = f" (h : {requires_term} = true)"
        ensures = getattr(rule, "ens", None)
        if ensures is not None:
            ensures = normalize_pattern(ensures)
            collect_variables(ensures, variables)
            ensured_symbols = collect_symbols(ensures)
            rule_symbols |= ensured_symbols
            used_symbols |= ensured_symbols
        binders = (
            " ".join(
                f"({_quoted_identifier(_var_ident(name))} : {sort})"
                for name, sort in variables.items()
            )
            + hypothesis
        )
        proposition = conclusion(rule)
        if binders.strip():
            proposition = f"∀ {binders.strip()}, {proposition}"
        proposition = quote_reserved_lean_identifiers(
            proposition, reserved_identifiers
        )
        propositions.append(
            (start_line, proposition, source_rule, rule_symbols)
        )

    propositions.sort(key=lambda item: item[0])
    seen_ids = [
        str(source_rule["source_rule_id"])
        for _line, _proposition, source_rule, _symbols in propositions
    ]
    expected_ids = [str(item["source_rule_id"]) for item in source_rules]
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
        lean_type = quote_reserved_lean_identifiers(
            lean_type, reserved_identifiers
        )
        name = _quoted_identifier(_symbol_ident(symbol))
        binding = {
            "kore_symbol": symbol,
            "name": name,
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

    # KORE is a recursively nested concrete syntax.  Large but valid frozen
    # definitions (for example generated Unicode tables) exceed Python's
    # conservative default recursion limit inside the pinned pyk parser.
    sys.setrecursionlimit(max(sys.getrecursionlimit(), 20_000))
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
            source_rule_inventory,
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
    from pyk.klean.k2lean4 import _symbol_ident

    reserved_identifiers = _definition_reserved_identifiers(
        definition, _symbol_ident
    )
    _quote_generated_tree(result_directory, reserved_identifiers)
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
