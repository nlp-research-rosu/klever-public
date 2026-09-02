#!/usr/bin/env python3
"""Float-aware, lemma-emitting wrapper around the pinned pyk Klean generator."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import sys
from collections.abc import Collection, Mapping
from graphlib import TopologicalSorter
from pathlib import Path
from typing import Callable, TypeVar


_PRELUDE_FLOAT_ABBREV = "abbrev SortFloat        : Type := Float\n"
_PRELUDE_ANCHOR = "abbrev SortInt          : Type := Int\n"
T = TypeVar("T")

# Sort-polymorphic K hook symbols (for example ``Lblite{SortSort}``) carry a
# ``SortVar`` parameter, so pyk's ``_param_sorts`` cannot give them a monomorphic
# KORE signature and they cannot become opaque ``targetStatement`` parameters.
# k2lean4 renders every instance to a single fixed ident (``Lblite`` -> ``kite``
# via ``_SYMBOL_OVERRIDES``, discarding the sort argument), so one honest total
# polymorphic Lean definition models all of a proposition's instances.  The K
# ``ite`` hook is total, and the lemma view is unwrapped (function symbols are
# applied directly, never Option-valued — see the generated targetStatement),
# so the model is a plain total definition.  Keyed by the ident k2lean4 emits.
_POLYMORPHIC_LEMMA_HOOK_DEFS = {
    "kite": "def kite {α : Type} (c : SortBool) (t e : α) : α := cond c t e",
}


def _polymorphic_lemma_hook_definition(
    declaration: object,
    symbol: str,
    symbol_ident: Callable[[str], str],
    sort_app_type: type,
) -> str | None:
    """Model a sort-polymorphic hook symbol, or None when it is monomorphic.

    Returns the honest total Lean definition line for a symbol whose KORE
    declaration carries a non-``SortApp`` parameter or result sort (so pyk cannot
    type an opaque binding for it), keyed by the ident k2lean4 renders.  Returns
    None for a fully monomorphic declaration, which keeps its opaque binding.
    Raises for a polymorphic symbol that is not modeled, to fail closed rather
    than emit a proposition that references an undefined identifier.
    """

    sorts = (*declaration.param_sorts, declaration.sort)
    if all(isinstance(sort, sort_app_type) for sort in sorts):
        return None
    ident = symbol_ident(symbol)
    definition_line = _POLYMORPHIC_LEMMA_HOOK_DEFS.get(ident)
    if definition_line is None:
        raise RuntimeError(
            f"sort-polymorphic lemma symbol without a Lean model: {symbol}"
        )
    return definition_line

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
        "prefix",
        "prec",
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


def deterministic_subsort_pairs(
    subsorts: Mapping[str, Collection[str]],
) -> tuple[tuple[str, str], ...]:
    """Return K subsort edges in a canonical order."""

    return tuple(
        (subsort, supersort)
        for supersort in sorted(subsorts)
        for subsort in sorted(subsorts[supersort])
    )


def deterministic_ordered_sccs(
    dependencies: Mapping[str, Collection[str]],
) -> list[list[str]]:
    """Match pinned Klean's SCC ordering without hash-order dependence."""

    normalized = {
        element: tuple(sorted(dependencies[element]))
        for element in sorted(dependencies)
    }
    component_by_element: dict[str, int] = {}
    next_component = 0
    for element, dependency_elements in normalized.items():
        if element in component_by_element:
            continue
        component_by_element[element] = next_component
        for dependency in dependency_elements:
            if element in normalized[dependency]:
                component_by_element[dependency] = next_component
        next_component += 1

    elements_by_component: dict[int, set[str]] = {}
    for element, component in component_by_element.items():
        elements_by_component.setdefault(component, set()).add(element)

    component_dependencies: dict[int, tuple[int, ...]] = {}
    ordered_components = sorted(
        elements_by_component,
        key=lambda component: tuple(sorted(elements_by_component[component])),
    )
    for component in ordered_components:
        dependency_components = {
            component_by_element[dependency]
            for element in elements_by_component[component]
            for dependency in normalized[element]
            if component_by_element[dependency] != component
        }
        component_dependencies[component] = tuple(
            sorted(
                dependency_components,
                key=lambda dependency: tuple(
                    sorted(elements_by_component[dependency])
                ),
            )
        )

    order = tuple(TopologicalSorter(component_dependencies).static_order())
    return [sorted(elements_by_component[component]) for component in order]


def _install_deterministic_klean_ordering() -> None:
    """Replace the two hash-sensitive orderings in pinned pyk/Klean."""

    from pyk.klean import k2lean4

    def deterministic_inj_commands(converter: object) -> tuple[object, ...]:
        return tuple(
            converter._inj_instance(subsort, supersort)
            for subsort, supersort in deterministic_subsort_pairs(
                converter.defn.subsorts
            )
            if not supersort.endswith("CellMap")
        )

    k2lean4._ordered_sccs = deterministic_ordered_sccs
    k2lean4.K2Lean4._inj_commands = deterministic_inj_commands


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


def canonicalize_lean_injection_chains(
    text: str,
    subsorts: Mapping[str, Collection[str]],
) -> str:
    """Render explicit injections with Klean's canonical subsort semantics."""

    descendants = {
        supersort: set(direct_subsorts)
        for supersort, direct_subsorts in subsorts.items()
    }
    changed = True
    while changed:
        changed = False
        for supersort, current in descendants.items():
            expanded = set(current)
            for subsort in current:
                expanded.update(descendants.get(subsort, ()))
            if expanded != current:
                descendants[supersort] = expanded
                changed = True

    head = re.compile(
        r"(?P<outer>Sort[A-Za-z0-9_]+)\.inj_"
        r"(?P<middle>Sort[A-Za-z0-9_]+)\s+"
    )

    def strip_balanced_parentheses(argument: str) -> str:
        stripped = argument.strip()
        while stripped.startswith("("):
            try:
                inner, end = _lean_application_argument(stripped, 0)
            except ValueError:
                break
            if end != len(stripped):
                break
            stripped = inner[1:-1].strip()
        return stripped

    while True:
        replacement: tuple[int, int, str] | None = None
        for outer_match in head.finditer(text):
            try:
                outer_argument, outer_end = _lean_application_argument(
                    text, outer_match.end()
                )
            except ValueError:
                continue
            inner_text = strip_balanced_parentheses(outer_argument)
            inner_match = head.match(inner_text)
            if (
                inner_match is None
                or inner_match.group("outer")
                != outer_match.group("middle")
            ):
                continue
            try:
                inner_argument, inner_end = _lean_application_argument(
                    inner_text, inner_match.end()
                )
            except ValueError:
                continue
            if inner_text[inner_end:].strip():
                continue
            innermost_sort = inner_match.group("middle")
            outer_sort = outer_match.group("outer")
            if innermost_sort not in descendants.get(outer_sort, set()):
                continue
            replacement = (
                outer_match.start(),
                outer_end,
                f"{outer_sort}.inj_{innermost_sort} {inner_argument}",
            )
            break
        if replacement is None:
            break
        start, end, canonical = replacement
        text = text[:start] + canonical + text[end:]

    while True:
        replacement = None
        for match in head.finditer(text):
            outer_sort = match.group("outer")
            subsort = match.group("middle")
            if (
                subsort not in descendants.get(outer_sort, set())
                or not descendants.get(subsort)
            ):
                continue
            try:
                argument, end = _lean_application_argument(
                    text, match.end()
                )
            except ValueError:
                continue
            replacement = (
                match.start(),
                end,
                f"(@inj {subsort} {outer_sort}) {argument}",
            )
            break
        if replacement is None:
            return text
        start, end, canonical = replacement
        text = text[:start] + canonical + text[end:]


def lean_predicate_equivalence(left: str, right: str) -> str:
    return f"({left}) ↔ ({right})"


def _lean_application_argument(text: str, start: int) -> tuple[str, int]:
    while start < len(text) and text[start].isspace():
        start += 1
    if start >= len(text):
        raise ValueError("missing Lean application argument")
    if text[start] != "(":
        end = start
        while end < len(text) and not text[end].isspace():
            end += 1
        return text[start:end], end
    depth = 0
    for end in range(start, len(text)):
        if text[end] == "(":
            depth += 1
        elif text[end] == ")":
            depth -= 1
            if depth == 0:
                return text[start : end + 1], end + 1
    raise ValueError("unbalanced Lean application argument")


def lean_requires_proposition(term: str) -> str:
    """Render K's polymorphic equality condition as Lean equality."""

    prefix = "«_==K_»"
    if term.startswith(prefix):
        try:
            left, offset = _lean_application_argument(term, len(prefix))
            right, offset = _lean_application_argument(term, offset)
        except ValueError:
            pass
        else:
            if not term[offset:].strip():
                return f"{left} = {right}"
    return f"({term}) = true"


def is_k_equality_identifier(identifier: str) -> bool:
    return identifier in {"_==K_", "«_==K_»"}


def lean_rule_relation(
    left: str, right: str, sort_name: str
) -> str:
    """Render a K rule as equality or as a configuration rewrite."""

    if sort_name == "SortGeneratedTopCell":
        return f"Rewrites {left} {right}"
    return lean_typed_equality(left, right, sort_name)


def operational_trust_rewrite_uid(
    rule_uid: str, sort_name: str
) -> str | None:
    """Return the UID only when the trust rule is an operational rewrite."""

    if sort_name == "SortGeneratedTopCell":
        return rule_uid
    return None


def lean_quantified_obligation(
    proposition: str,
    *,
    universal_binders: tuple[str, ...],
    existential_binders: tuple[str, ...],
    hypotheses: tuple[str, ...] = (),
) -> str:
    """Place K rule inputs outside and fresh outputs inside the goal."""

    if existential_binders:
        proposition = (
            f"∃ {' '.join(existential_binders)}, {proposition}"
        )
    outer = universal_binders + hypotheses
    if outer:
        proposition = f"∀ {' '.join(outer)}, {proposition}"
    return proposition


def normalize_generated_wildcards(
    patterns: tuple[object, ...],
    *,
    evar_type: type,
    and_type: type,
) -> tuple[object, ...]:
    """Propagate K frontend wildcard intersections across one rule."""

    def wildcard_name(pattern: object) -> str | None:
        if not isinstance(pattern, evar_type):
            return None
        name = getattr(pattern, "name", None)
        if not isinstance(name, str) or re.fullmatch(
            r"Var'Unds'Gen\d+", name
        ) is None:
            return None
        return name

    bindings: dict[str, object] = {}
    pending = list(patterns)
    while pending:
        current = pending.pop()
        if isinstance(current, and_type) and len(current.ops) == 2:
            left, right = current.ops
            left_name = wildcard_name(left)
            right_name = wildcard_name(right)
            if left_name is not None and right_name is None:
                previous = bindings.setdefault(left_name, right)
                if previous != right:
                    raise RuntimeError(
                        "generated K wildcard has conflicting constraints"
                    )
            if right_name is not None and left_name is None:
                previous = bindings.setdefault(right_name, left)
                if previous != left:
                    raise RuntimeError(
                        "generated K wildcard has conflicting constraints"
                    )
        pending.extend(getattr(current, "patterns", ()))

    def strip_intersections(pattern: object) -> object:
        def strip(current: object) -> object:
            if isinstance(current, and_type) and len(current.ops) == 2:
                left, right = current.ops
                if wildcard_name(left) is not None:
                    return right
                if wildcard_name(right) is not None:
                    return left
            return current

        return pattern.bottom_up(strip)

    resolved: dict[str, object] = {}

    def resolve(name: str, active: frozenset[str]) -> object:
        if name in resolved:
            return resolved[name]
        if name in active:
            raise RuntimeError("generated K wildcard constraints are cyclic")
        value = strip_intersections(bindings[name])

        def substitute(current: object) -> object:
            nested = wildcard_name(current)
            if nested is not None and nested in bindings:
                return resolve(nested, active | {name})
            return current

        value = value.bottom_up(substitute)
        resolved[name] = value
        return value

    def normalize(pattern: object) -> object:
        stripped = strip_intersections(pattern)

        def substitute(current: object) -> object:
            name = wildcard_name(current)
            if name is not None and name in bindings:
                return resolve(name, frozenset())
            return current

        return stripped.bottom_up(substitute)

    return tuple(normalize(pattern) for pattern in patterns)


def _pattern_sort_names(pattern: object) -> set[str]:
    """Collect concrete sort names needed to render a KORE pattern in Lean."""

    result: set[str] = set()
    pending = [pattern]
    seen: set[int] = set()
    while pending:
        current = pending.pop()
        identity = id(current)
        if identity in seen:
            continue
        seen.add(identity)
        for attribute in ("sort", "op_sort"):
            sort = getattr(current, attribute, None)
            name = getattr(sort, "name", None)
            if isinstance(name, str):
                result.add(name)
        for sort in getattr(current, "sorts", ()):
            name = getattr(sort, "name", None)
            if isinstance(name, str):
                result.add(name)
        pending.extend(getattr(current, "patterns", ()))
    return result


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
    observed_line = int(location.group(1))
    matches = [
        source_rule
        for source_rule in eligible_by_line.values()
        if isinstance(source_rule.get("start_line"), int)
        and isinstance(source_rule.get("end_line"), int)
        and source_rule["start_line"] <= observed_line <= source_rule["end_line"]
    ]
    if not matches:
        return None
    if len(matches) != 1:
        raise RuntimeError("KORE source location matches multiple trust rules")
    source_rule = matches[0]
    return int(source_rule["start_line"]), source_rule


def _trust_lemma_dependencies(
    definition_directory: Path,
    summary_functions: tuple[str, ...],
    source_marker: str,
    source_rule_inventory: Path,
) -> tuple[set[str], set[str], set[str], bool]:
    from pyk.kore.manip import collect_symbols
    from pyk.kore.parser import KoreParser
    from pyk.kore.rule import AppRule, Rule

    definition = KoreParser(
        (definition_directory / "definition.kore").read_text()
    ).definition()
    eligible_by_line = _source_rule_lines(source_rule_inventory)
    symbols: set[str] = set()
    sorts: set[str] = set()
    rewrite_uids: set[str] = set()
    needs_operational_rewrites = False
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
        rewrite_uid = operational_trust_rewrite_uid(
            rule.uid, rule.sort.name
        )
        if rewrite_uid is not None:
            rewrite_uids.add(rewrite_uid)
            needs_operational_rewrites = True
        patterns = [rule.lhs, rule.rhs]
        requires = getattr(rule, "req", None)
        if requires is not None:
            patterns.append(requires)
        ensures = getattr(rule, "ens", None)
        if ensures is not None:
            patterns.append(ensures)
        for pattern in patterns:
            symbols |= collect_symbols(pattern)
            sorts |= _pattern_sort_names(pattern)
    if sorted(seen_lines) != sorted(eligible_by_line):
        raise RuntimeError(
            "source trust rules and KORE rules are not bijective: "
            f"expected lines {list(eligible_by_line)}, observed {seen_lines}"
        )
    symbols.discard("inj")
    return symbols, sorts, rewrite_uids, needs_operational_rewrites


def _widen_projection(
    definition: object,
    extra_symbols: set[str],
    extra_sorts: set[str],
) -> object:
    from pyk.utils import FrozenDict

    baseline = set(definition._config_symbols()) | set(
        definition._rewrite_symbols()
    )
    keep = baseline | {
        symbol for symbol in extra_symbols if symbol in definition.symbols
    }
    symbols = FrozenDict(
        (symbol, declaration)
        for symbol, declaration in definition.symbols.items()
        if symbol in keep
    )
    # Retain executable equations required by the rewrite projection.  The
    # immutable target statement separately parameterizes functions used by
    # trust obligations, so it does not assume those equations.
    functions = FrozenDict(
        (symbol, rules)
        for symbol, rules in definition.functions.items()
        if symbol in baseline
    )
    projected = definition.let(
        symbols=symbols, functions=functions
    ).project_to_symbols()
    retained_sorts = set(projected.sorts) | extra_sorts
    sorts = FrozenDict(
        (sort, declaration)
        for sort, declaration in definition.sorts.items()
        if sort in retained_sorts
    )
    subsorts = FrozenDict(
        (
            supersort,
            frozenset(
                subsort
                for subsort in subsort_set
                if subsort in sorts
            ),
        )
        for supersort, subsort_set in definition.subsorts.items()
        if supersort in sorts
    )
    return projected.let(sorts=sorts, subsorts=subsorts)


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
    from pyk.kore.syntax import And, DV, EVar, Equals, MLQuant, SortApp, String, SVar, Top

    definition = KoreParser(
        (definition_directory / "definition.kore").read_text()
    ).definition()
    full_definition = _load_defn(definition_directory)
    converter = K2Lean4(full_definition)

    def lean_pattern(pattern: object) -> str:
        return canonicalize_lean_injection_chains(
            str(converter._transform_pattern(pattern, concrete=True)),
            full_definition.subsorts,
        )

    def is_generated_wildcard(pattern: object) -> bool:
        return isinstance(pattern, EVar) and re.fullmatch(
            r"Var'Unds'Gen\d+", pattern.name
        ) is not None

    def is_true(pattern: object) -> bool:
        if isinstance(pattern, Top) or is_generated_wildcard(pattern):
            return True
        if isinstance(pattern, And):
            return all(is_true(item) for item in pattern.ops)
        return (
            isinstance(pattern, DV)
            and isinstance(pattern.sort, SortApp)
            and pattern.sort.name == "SortBool"
            and isinstance(pattern.value, String)
            and pattern.value.value == "true"
        )

    def conclusion(lhs: object, rhs: object, sort_name: str) -> str:
        def equality(pattern: Equals) -> str:
            left = lean_pattern(pattern.left)
            right = lean_pattern(pattern.right)
            return lean_typed_equality(
                left, right, pattern.op_sort.name
            )

        if isinstance(lhs, Equals) and isinstance(rhs, Equals):
            return lean_predicate_equivalence(
                equality(lhs), equality(rhs)
            )
        if isinstance(lhs, Equals) and is_true(rhs):
            return equality(lhs)
        if isinstance(rhs, Equals) and is_true(lhs):
            return equality(rhs)
        if not sort_name.startswith("Sort"):
            # A rule whose sort is a sort variable (e.g. ``Q0``) is a
            # matching-logic predicate simplification (``#Ceil`` definedness
            # lemmas and the like).  Both sides are predicates, related by
            # logical equivalence rather than typed term equality at a
            # non-existent Lean type.
            return lean_predicate_equivalence(
                lean_pattern(lhs), lean_pattern(rhs)
            )
        left = lean_pattern(lhs)
        right = lean_pattern(rhs)
        return lean_rule_relation(left, right, sort_name)

    def collect_variables(pattern: object, variables: dict[str, str]) -> None:
        pending = [pattern]
        while pending:
            current = pending.pop()
            if isinstance(current, (EVar, SVar)):
                # Set variables (``@V``) in matching-logic simplification rules
                # bind exactly like element variables in the Lean obligation.
                variables[current.name] = current.sort.name
            pending.extend(getattr(current, "patterns", ()))

    def collect_ml_bound(pattern: object, names: set[str]) -> None:
        # Variables bound by a matching-logic quantifier (``\exists``/``\forall``)
        # are already bound inside the transformed proposition; they must not be
        # re-bound as rule-level existentials.
        pending = [pattern]
        while pending:
            current = pending.pop()
            if isinstance(current, MLQuant):
                names.add(current.var.name)
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
        raw_patterns = [rule.lhs, rule.rhs]
        raw_requires = getattr(rule, "req", None)
        raw_ensures = getattr(rule, "ens", None)
        if raw_requires is not None:
            raw_patterns.append(raw_requires)
        if raw_ensures is not None:
            raw_patterns.append(raw_ensures)
        normalized = iter(
            normalize_generated_wildcards(
                tuple(raw_patterns),
                evar_type=EVar,
                and_type=And,
            )
        )
        normalized_lhs = next(normalized)
        normalized_rhs = next(normalized)
        requires = next(normalized) if raw_requires is not None else None
        ensures = next(normalized) if raw_ensures is not None else None
        universal_variables: dict[str, str] = {}
        rhs_variables: dict[str, str] = {}
        collect_variables(normalized_lhs, universal_variables)
        collect_variables(normalized_rhs, rhs_variables)
        rule_symbols = collect_symbols(normalized_lhs) | collect_symbols(
            normalized_rhs
        )
        used_symbols |= rule_symbols
        hypotheses: list[str] = []
        if requires is not None:
            requires_term = lean_pattern(requires)
            if requires_term not in ("true", "(true)"):
                collect_variables(requires, universal_variables)
                required_symbols = collect_symbols(requires)
                requires_proposition = lean_requires_proposition(
                    requires_term
                )
                equality_requires = requires_proposition != (
                    f"({requires_term}) = true"
                )
                if equality_requires:
                    required_symbols = {
                        symbol
                        for symbol in required_symbols
                        if not is_k_equality_identifier(
                            _symbol_ident(symbol)
                        )
                    }
                rule_symbols |= required_symbols
                used_symbols |= required_symbols
                hypotheses.append(
                    f"(h : {requires_proposition})"
                )
        if ensures is not None:
            collect_variables(ensures, rhs_variables)
            ensured_symbols = collect_symbols(ensures)
            rule_symbols |= ensured_symbols
            used_symbols |= ensured_symbols
        ml_bound_variables: set[str] = set()
        collect_ml_bound(normalized_rhs, ml_bound_variables)
        existential_variables = {
            name: sort
            for name, sort in rhs_variables.items()
            if name not in universal_variables
            and name not in ml_bound_variables
        }
        proposition = conclusion(
            normalized_lhs, normalized_rhs, rule.sort.name
        )
        if ensures is not None:
            ensures_term = lean_pattern(ensures)
            if ensures_term not in ("true", "(true)"):
                proposition = f"({proposition}) ∧ ({ensures_term} = true)"
        proposition = lean_quantified_obligation(
            proposition,
            universal_binders=tuple(
                f"({_quoted_identifier(_var_ident(name))} : {sort})"
                for name, sort in universal_variables.items()
            ),
            existential_binders=tuple(
                f"({_quoted_identifier(_var_ident(name))} : {sort})"
                for name, sort in existential_variables.items()
            ),
            hypotheses=tuple(hypotheses),
        )
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
    polymorphic_definitions: dict[str, str] = {}
    for symbol in sorted(used_symbols):
        if symbol == "inj" or symbol not in full_definition.symbols:
            continue
        declaration = full_definition.symbols[symbol]
        if "function" not in declaration.attrs_by_key:
            continue
        # Sort-polymorphic hooks (for example K ``ite``) cannot carry a
        # monomorphic opaque binding; model them with an honest total Lean
        # definition instead and skip the opaque parameter.
        definition_line = _polymorphic_lemma_hook_definition(
            declaration, symbol, _symbol_ident, SortApp
        )
        if definition_line is not None:
            polymorphic_definitions[_symbol_ident(symbol)] = definition_line
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
        *(
            [f"import {library_name}.Rewrite"]
            if any(
                "Rewrites " in proposition
                for _line, proposition, _source_rule, _symbols
                in propositions
            )
            else []
        ),
        "",
        "/- K trust-boundary goals. The second-pass agent must replace every",
        "   writable opaque stub with an honest definition and prove this",
        "   immutable proposition in the separate Proof.lean workspace. -/",
        "",
        f"namespace {namespace}",
        "",
    ]
    if propositions and polymorphic_definitions:
        # Honest total models for sort-polymorphic hooks the propositions apply
        # (for example K ``ite`` rendered as ``kite``); emitted ahead of the
        # obligation so targetStatement resolves them in-namespace.
        for _ident, definition_line in sorted(polymorphic_definitions.items()):
            lines.append(definition_line)
        lines.append("")
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

    _install_deterministic_klean_ordering()

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
    lemma_symbols: set[str] = set()
    lemma_sorts: set[str] = set()
    trust_rewrite_uids: set[str] = set()
    needs_operational_rewrites = False
    if emit_lemmas:
        (
            lemma_symbols,
            lemma_sorts,
            trust_rewrite_uids,
            needs_operational_rewrites,
        ) = _trust_lemma_dependencies(
            namespace.definition_dir,
            tuple(summary_functions),
            source_marker,
            source_rule_inventory,
        )
    if needs_operational_rewrites:
        observed = {
            rewrite.uid
            for rewrite in definition.rewrites
            if rewrite.uid in trust_rewrite_uids
        }
        if observed != trust_rewrite_uids:
            raise RuntimeError(
                "Klean rewrite model is missing a selected trust rule"
            )
        definition = definition.let(
            rewrites=tuple(
                rewrite
                for rewrite in definition.rewrites
                if rewrite.uid not in trust_rewrite_uids
            )
        )
    elif namespace.rules:
        substrings = tuple(namespace.rules)
        rewrites = tuple(
            rewrite
            for rewrite in definition.rewrites
            if rewrite.label
            and any(value in rewrite.label for value in substrings)
        )
        definition = definition.let(rewrites=rewrites)
    if lemma_symbols or lemma_sorts:
        definition = _widen_projection(
            definition, lemma_symbols, lemma_sorts
        )
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
