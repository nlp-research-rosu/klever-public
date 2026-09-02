#!/usr/bin/env python3
"""Deterministically export one frozen K proof workspace to a Lean project."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import shlex
import stat
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


REPO = Path(__file__).resolve().parent.parent
KLEAN = REPO / "tools/klean.py"
KOMPILE_TIMEOUT = 480
KLEAN_TIMEOUT = 300
BUILD_TIMEOUT = 600

K_IDENTIFIER = r"[A-Za-z][A-Za-z0-9_'-]*"
SYNTAX_BLOCK_RE = re.compile(
    rf"(?ms)^[ \t]*syntax\s+(?P<ret>{K_IDENTIFIER})\s*::=\s*"
    r"(?P<body>.*?)"
    r"(?=^[ \t]*(?:syntax|rule|module|endmodule|imports)\b|\Z)"
)
FUNC_PRODUCTION_RE = re.compile(
    r"(?:\A|^[ \t]*\|)\s*"
    rf"(?P<name>{K_IDENTIFIER})\s*\((?P<args>[^)]*)\)\s*"
    r"\[(?P<attrs>[^\]]*)\]",
    re.M,
)
K_IDENTIFIER_END = r"(?![A-Za-z0-9_'-])"
MODULE_RE = re.compile(
    rf"(?m)^[ \t]*module\s+({K_IDENTIFIER}){K_IDENTIFIER_END}"
)
MODULE_BLOCK_RE = re.compile(
    rf"(?ms)^[ \t]*module\s+(?P<name>{K_IDENTIFIER}){K_IDENTIFIER_END}"
    r"(?P<body>.*?)\bendmodule\b"
)
IMPORT_RE = re.compile(
    rf"(?m)^[ \t]*imports\s+({K_IDENTIFIER}){K_IDENTIFIER_END}"
)
REQUIRES_RE = re.compile(r'requires\s+"([^"]+)"')
_TERM_HEAD_RE = re.compile(r"fail to show termination for\s*\n\s*(«[^»]+»|\S+)")
_TERM_CALL_RE = re.compile(r"Call from («[^»]+»|\S+) to («[^»]+»|\S+)")
_ELAB_LINE_RE = re.compile(
    r"error:\s+\S*Func\.lean:(\d+):\d+:\s+"
    r"(?:unknown identifier|Application type mismatch)"
)
_DEF_RE = re.compile(r"^(\s*)(?:noncomputable\s+)?def\s+(\S+)\b")
_NONCOMPUTABLE_RE = re.compile(r"(?m)^\s*noncomputable\s+def\s+(\S+)")
_LEAN_NAMESPACE_RE = re.compile(r"^\s*namespace\s+(\S+)\s*$")
_LEAN_END_RE = re.compile(r"^\s*end(?:\s+(\S+))?\s*$")
_LEAN_TRUST_DECL_RE = re.compile(
    r"^\s*(axiom|opaque)\s+(\S+)\s+(.+?)\s*$"
)
_RULE_HEAD_RE = re.compile(
    rf"(?m)^\s*rule(?:\s+\[[^\]]+\]:)?\s+"
    rf"(?P<name>{K_IDENTIFIER}){K_IDENTIFIER_END}"
)
_SYNTAX_PRODUCTION_LINE_RE = re.compile(
    rf"^(?P<prefix>[ \t]*(?:syntax\s+{K_IDENTIFIER}\s*::=\s*|\|\s*))"
    rf"(?P<name>{K_IDENTIFIER})\s*\((?P<args>[^)]*)\)"
    r"(?P<spacing>[ \t]*)(?P<attrs>\[[^\]]*\])?"
    r"(?P<suffix>[ \t]*(?://.*)?)$"
)

if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools import k_rule_inventory, lemma_discovery_contract


class KleanExportError(RuntimeError):
    pass


@dataclass(frozen=True)
class Func:
    name: str
    ret: str
    args: list[str]


@dataclass(frozen=True)
class DefinitionResolution:
    verification_file: Path
    verification_module: str
    syntax_module: str
    required_files: tuple[Path, ...]
    entry_files: tuple[Path, ...]


@dataclass(frozen=True)
class KompileCommand:
    source: Path
    main_module: str | None
    syntax_module: str | None
    backend: str | None


def _proof_kompile_commands(workspace: Path) -> tuple[KompileCommand, ...]:
    prove = workspace / "prove.sh"
    if not prove.is_file() or prove.is_symlink():
        return ()
    logical_lines = prove.read_text().replace("\\\n", " ").splitlines()
    commands: list[KompileCommand] = []
    for line in logical_lines:
        try:
            words = shlex.split(line, comments=True)
        except ValueError:
            continue
        try:
            index = words.index("kompile")
        except ValueError:
            continue
        arguments = words[index + 1 :]
        source_word = next(
            (
                word
                for word in arguments
                if not word.startswith("-") and word.endswith(".k")
            ),
            None,
        )
        if source_word is None:
            continue
        source = (workspace / source_word).resolve()
        try:
            source.relative_to(workspace)
        except ValueError:
            continue
        if not source.is_file() or source.is_symlink():
            continue

        def option(name: str) -> str | None:
            if name not in arguments:
                return None
            option_index = arguments.index(name)
            if option_index + 1 >= len(arguments):
                return None
            return arguments[option_index + 1]

        commands.append(
            KompileCommand(
                source=source,
                main_module=option("--main-module"),
                syntax_module=option("--syntax-module"),
                backend=option("--backend"),
            )
        )
    return tuple(commands)


def _workspace_k_files(workspace: Path) -> tuple[Path, ...]:
    workspace = Path(workspace)
    if not workspace.is_dir() or workspace.is_symlink():
        raise KleanExportError("K definition workspace must be a real directory")
    files = tuple(
        path.resolve()
        for _relative, kind, path in _tree_entries(workspace)
        if kind == "file" and path.suffix == ".k"
    )
    if not files:
        raise KleanExportError("K definition workspace contains no .k files")
    return tuple(sorted(files, key=str))


def _local_required_file(source: Path, required: str, workspace: Path) -> Path | None:
    candidate = Path(required)
    unresolved = (
        candidate
        if candidate.is_absolute()
        else source.parent / candidate
    )
    resolved = unresolved.resolve()
    try:
        resolved.relative_to(workspace)
    except ValueError:
        raise KleanExportError(
            "K definition requires a file outside the frozen workspace: "
            f"{required}"
        )
    if not resolved.exists():
        if resolved.suffix == ".k":
            raise KleanExportError(
                f"K definition requires a missing workspace .k file: {required}"
            )
        return None
    if unresolved.is_symlink() or not resolved.is_file() or resolved.suffix != ".k":
        raise KleanExportError(
            f"K definition require is not a regular workspace .k file: {resolved}"
        )
    return resolved


def resolve_definition_closure(workspace: Path) -> DefinitionResolution:
    original_workspace = Path(workspace)
    try:
        workspace_mode = original_workspace.stat(
            follow_symlinks=False
        ).st_mode
    except OSError as error:
        raise KleanExportError(
            "K definition workspace must be a real directory"
        ) from error
    if not stat.S_ISDIR(workspace_mode):
        raise KleanExportError(
            "K definition workspace must be a real directory"
        )
    workspace = original_workspace.resolve()
    verification_file = workspace / "verification.k"
    if not verification_file.is_file() or verification_file.is_symlink():
        raise KleanExportError(
            "K definition workspace is missing regular verification.k"
        )
    files = _workspace_k_files(workspace)
    # A prove.sh may leave mutation and bridge byproducts (verification-mutant.k,
    # spec-mutant.k, spec-body-mutation.k, ...) in the workspace that reuse the
    # canonical module names SPEC/VERIFICATION.  Record every declaration during
    # the flat scan without failing on a collision; ambiguity is adjudicated
    # below against the files actually reached from the export target, so an
    # unreached duplicate is ignored while a reached duplicate still fails
    # closed.
    module_declarations: dict[str, list[tuple[Path, tuple[str, ...]]]] = {}
    file_modules: dict[Path, tuple[str, ...]] = {}
    file_requires: dict[Path, tuple[Path, ...]] = {}
    for path in files:
        text = path.read_text()
        declared: list[str] = []
        for block in MODULE_BLOCK_RE.finditer(text):
            name = block.group("name")
            imports = tuple(IMPORT_RE.findall(block.group("body")))
            module_declarations.setdefault(name, []).append((path, imports))
            declared.append(name)
        file_modules[path] = tuple(declared)
        file_requires[path] = tuple(
            required_path
            for required in REQUIRES_RE.findall(text)
            if (
                required_path := _local_required_file(
                    path, required, workspace
                )
            )
            is not None
        )

    try:
        verification_module = k_rule_inventory.inventory_verification(
            workspace
        )["verification_module"]
    except k_rule_inventory.KRuleInventoryError as error:
        raise KleanExportError(str(error)) from error
    if verification_module not in file_modules.get(verification_file, ()):
        raise KleanExportError(
            "selected verification module is not defined in verification.k"
        )

    def _requires_reaches(source: Path, target: Path) -> bool:
        """True when ``target`` lies in ``source``'s transitive requires."""

        seen: set[Path] = set()
        stack = [source]
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            if current == target:
                return True
            stack.extend(file_requires.get(current, ()))
        return False

    commands = _proof_kompile_commands(workspace)
    # A kompile command seeds the export closure only when its source is the
    # frozen verification target or transitively requires it.  This keeps a
    # legitimate reverse-require compilation root (a driver that requires
    # verification.k) reachable while excluding mutation and bridge byproducts
    # (verification-mutant.k re-declares VERIFICATION beside the target,
    # bridge-verification.k compiles a parallel definition) that would otherwise
    # pollute the closure with duplicate targets.
    export_commands = tuple(
        command
        for command in commands
        if _requires_reaches(command.source, verification_file)
    )

    def _resolve_module_file(
        name: str,
    ) -> tuple[Path, tuple[str, ...]] | None:
        """Bind ``name`` to the reached file declaring it, failing closed on a
        genuine ambiguity among candidate files."""

        candidates = module_declarations.get(name)
        if not candidates:
            return None
        reached = [
            (path, imports)
            for path, imports in candidates
            if path in reached_files
        ]
        if reached:
            distinct = {path for path, _ in reached}
            if len(distinct) > 1:
                raise KleanExportError(
                    f"duplicate module definition {name}: "
                    + " and ".join(str(path) for path in sorted(distinct, key=str))
                )
            return reached[0]
        if len(candidates) == 1:
            return candidates[0]
        raise KleanExportError(
            f"duplicate module definition {name}: "
            + " and ".join(
                str(path)
                for path in sorted({path for path, _ in candidates}, key=str)
            )
        )

    reached_modules: set[str] = set()
    reached_files: set[Path] = set()
    pending_modules = [verification_module]
    pending_files = [
        verification_file,
        *(command.source for command in export_commands),
    ]
    pending_modules.extend(
        module
        for command in export_commands
        for module in (command.main_module, command.syntax_module)
        if module is not None and module in module_declarations
    )
    while pending_modules or pending_files:
        while pending_files:
            path = pending_files.pop()
            if path in reached_files:
                continue
            reached_files.add(path)
            pending_files.extend(file_requires.get(path, ()))
        if not pending_modules:
            continue
        name = pending_modules.pop()
        if name in reached_modules:
            continue
        reached_modules.add(name)
        resolved = _resolve_module_file(name)
        if resolved is None:
            continue
        path, imports = resolved
        if path not in reached_files:
            pending_files.append(path)
        pending_modules.extend(imports)

    # Fail closed if two files actually reached from the export target declare
    # the same module: the target definition must remain unambiguous even after
    # mutation byproducts have been excluded from the closure.
    for name, candidates in module_declarations.items():
        reached = sorted(
            {path for path, _ in candidates if path in reached_files}, key=str
        )
        if len(reached) > 1:
            raise KleanExportError(
                f"duplicate module definition {name}: "
                + " and ".join(str(path) for path in reached)
            )

    explicit_syntax_modules = [
        command.syntax_module
        for command in export_commands
        if command.syntax_module in reached_modules
    ]
    haskell_syntax_modules = [
        command.syntax_module
        for command in export_commands
        if command.backend == "haskell"
        and command.syntax_module in reached_modules
    ]
    syntax_modules = sorted(
        name
        for name in reached_modules
        if name.endswith("-SYNTAX") and name in module_declarations
    )
    preferred = (
        verification_module.removesuffix("-VERIFICATION") + "-SYNTAX"
    )
    if haskell_syntax_modules:
        syntax_module = haskell_syntax_modules[-1]
    elif explicit_syntax_modules:
        syntax_module = explicit_syntax_modules[-1]
    elif preferred in syntax_modules:
        syntax_module = preferred
    elif len(syntax_modules) == 1:
        syntax_module = syntax_modules[0]
    elif not syntax_modules:
        raise KleanExportError(
            f"no reachable -SYNTAX module for {verification_module}"
        )
    else:
        raise KleanExportError(
            "multiple reachable -SYNTAX modules: "
            + ", ".join(syntax_modules)
        )
    required_by: dict[Path, set[Path]] = {
        path: set() for path in reached_files
    }
    for parent in reached_files:
        for dependency in file_requires.get(parent, ()):
            if dependency in reached_files:
                required_by[dependency].add(parent)
    entry_files = tuple(
        sorted(
            (
                path
                for path in reached_files
                if not required_by[path]
            ),
            key=str,
        )
    )
    if not entry_files:
        entry_files = (verification_file,)
    return DefinitionResolution(
        verification_file=verification_file,
        verification_module=verification_module,
        syntax_module=syntax_module,
        required_files=tuple(sorted(reached_files, key=str)),
        entry_files=entry_files,
    )


def stage_definition_driver(
    scratch: Path,
    workspace: Path,
    resolution: DefinitionResolution,
    transformed_verification: str,
    export_module_text: str,
) -> Path:
    """Mirror the frozen K closure and require each root exactly once."""

    scratch = Path(scratch)
    workspace = Path(workspace).resolve()
    source_root = scratch / "definition-source"
    source_root.mkdir()
    staged: dict[Path, Path] = {}
    for source in resolution.required_files:
        relative = source.relative_to(workspace)
        destination = source_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        staged[source] = destination
    staged_verification = staged.get(resolution.verification_file)
    if staged_verification is None:
        raise KleanExportError("definition closure omitted verification.k")
    staged_verification.write_text(transformed_verification)
    entry_files: list[Path] = []
    for source in resolution.entry_files:
        entry = staged.get(source)
        if entry is None:
            raise KleanExportError("definition entry file is outside closure")
        entry_files.append(entry)
    driver = scratch / "export.k"
    driver.write_text(
        "".join(f'requires "{path}"\n' for path in entry_files)
        + export_module_text
    )
    return driver


def lib_name(package: str) -> str:
    return "".join(word.capitalize() for word in package.split("-"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def lean_trust_declarations(path: Path) -> list[dict[str, str]]:
    """Inventory one-line Lean trust declarations with qualified identities."""

    namespaces: list[str] = []
    declarations: list[dict[str, str]] = []
    for line_number, line in enumerate(Path(path).read_text().splitlines(), 1):
        namespace = _LEAN_NAMESPACE_RE.match(line)
        if namespace is not None:
            namespaces.append(namespace.group(1))
            continue
        ending = _LEAN_END_RE.match(line)
        if ending is not None and namespaces:
            explicit = ending.group(1)
            current = namespaces[-1]
            if explicit is None or explicit == current:
                namespaces.pop()
            continue
        declaration = _LEAN_TRUST_DECL_RE.match(line)
        if declaration is None:
            continue
        kind, name, signature = declaration.groups()
        lean_type = signature.strip()
        if lean_type.startswith(":"):
            lean_type = lean_type[1:].strip()
        qualified_name = ".".join((*namespaces, name))
        declarations.append(
            {
                "name": qualified_name,
                "declaration_name": name,
                "kind": kind,
                "type": lean_type,
                "line": str(line_number),
            }
        )
    return declarations


def parse_verification(text: str) -> tuple[str, list[Func]]:
    modules = MODULE_RE.findall(text)
    verification = next(
        (
            module
            for module in modules
            if module.endswith("VERIFICATION")
            and not module.endswith("-SYNTAX")
        ),
        None,
    )
    if verification is None:
        verification = next(
            (module for module in modules if not module.endswith("-SYNTAX")),
            modules[-1] if modules else "",
        )
    functions: list[Func] = []
    seen: set[str] = set()
    for block in SYNTAX_BLOCK_RE.finditer(text):
        for match in FUNC_PRODUCTION_RE.finditer(block.group("body")):
            if "function" not in match.group("attrs"):
                continue
            name = match.group("name")
            if name in seen:
                continue
            seen.add(name)
            arguments = [
                argument.strip()
                for argument in match.group("args").split(",")
                if argument.strip()
            ]
            functions.append(Func(name, block.group("ret"), arguments))
    return verification, functions


def export_module(verification_module: str, functions: list[Func]) -> str:
    lines = [
        f"module {verification_module.rsplit('-', 1)[0]}-KLEAN-EXPORT",
        f"  imports {verification_module}",
    ]
    for index, function in enumerate(functions):
        tag = f"#kxExport{index}"
        if function.args:
            signature = ' "," '.join(function.args)
            production = f'  syntax KItem ::= "{tag}" "(" {signature} ")"'
            binders = ", ".join(
                f"V{argument}:{sort}"
                for argument, sort in enumerate(function.args)
            )
            call = ", ".join(
                f"V{argument}" for argument in range(len(function.args))
            )
            rule = (
                f"  rule [kxExport{index}]: <k> {tag}({binders}) "
                f"=> {function.name}({call}) ... </k>"
            )
        else:
            production = f'  syntax KItem ::= "{tag}"'
            rule = (
                f"  rule [kxExport{index}]: <k> {tag} "
                f"=> {function.name}() ... </k>"
            )
        lines.extend((production, rule))
    lines.append("endmodule")
    return "\n".join(lines) + "\n"


def promote_referenced_structural_definitions(
    verification_text: str,
    definitions: list[dict[str, Any]],
    domain_lemmas: list[dict[str, Any]],
) -> tuple[str, tuple[str, ...]]:
    """Make selected structural definitions transparent to Klean.

    K rewrites are contextual, but Klean's generated ``Rewrites`` relation
    contains only whole-configuration steps.  A constructor-style helper used
    inside a selected domain lemma would therefore become opaque unless its
    Stage 3 ``DEFINITION`` equations are exported as a K function.
    """

    definitions_by_head: dict[str, list[str]] = {}
    for definition in definitions:
        text = definition.get("text")
        if not isinstance(text, str):
            continue
        match = _RULE_HEAD_RE.search(text)
        if match is None:
            continue
        definitions_by_head.setdefault(match.group("name"), []).append(text)

    referenced = {
        token
        for lemma in domain_lemmas
        if isinstance((text := lemma.get("text")), str)
        for token in re.findall(K_IDENTIFIER, text)
    }
    required = set(definitions_by_head) & referenced
    pending = list(required)
    while pending:
        head = pending.pop()
        dependencies = {
            token
            for text in definitions_by_head[head]
            for token in re.findall(K_IDENTIFIER, text)
        }
        for dependency in dependencies & set(definitions_by_head):
            if dependency not in required:
                required.add(dependency)
                pending.append(dependency)

    existing_functions = {
        function.name for function in parse_verification(verification_text)[1]
    }
    candidates = required - existing_functions
    production_counts: dict[str, int] = {
        name: 0 for name in candidates
    }
    for line in verification_text.splitlines():
        match = _SYNTAX_PRODUCTION_LINE_RE.fullmatch(line)
        if match is not None and match.group("name") in production_counts:
            production_counts[match.group("name")] += 1
    ambiguous = sorted(
        name for name, count in production_counts.items() if count > 1
    )
    if ambiguous:
        raise KleanExportError(
            "referenced structural definitions have multiple function-style "
            "syntax productions: " + ", ".join(ambiguous)
        )
    promote = {
        name for name, count in production_counts.items() if count == 1
    }
    if not promote:
        return verification_text, ()

    observed: dict[str, int] = {name: 0 for name in promote}
    transformed_lines: list[str] = []
    for line in verification_text.splitlines(keepends=True):
        newline = "\n" if line.endswith("\n") else ""
        body = line[:-1] if newline else line
        match = _SYNTAX_PRODUCTION_LINE_RE.fullmatch(body)
        if match is None or match.group("name") not in promote:
            transformed_lines.append(line)
            continue
        name = match.group("name")
        observed[name] += 1
        attrs = match.group("attrs")
        if attrs is None:
            replacement_attrs = "[function, total]"
        else:
            values = [
                value.strip()
                for value in attrs[1:-1].split(",")
                if value.strip()
            ]
            if "constructor" in values:
                raise KleanExportError(
                    f"referenced definition {name} is declared constructor"
                )
            for value in ("function", "total"):
                if value not in values:
                    values.append(value)
            replacement_attrs = "[" + ", ".join(values) + "]"
        transformed_lines.append(
            match.group("prefix")
            + name
            + "("
            + match.group("args")
            + ") "
            + replacement_attrs
            + match.group("suffix")
            + newline
        )

    unresolved = sorted(
        name for name, count in observed.items() if count != 1
    )
    if unresolved:
        raise KleanExportError(
            "referenced structural definitions need exactly one function-style "
            "syntax production: "
            + ", ".join(unresolved)
        )
    return "".join(transformed_lines), tuple(sorted(promote))


def _definition_return_sorts(
    verification_text: str, names: set[str]
) -> dict[str, str]:
    result: dict[str, str] = {}
    production = re.compile(
        rf"(?:\A|^[ \t]*\|)\s*(?P<name>{K_IDENTIFIER})\s*\(",
        re.M,
    )
    for block in SYNTAX_BLOCK_RE.finditer(verification_text):
        for match in production.finditer(block.group("body")):
            name = match.group("name")
            if name not in names:
                continue
            previous = result.setdefault(name, block.group("ret"))
            if previous != block.group("ret"):
                raise KleanExportError(
                    f"referenced definition {name} has multiple return sorts"
                )
    missing = sorted(names - set(result))
    if missing:
        raise KleanExportError(
            "referenced structural definition has no syntax sort: "
            + ", ".join(missing)
        )
    return result


def _call_end(text: str, open_paren: int) -> int:
    depth = 0
    quote = False
    escaped = False
    for index in range(open_paren, len(text)):
        character = text[index]
        if quote:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quote = False
            continue
        if character == '"':
            quote = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return index + 1
    raise KleanExportError("referenced structural definition call is unbalanced")


def lower_structural_calls_in_domain_rule(
    rule_text: str, return_sorts: dict[str, str]
) -> str:
    """Flatten nested transparent calls into variables plus K requires facts."""

    arrow = rule_text.find("=>")
    if arrow < 0:
        raise KleanExportError("domain rule has no rewrite arrow")
    lhs = rule_text[:arrow]
    call_patterns = {
        name: re.compile(
            rf"(?<![A-Za-z0-9_'-]){re.escape(name)}\s*\("
        )
        for name in return_sorts
    }
    calls: list[tuple[int, int, str, str]] = []
    cursor = 0
    while cursor < len(lhs):
        matches = [
            (match.start(), name, match)
            for name, pattern in call_patterns.items()
            if (match := pattern.search(lhs, cursor)) is not None
        ]
        if not matches:
            break
        _start, name, match = min(matches, key=lambda item: item[0])
        open_paren = lhs.find("(", match.start(), match.end())
        end = _call_end(lhs, open_paren)
        variable = f"KleanDef{len(calls)}"
        while variable in rule_text:
            variable += "_"
        calls.append(
            (
                match.start(),
                end,
                f"{variable}:{return_sorts[name]}",
                f"{variable} ==K {lhs[match.start():end]}",
            )
        )
        cursor = end
    if not calls:
        return rule_text
    if re.search(r"\brequires\b", rule_text[arrow + 2 :]):
        raise KleanExportError(
            "selected rule with a structural definition already has requires"
        )
    lowered_lhs = lhs
    for start, end, replacement, _condition in reversed(calls):
        lowered_lhs = lowered_lhs[:start] + replacement + lowered_lhs[end:]
    lowered = lowered_lhs + rule_text[arrow:]
    condition = " andBool ".join(
        f"({item[3]})" if len(calls) > 1 else item[3]
        for item in calls
    )
    attributes = re.search(
        r"(?s)(?P<body>.*?)(?P<spacing>[ \t\r\n]*)"
        r"(?P<attrs>\[[^\[\]]*\])[ \t\r\n]*\Z",
        lowered,
    )
    if attributes is None:
        return lowered + " requires " + condition
    return (
        attributes.group("body")
        + " requires "
        + condition
        + attributes.group("spacing")
        + attributes.group("attrs")
    )


def lower_referenced_structural_definitions(
    verification_text: str,
    domain_lemmas: list[dict[str, Any]],
    promoted: tuple[str, ...],
) -> tuple[str, tuple[str, ...]]:
    if not promoted:
        return verification_text, ()
    promoted_set = set(promoted)
    return_sorts = _definition_return_sorts(
        verification_text, promoted_set
    )
    lowered_ids: list[str] = []
    transformed = verification_text
    for rule in domain_lemmas:
        text = rule.get("text")
        source_rule_id = rule.get("source_rule_id")
        if not isinstance(text, str) or not isinstance(source_rule_id, str):
            raise KleanExportError("validated domain rule is malformed")
        referenced = set(re.findall(K_IDENTIFIER, text)) & promoted_set
        if not referenced:
            continue
        lowered = lower_structural_calls_in_domain_rule(
            text,
            {name: return_sorts[name] for name in referenced},
        )
        if transformed.count(text) != 1:
            raise KleanExportError(
                "validated domain rule is not unique in verification source"
            )
        transformed = transformed.replace(text, lowered, 1)
        lowered_ids.append(source_rule_id)
    return transformed, tuple(lowered_ids)


def absolutize_requires(text: str, base: Path) -> str:
    def replace(match: re.Match[str]) -> str:
        path = Path(match.group(1))
        if path.is_absolute():
            return match.group(0)
        resolved = (base / path).resolve()
        if resolved.exists():
            return f'requires "{resolved}"'
        return match.group(0)

    return REQUIRES_RE.sub(replace, text)


def termination_failures(build_output: str) -> set[str]:
    flagged = set(_TERM_HEAD_RE.findall(build_output))
    for source, target in _TERM_CALL_RE.findall(build_output):
        flagged.update((source, target))
    return {name for name in flagged if name and name != "at"}


def elaboration_failures(
    function_text: str, build_output: str
) -> set[str]:
    """Map narrowly recognized generated Func.lean errors to their definitions."""

    lines = function_text.splitlines()
    flagged: set[str] = set()
    for match in _ELAB_LINE_RE.finditer(build_output):
        line_number = int(match.group(1))
        if not 1 <= line_number <= len(lines):
            continue
        for line in reversed(lines[:line_number]):
            definition = _DEF_RE.match(line)
            if definition is not None:
                flagged.add(definition.group(2))
                break
    return flagged


def _defname_re(flagged: set[str]) -> re.Pattern[str]:
    return re.compile(
        r"^\s*(?:noncomputable )?def ("
        + "|".join(re.escape(name) for name in flagged)
        + r")\b"
    )


def _def_to_axiom(lines: list[str]) -> str:
    head = lines[0]
    match = _DEF_RE.match(head)
    if match is None:
        raise KleanExportError(f"cannot axiomatize malformed definition: {head}")
    if " := " in head:
        signature = head.split(" := ", 1)[0].strip()
    else:
        signature = head.strip()
    signature = re.sub(r"^(?:noncomputable\s+)?def\s+", "", signature)
    return f"axiom {signature}"


def _axiomatize_group(inner: list[str]) -> list[str]:
    output: list[str] = []
    index = 0
    while index < len(inner):
        if _DEF_RE.match(inner[index]):
            end = index + 1
            while end < len(inner) and not _DEF_RE.match(inner[end]):
                end += 1
            output.append(_def_to_axiom(inner[index:end]))
            index = end
        else:
            index += 1
    return output


def axiomatize(function_text: str, flagged: set[str]) -> str:
    if not flagged:
        return function_text
    hit = _defname_re(flagged)
    lines = function_text.split("\n")
    output: list[str] = []
    index = 0
    while index < len(lines):
        if lines[index].strip() == "mutual":
            end = index
            while end < len(lines) and lines[end].strip() != "end":
                end += 1
            block = lines[index : end + 1]
            if any(hit.match(line) for line in block):
                output.extend(_axiomatize_group(block[1:-1]))
            else:
                output.extend(block)
            index = end + 1
        elif _DEF_RE.match(lines[index]) and hit.match(lines[index]):
            end = index + 1
            while (
                end < len(lines)
                and not _DEF_RE.match(lines[end])
                and lines[end].strip() != "mutual"
            ):
                end += 1
            output.append(_def_to_axiom(lines[index:end]))
            index = end
        else:
            output.append(lines[index])
            index += 1
    return "\n".join(output)


_COLLECTION_HOOK_MODELS = {
    "axiom «.List» : Option SortList": (
        "noncomputable def «.List» : Option SortList := some ⟨[]⟩"
    ),
    "axiom «.Map» : Option SortMap": (
        "noncomputable def «.Map» : Option SortMap := some ⟨[]⟩"
    ),
    "axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList": (
        "noncomputable def _List_ (x0 : SortList) (x1 : SortList) "
        ": Option SortList := some ⟨x0.coll ++ x1.coll⟩"
    ),
    "axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap": (
        "noncomputable def _Map_ (x0 : SortMap) (x1 : SortMap) "
        ": Option SortMap :=\n"
        "  if kleanMapDisjointModel x0.coll x1.coll then\n"
        "    some ⟨x0.coll.foldr\n"
        "      (fun kv acc => kleanMapInsertModel kv.1 kv.2 acc)\n"
        "      x1.coll⟩\n"
        "  else none"
    ),
    (
        "axiom «_in_keys(_)_MAP_Bool_KItem_Map» "
        "(x0 : SortKItem) (x1 : SortMap) : Option SortBool"
    ): (
        "noncomputable def «_in_keys(_)_MAP_Bool_KItem_Map» "
        "(x0 : SortKItem) (x1 : SortMap) : Option SortBool :=\n"
        "  some (kleanMapContainsModel x1.coll x0)"
    ),
    (
        "axiom «_[_<-undef]» (x0 : SortMap) (x1 : SortKItem) "
        ": Option SortMap"
    ): (
        "noncomputable def «_[_<-undef]» "
        "(x0 : SortMap) (x1 : SortKItem) : Option SortMap :=\n"
        "  some ⟨kleanMapDeleteModel x0.coll x1⟩"
    ),
    (
        "axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) "
        ": Option SortMap"
    ): (
        "noncomputable def «_|->_» "
        "(x0 : SortKItem) (x1 : SortKItem) : Option SortMap :=\n"
        "  some ⟨[(x0, x1)]⟩"
    ),
    "axiom ListItem (x0 : SortKItem) : Option SortList": (
        "noncomputable def ListItem (x0 : SortKItem) : Option SortList :=\n"
        "  some ⟨[x0]⟩"
    ),
    (
        "axiom «Map:lookup» (x0 : SortMap) (x1 : SortKItem) "
        ": Option SortKItem"
    ): (
        "noncomputable def «Map:lookup» "
        "(x0 : SortMap) (x1 : SortKItem) : Option SortKItem :=\n"
        "  kleanMapLookupModel x0.coll x1"
    ),
    (
        "axiom «Map:update» (x0 : SortMap) (x1 : SortKItem) "
        "(x2 : SortKItem) : Option SortMap"
    ): (
        "noncomputable def «Map:update» "
        "(x0 : SortMap) (x1 : SortKItem) (x2 : SortKItem) "
        ": Option SortMap :=\n"
        "  some ⟨kleanMapUpdateModel x0.coll x1 x2⟩"
    ),
}

_COLLECTION_HOOK_HELPERS = """noncomputable local instance : DecidableEq SortKItem :=
  Classical.typeDecidableEq SortKItem

private noncomputable def kleanMapLookupModel
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : Option SortKItem :=
  match entries with
  | [] => none
  | (candidate, value) :: rest =>
      if candidate = key then some value
      else kleanMapLookupModel rest key

private noncomputable def kleanMapContainsModel
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : Bool :=
  match entries with
  | [] => false
  | (candidate, _) :: rest =>
      if candidate = key then true
      else kleanMapContainsModel rest key

private noncomputable def kleanMapDisjointModel
    (left right : List (SortKItem × SortKItem)) : Bool :=
  match right with
  | [] => true
  | (key, _) :: rest =>
      if kleanMapContainsModel left key then false
      else kleanMapDisjointModel left rest

private noncomputable def kleanMapDeleteModel
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : List (SortKItem × SortKItem) :=
  match entries with
  | [] => []
  | (candidate, value) :: rest =>
      if candidate = key then kleanMapDeleteModel rest key
      else (candidate, value) :: kleanMapDeleteModel rest key

private noncomputable def kleanKeyOrderModel : SortKItem → SortKItem → Bool
  | SortKItem.inj_SortInt a,    SortKItem.inj_SortInt b    => decide (a < b)
  | SortKItem.inj_SortInt _,    _                          => true
  | _,                          SortKItem.inj_SortInt _    => false
  | SortKItem.inj_SortString a, SortKItem.inj_SortString b => decide (a < b)
  | SortKItem.inj_SortString _, _                          => true
  | _,                          SortKItem.inj_SortString _ => false
  | _, _ => false

private noncomputable def kleanMapInsertModel
    (key value : SortKItem) :
    List (SortKItem × SortKItem) → List (SortKItem × SortKItem)
  | [] => [(key, value)]
  | (candidate, oldValue) :: rest =>
      if kleanKeyOrderModel candidate key then
        (candidate, oldValue) :: kleanMapInsertModel key value rest
      else (key, value) :: (candidate, oldValue) :: rest

private noncomputable def kleanMapUpdateModel
    (entries : List (SortKItem × SortKItem))
    (key value : SortKItem) : List (SortKItem × SortKItem) :=
  kleanMapInsertModel key value (kleanMapDeleteModel entries key)
"""


# The pyk exporter emits an axiom only for the collection hooks a definition
# actually references, so a registered hook being absent is normal rather than a
# defect: any subset of the registry may appear.  Every registered hook
# signature that is present is modeled by exact-match replacement; absent
# registrations are simply skipped.  Completeness is deliberately NOT required.
# The real safety net is ``_assert_no_unmodeled_hook_axioms`` below, which fails
# closed on any hook-bearing axiom that survives modeling.

# Canonical order of the modeled-hook identities recorded in the manifests.
_COLLECTION_HOOK_NAME_ORDER = (
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
)


def _hook_axiom_symbol(signature: str) -> str:
    """Recover the K symbol a hook ``axiom`` declaration names.

    Accepts either a bare registered signature or a full ``axiom`` line taken
    from generated Lean text, tolerating leading whitespace.
    """

    body = signature.strip()
    if body.startswith("axiom "):
        body = body[len("axiom ") :].lstrip()
    if body.startswith("«"):
        end = body.find("»")
        return body[1:end] if end != -1 else body[1:]
    return body.split(None, 1)[0] if body else ""


def model_collection_hooks(
    function_text: str,
) -> tuple[str, tuple[str, ...]]:
    """Replace Klean's unconstrained List/Map hook axioms with K models.

    The pyk exporter emits an axiom only for the collection hooks a definition
    references, so any subset of the registry may appear.  Every registered
    hook signature that is present is replaced by its Lean model; absent
    registrations are skipped.  Completeness is not required here — the
    ``_assert_no_unmodeled_hook_axioms`` net is the fail-closed guard against a
    hook-bearing axiom we leave behind.
    """

    signature_of = {
        _hook_axiom_symbol(signature): signature
        for signature in _COLLECTION_HOOK_MODELS
    }
    if set(_COLLECTION_HOOK_NAME_ORDER) != set(signature_of):
        raise KleanExportError("collection-hook registry is inconsistent")

    present = [
        signature_of[name]
        for name in _COLLECTION_HOOK_NAME_ORDER
        if signature_of[name] in function_text
    ]
    if not present:
        return function_text, ()

    for signature in present:
        if function_text.count(signature) != 1:
            raise KleanExportError(
                f"generated collection hook is not unique: {signature}"
            )
    first = min(present, key=function_text.index)
    repaired = function_text.replace(
        first,
        _COLLECTION_HOOK_HELPERS.rstrip()
        + "\n\n"
        + _COLLECTION_HOOK_MODELS[first],
        1,
    )
    for signature in present:
        if signature == first:
            continue
        repaired = repaired.replace(
            signature, _COLLECTION_HOOK_MODELS[signature], 1
        )

    present_set = set(present)
    names = tuple(
        name
        for name in _COLLECTION_HOOK_NAME_ORDER
        if signature_of[name] in present_set
    )
    return repaired, names


_CORE_OPERATIONAL_HOOK_MODELS = {
    (
        "axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) "
        ": Option SortInt"
    ): (
        "noncomputable def «_%Int_» "
        "(x0 : SortInt) (x1 : SortInt) : Option SortInt :=\n"
        "  if x1 = 0 then none else some (Int.tmod x0 x1)"
    ),
    "axiom append (x0 : SortK) (x1 : SortK) : Option SortK": (
        "noncomputable def append : SortK → SortK → Option SortK\n"
        "  | SortK.dotk, rest => some rest\n"
        "  | SortK.kseq item tail, rest => do\n"
        "      let modeledRest ← append tail rest\n"
        "      return SortK.kseq item modeledRest"
    ),
    (
        "axiom «strToCodes(_)_MPY-STR_IntSeq_String» "
        "(x0 : SortString) : Option SortIntSeq"
    ): (
        "noncomputable def «strToCodes(_)_MPY-STR_IntSeq_String» "
        "(x0 : SortString) : Option SortIntSeq :=\n"
        "  some (x0.data.foldr\n"
        "    (fun character codes =>\n"
        "      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»\n"
        "        (Int.ofNat character.toNat) codes)\n"
        "    SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)"
    ),
    (
        "axiom «_==K_» (x0 : SortK) (x1 : SortK) "
        ": Option SortBool"
    ): (
        "noncomputable local instance : DecidableEq SortK :=\n"
        "  Classical.typeDecidableEq SortK\n"
        "noncomputable def «_==K_» "
        "(x0 : SortK) (x1 : SortK) : Option SortBool :=\n"
        "  some (decide (x0 = x1))"
    ),
}


# Canonical order of the modeled operational-hook identities in the manifests.
_CORE_OPERATIONAL_HOOK_NAME_ORDER = (
    "_%Int_",
    "strToCodes(_)_MPY-STR_IntSeq_String",
    "append",
    "_==K_",
)


def model_core_operational_hooks(
    function_text: str,
) -> tuple[str, tuple[str, ...]]:
    """Replace exact K integer remainder and K-sequence append axioms.

    pyk emits an axiom only for the operational hooks a definition references,
    so either hook may appear alone.  Every registered operational hook that is
    present is replaced by its exact model; absent registrations are skipped.
    Completeness is not required — the ``_assert_no_unmodeled_hook_axioms`` net
    fails closed on any operational hook we leave unmodeled.
    """

    signature_of = {
        _hook_axiom_symbol(signature): signature
        for signature in _CORE_OPERATIONAL_HOOK_MODELS
    }
    if set(_CORE_OPERATIONAL_HOOK_NAME_ORDER) != set(signature_of):
        raise KleanExportError(
            "core operational-hook registry is inconsistent"
        )

    present = [
        signature_of[name]
        for name in _CORE_OPERATIONAL_HOOK_NAME_ORDER
        if signature_of[name] in function_text
    ]
    if not present:
        return function_text, ()

    repaired = function_text
    for signature in present:
        if repaired.count(signature) != 1:
            raise KleanExportError(
                f"generated core operational hook is not unique: {signature}"
            )
        repaired = repaired.replace(
            signature, _CORE_OPERATIONAL_HOOK_MODELS[signature], 1
        )

    present_set = set(present)
    names = tuple(
        name
        for name in _CORE_OPERATIONAL_HOOK_NAME_ORDER
        if signature_of[name] in present_set
    )
    return repaired, names


_HOOK_BEARING_SORT_RE = re.compile(r"\bSort(?:Map|List|Set|K)\b")


def _registered_hook_symbols() -> frozenset[str]:
    """Every hook symbol carried by the collection and operational registries."""

    return frozenset(
        _hook_axiom_symbol(signature)
        for signature in (
            *_COLLECTION_HOOK_MODELS,
            *_CORE_OPERATIONAL_HOOK_MODELS,
        )
    )


def _looks_like_hook_symbol(symbol: str) -> bool:
    """Recognize K builtin hook symbols by their structural naming patterns.

    Covers unregistered/new hooks so the net still fails closed on a collection
    or K-sequence builtin we do not yet model.
    """

    return (
        ":" in symbol  # «Map:lookup», «Map:update», «Set:in», «List:range» ...
        or "_in_keys" in symbol
        or symbol == "append"
        or symbol.startswith("_[")  # «_[_<-undef]», «_[_]» element access ...
        or "|->" in symbol  # «_|->_» map entry
        or "%Int" in symbol  # «_%Int_» integer remainder
    )


def _unmodeled_hook_axioms(function_text: str) -> list[str]:
    """List every hook-bearing ``axiom`` line that survived hook modeling.

    An axiom is treated as an unmodeled hook when its declaration mentions a
    hook-bearing sort (SortMap/SortList/SortSet or a bare SortK arrow form), or
    its symbol is registered, or its symbol matches a known hook naming
    pattern.  Every currently registered hook is therefore caught if left
    behind, and genuine non-hook axioms (which never mention these sorts and
    only appear later, from build-repair axiomatization) are not flagged.
    """

    registered = _registered_hook_symbols()
    flagged: list[str] = []
    for line in function_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("axiom "):
            continue
        symbol = _hook_axiom_symbol(stripped)
        if (
            _HOOK_BEARING_SORT_RE.search(stripped)
            or symbol in registered
            or _looks_like_hook_symbol(symbol)
        ):
            flagged.append(stripped)
    return flagged


def _assert_no_unmodeled_hook_axioms(function_text: str) -> None:
    """Fail closed if any hook-bearing axiom remains after modeling."""

    remaining = _unmodeled_hook_axioms(function_text)
    if remaining:
        raise KleanExportError(
            "unmodeled hook axiom remains: " + "; ".join(remaining)
        )


_BUILD_IS_HELPER_AXIOM = (
    "axiom _5bd0f09 : SortIntSeq → SortInt → SortInt → SortInt → "
    "Option SortIntSeq"
)
_BUILD_IS_PUBLIC_AXIOM = (
    "axiom «buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int» "
    "(x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) "
    ": Option SortIntSeq"
)
_BUILD_IS_MODEL = """private def kleanIntSeqLengthModel : SortIntSeq → Nat
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => 0
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest =>
      kleanIntSeqLengthModel rest + 1

private def kleanIntSeqAtNatModel : SortIntSeq → Nat → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» value _, 0 =>
      some value
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest, index + 1 =>
      kleanIntSeqAtNatModel rest index
  | _, _ => none

private def kleanIntSeqAtModel
    (input : SortIntSeq) (index : SortInt) : Option SortInt :=
  if index < 0 then none else kleanIntSeqAtNatModel input index.toNat

private def kleanBuildISContinueModel
    (index stop step : SortInt) : Bool :=
  (step > 0 && index < stop) || (step < 0 && index > stop)

private def kleanBuildISFuelModel :
    Nat → SortIntSeq → SortInt → SortInt → SortInt → Option SortIntSeq
  | 0, _, index, stop, step =>
      if kleanBuildISContinueModel index stop step then none
      else some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | fuel + 1, input, index, stop, step =>
      if kleanBuildISContinueModel index stop step then
        match kleanIntSeqAtModel input index with
        | none => none
        | some value =>
            match kleanBuildISFuelModel fuel input (index + step) stop step with
            | none => none
            | some rest =>
                some (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
                  value rest)
      else some SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

private def kleanBuildISModel
    (x0 : SortIntSeq) (x1 x2 x3 : SortInt) : Option SortIntSeq :=
  kleanBuildISFuelModel (kleanIntSeqLengthModel x0 + 1) x0 x1 x2 x3

noncomputable def _5bd0f09 :
    SortIntSeq → SortInt → SortInt → SortInt → Option SortIntSeq :=
  kleanBuildISModel
"""
_BUILD_IS_PUBLIC_MODEL = """noncomputable def «buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int»
    (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) :
    Option SortIntSeq :=
  kleanBuildISModel x0 x1 x2 x3"""
_BUILD_IS_MUTUAL_DEFS = re.compile(
    r"(?ms)^mutual\n"
    r"  (?:noncomputable )?def _5bd0f09 : SortIntSeq → SortInt → "
    r"SortInt → SortInt → Option SortIntSeq\n"
    r".*?"
    r"^  (?:noncomputable )?def "
    r"«buildIS\(_,_,_,_\)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int» "
    r"\(x0 : SortIntSeq\) \(x1 : SortInt\) \(x2 : SortInt\) "
    r"\(x3 : SortInt\) : Option SortIntSeq := .*?\n"
    r"end(?:\n|$)"
)


def model_recursive_build_is(
    function_text: str,
) -> tuple[str, tuple[str, ...]]:
    """Model the exact recursive IntSeq slicing rules with structural fuel."""

    helper_count = function_text.count(_BUILD_IS_HELPER_AXIOM)
    public_count = function_text.count(_BUILD_IS_PUBLIC_AXIOM)
    mutual_defs = list(_BUILD_IS_MUTUAL_DEFS.finditer(function_text))
    if helper_count == 0 and public_count == 0 and not mutual_defs:
        return function_text, ()
    if helper_count or public_count:
        if helper_count != 1 or public_count != 1 or mutual_defs:
            raise KleanExportError(
                "generated buildIS definition pair is incomplete or non-unique"
            )
        repaired = function_text.replace(
            _BUILD_IS_HELPER_AXIOM, _BUILD_IS_MODEL.rstrip(), 1
        )
        repaired = repaired.replace(
            _BUILD_IS_PUBLIC_AXIOM, _BUILD_IS_PUBLIC_MODEL.rstrip(), 1
        )
    elif len(mutual_defs) == 1:
        replacement = _BUILD_IS_MODEL.rstrip() + "\n\n" + _BUILD_IS_PUBLIC_MODEL
        repaired = _BUILD_IS_MUTUAL_DEFS.sub(replacement + "\n", function_text)
    else:
        raise KleanExportError(
            "generated buildIS mutual definition pair is incomplete or non-unique"
        )
    return repaired, (
        "_5bd0f09",
        "buildIS(_,_,_,_)_MPY-SUBSCRIPT_IntSeq_IntSeq_Int_Int_Int",
    )


def needs_noncomputable(build_output: str) -> bool:
    return (
        "consider marking definition as 'noncomputable'" in build_output
        or "not supported by code generator" in build_output
        or "has no executable code" in build_output
    )


def mark_all_noncomputable(function_text: str) -> str:
    return re.sub(
        r"(?m)^(\s*)def ", r"\1noncomputable def ", function_text
    )


def _patch_lake_build_directory(package: Path) -> None:
    lakefile = package / "lakefile.toml"
    if not lakefile.is_file() or lakefile.is_symlink():
        raise KleanExportError("generated package is missing regular lakefile.toml")
    text = lakefile.read_text()
    build_setting = 'buildDir = "/tmp/klean-generated-build"\n'
    stack_setting = (
        'moreLeanArgs = ["-D maxRecDepth=100000", "-s", "65536"]\n'
    )
    if build_setting in text and stack_setting in text:
        return
    setting = ""
    if build_setting not in text:
        setting += build_setting
    if stack_setting not in text:
        setting += stack_setting
    marker = "[[lean_lib]]"
    if marker in text:
        text = text.replace(marker, setting + "\n" + marker, 1)
    else:
        text = text.rstrip() + "\n" + setting
    lakefile.write_text(text)


def _tree_entries(root: Path) -> list[tuple[str, str, Path]]:
    if not root.is_dir() or root.is_symlink():
        raise KleanExportError(f"tree root must be a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise KleanExportError(
                    f"tree contains linked or unsupported entry: {path}"
                )
    return sorted(entries)


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in _tree_entries(Path(root)):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


def _regular_json(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise KleanExportError(f"required JSON is not a regular file: {path}")
    try:
        document = json.loads(path.read_text())
    except (OSError, ValueError) as error:
        raise KleanExportError(f"malformed JSON: {path}") from error
    if not isinstance(document, dict):
        raise KleanExportError(f"JSON must be an object: {path}")
    return document


def _run_command(
    command: list[str] | str,
    *,
    cwd: Path | None,
    timeout: int,
    env: dict[str, str],
    shell: bool = False,
) -> tuple[int, str]:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            timeout=timeout,
            shell=shell,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        return result.returncode, result.stdout
    except subprocess.TimeoutExpired:
        return 124, f"TIMEOUT after {timeout}s"


def _trust_inventory(
    package: Path,
    *,
    axiomatized: set[str],
    noncomputable_repair: bool,
    modeled_collection_hooks: tuple[str, ...] = (),
    modeled_operational_hooks: tuple[str, ...] = (),
    modeled_recursive_functions: tuple[str, ...] = (),
) -> dict[str, Any]:
    axioms: set[str] = set()
    allowlist: dict[str, dict[str, str]] = {}
    noncomputable: set[str] = set()
    designated_sorries = 0
    other_sorries = 0
    for _relative, kind, path in _tree_entries(package):
        if kind != "file" or path.suffix != ".lean":
            continue
        text = path.read_text()
        for declaration in lean_trust_declarations(path):
            name = declaration["name"]
            declaration_name = declaration["declaration_name"]
            kind = declaration["kind"]
            if kind == "axiom":
                axioms.add(name)
            allowlist[name] = {
                "name": name,
                "declaration_name": declaration_name,
                "kind": kind,
                "type": declaration["type"],
                "source": path.relative_to(package).as_posix(),
                "line": declaration["line"],
                "reason": (
                    "deterministic Klean definition repair"
                    if declaration_name in axiomatized
                    else (
                        "Klean-generated opaque definition"
                        if kind == "opaque"
                        else "Klean-generated trust boundary"
                    )
                ),
            }
        noncomputable.update(_NONCOMPUTABLE_RE.findall(text))
        count = len(re.findall(r"\bsorry\b", text))
        if path.name == "Lemmas.lean":
            designated_sorries += count
        else:
            other_sorries += count
    return {
        "axioms": sorted(axioms),
        "automatic_axiomatization": sorted(axiomatized),
        "modeled_collection_hooks": list(modeled_collection_hooks),
        "modeled_operational_hooks": list(modeled_operational_hooks),
        "modeled_recursive_functions": list(modeled_recursive_functions),
        "noncomputable_definitions": sorted(noncomputable),
        "automatic_noncomputable_repair": noncomputable_repair,
        "designated_sorries": designated_sorries,
        "other_sorries": other_sorries,
        "allowlist": [allowlist[name] for name in sorted(allowlist)],
    }


def target_statement(generated: Path) -> dict[str, Any] | None:
    obligation_map = _regular_json(generated / "obligation-map.json")
    obligations = obligation_map.get("obligations")
    parameters = obligation_map.get("trust_parameters")
    if not isinstance(obligations, list) or not isinstance(parameters, list):
        raise KleanExportError("generated obligation map is malformed")
    candidates: list[tuple[Path, str]] = []
    raw_count = 0
    for relative, kind, path in _tree_entries(generated):
        if kind != "file" or path.suffix != ".lean":
            continue
        text = path.read_text()
        raw_count += len(
            re.findall(r"(?m)^\s*def\s+targetStatement\b", text)
        )
        for match in re.finditer(
            r"(?ms)^\s*def\s+targetStatement\b.*?"
            r"(?=^\s*end\s+\S+\s*$)",
            text,
        ):
            candidates.append((path, match.group(0).strip()))
    if not obligations:
        if raw_count != 0:
            raise KleanExportError(
                "zero obligations must not generate a target proposition"
            )
        return None
    if raw_count != 1 or len(candidates) != 1:
        raise KleanExportError(
            "generated project must contain exactly one target proposition; "
            f"found {raw_count}"
        )
    path, definition = candidates[0]
    names: list[str] = []
    normalized_parameters: list[dict[str, Any]] = []
    for parameter in parameters:
        if not isinstance(parameter, dict):
            raise KleanExportError("target parameter is malformed")
        name = parameter.get("name")
        lean_type = parameter.get("type")
        kore_symbol = parameter.get("kore_symbol")
        source_rule_ids = parameter.get("source_rule_ids")
        binding_sha256 = parameter.get("binding_sha256")
        if not isinstance(name, str) or not name:
            raise KleanExportError("target parameter name is malformed")
        if not isinstance(lean_type, str) or not lean_type:
            raise KleanExportError("target parameter type is malformed")
        if not isinstance(kore_symbol, str) or not kore_symbol:
            raise KleanExportError("target KORE symbol binding is malformed")
        if (
            not isinstance(source_rule_ids, list)
            or not source_rule_ids
            or not all(
                isinstance(source_rule_id, str) and source_rule_id
                for source_rule_id in source_rule_ids
            )
        ):
            raise KleanExportError("target source-rule binding is malformed")
        binding = {
            "kore_symbol": kore_symbol,
            "name": name,
            "type": lean_type,
            "source_rule_ids": source_rule_ids,
        }
        expected_binding_sha256 = sha256_text(
            json.dumps(binding, sort_keys=True, separators=(",", ":"))
        )
        if binding_sha256 != expected_binding_sha256:
            raise KleanExportError("target parameter binding hash changed")
        names.append(name)
        normalized_parameters.append(
            {**binding, "binding_sha256": binding_sha256}
        )
    declaration = f"{path.parent.name}.Lemmas.targetStatement"
    statement = " ".join((declaration, *names))
    return {
        "declaration": declaration,
        "file": path.relative_to(generated).as_posix(),
        "statement": statement,
        "statement_sha256": sha256_text(statement),
        "definition_sha256": sha256_text(definition),
        "parameters": normalized_parameters,
    }


def expected_target_definition(obligation_map: dict[str, Any]) -> str | None:
    obligations = obligation_map.get("obligations")
    parameters = obligation_map.get("trust_parameters")
    if not isinstance(obligations, list) or not isinstance(parameters, list):
        raise KleanExportError("generated obligation map is malformed")
    if not obligations:
        return None
    lines = ["def targetStatement"]
    for parameter in parameters:
        if not isinstance(parameter, dict):
            raise KleanExportError("target parameter is malformed")
        name = parameter.get("name")
        lean_type = parameter.get("type")
        if not isinstance(name, str) or not isinstance(lean_type, str):
            raise KleanExportError("target parameter is malformed")
        lines.append(f"    ({name} : {lean_type})")
    conjuncts: list[str] = []
    for obligation in obligations:
        if not isinstance(obligation, dict):
            raise KleanExportError("generated obligation is malformed")
        conjunct = obligation.get("lean_conjunct")
        if not isinstance(conjunct, str) or not conjunct:
            raise KleanExportError("generated Lean conjunct is malformed")
        conjuncts.append(f"({conjunct})")
    lines.extend(("    : Prop :=", "    " + "\n    ∧ ".join(conjuncts)))
    return "\n".join(lines)


def _write_json(path: Path, document: dict[str, Any]) -> None:
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")


def _domain_source_rules(
    validated: dict[str, Any],
    discovery_manifest_sha256: str,
) -> list[dict[str, Any]]:
    inventory_sha256 = validated["inventory_sha256"]
    return [
        {
            **rule,
            "inventory_sha256": inventory_sha256,
            "discovery_manifest_sha256": discovery_manifest_sha256,
        }
        for rule in validated["domain_lemmas"]
    ]


def _klean_source_rules(
    domain_rules: list[dict[str, Any]],
    line_offset: int,
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for rule in domain_rules:
        entry: dict[str, Any] = {
            "source_rule_id": rule["source_rule_id"],
            "start_line": rule["start_line"] + line_offset,
            "end_line": rule["end_line"] + line_offset,
            "normalized_sha256": rule["normalized_sha256"],
            "classification": "TRUST_OBLIGATION",
        }
        if "file" in rule:
            entry["file"] = rule["file"]
        entries.append(entry)
    return entries


def _bind_obligation_provenance(
    package: Path,
    domain_rules: list[dict[str, Any]],
    klean_rules: list[dict[str, Any]],
) -> dict[str, Any]:
    path = package / "obligation-map.json"
    document = _regular_json(path)
    obligations = document.get("obligations")
    parameters = document.get("trust_parameters")
    if not isinstance(obligations, list) or not isinstance(parameters, list):
        raise KleanExportError("generated obligation map is malformed")
    expected_ids = [rule["source_rule_id"] for rule in domain_rules]
    observed_ids = [
        obligation.get("source_rule_id")
        if isinstance(obligation, dict)
        else None
        for obligation in obligations
    ]
    if observed_ids != expected_ids:
        raise KleanExportError(
            "validated DOMAIN_LEMMA records and generated obligations "
            "are not bijective"
        )
    enriched: list[dict[str, Any]] = []
    for obligation, rule, klean_rule in zip(
        obligations, domain_rules, klean_rules, strict=True
    ):
        if obligation.get("source_span") != {
            "start_line": klean_rule["start_line"],
            "end_line": klean_rule["end_line"],
        }:
            raise KleanExportError(
                "generated obligation source span differs from Stage 1"
            )
        enriched.append(
            {
                **obligation,
                "source_span": {
                    "start_line": rule["start_line"],
                    "end_line": rule["end_line"],
                },
                "normalized_sha256": rule["normalized_sha256"],
                "inventory_sha256": rule["inventory_sha256"],
                "discovery_manifest_sha256": rule[
                    "discovery_manifest_sha256"
                ],
            }
        )
    document = {
        **document,
        "schema_version": 3,
        "source_rules": domain_rules,
        "obligations": enriched,
    }
    _write_json(path, document)
    return document


def export_frozen(
    frozen_input: Path,
    discovery_manifest: Path,
    output: Path,
    *,
    run_command: Callable[..., tuple[int, str]] = _run_command,
    problem: str | None = None,
    toolchain_lock: Path | None = None,
    generator_image_id: str | None = None,
) -> dict[str, Any]:
    frozen_input = Path(frozen_input)
    discovery_manifest = Path(discovery_manifest)
    destination = Path(output)
    problem = problem or os.environ.get("PROBLEM_ID") or destination.name
    toolchain_lock = (
        REPO / "data/klean-toolchain.lock.json"
        if toolchain_lock is None
        else Path(toolchain_lock)
    )
    if re.fullmatch(r"[A-Za-z0-9_-]+", problem) is None:
        raise KleanExportError("problem ID is malformed")
    if not frozen_input.is_dir() or frozen_input.is_symlink():
        raise KleanExportError("frozen input must be a real directory")
    before_hash = tree_digest(frozen_input)
    if not discovery_manifest.is_file() or discovery_manifest.is_symlink():
        raise KleanExportError(
            "validated Stage 3 discovery manifest must be a regular file"
        )
    discovery_bytes = discovery_manifest.read_bytes()
    try:
        validated = lemma_discovery_contract.validate_trust_boundary(
            frozen_input, discovery_manifest
        )
    except lemma_discovery_contract.LemmaDiscoveryContractError as error:
        raise KleanExportError(str(error)) from error
    if discovery_manifest.read_bytes() != discovery_bytes:
        raise KleanExportError(
            "validated Stage 3 discovery manifest changed during validation"
        )
    if tree_digest(frozen_input) != before_hash:
        raise KleanExportError(
            "frozen input changed during discovery validation"
        )
    discovery_manifest_sha256 = hashlib.sha256(discovery_bytes).hexdigest()
    if destination.exists() or destination.is_symlink():
        raise KleanExportError(f"destination already exists: {destination}")
    if not destination.parent.is_dir() or destination.parent.is_symlink():
        raise KleanExportError("destination parent must be a real directory")
    verification = frozen_input / "verification.k"
    if not verification.is_file() or verification.is_symlink():
        raise KleanExportError("frozen input is missing regular verification.k")
    lock = _regular_json(toolchain_lock)
    for key in (
        "runtimeverification_k_commit",
        "pyk_project",
        "lean_toolchain",
    ):
        if not isinstance(lock.get(key), str) or not lock[key]:
            raise KleanExportError(f"toolchain lock is missing {key}")
    verification_text = verification.read_text()
    canonical_inventory = validated
    resolution = resolve_definition_closure(frozen_input)
    module = resolution.verification_module
    if module != canonical_inventory["verification_module"]:
        raise KleanExportError(
            "Stage 1 inventory and K definition resolution disagree"
        )
    domain_rules = _domain_source_rules(
        validated, discovery_manifest_sha256
    )
    transformed, promoted_structural_definitions = (
        promote_referenced_structural_definitions(
            verification_text,
            validated["definitions"],
            validated["domain_lemmas"],
        )
    )
    transformed, lowered_structural_definition_rules = (
        lower_referenced_structural_definitions(
            transformed,
            validated["domain_lemmas"],
            promoted_structural_definitions,
        )
    )
    _parsed_module, functions = parse_verification(transformed)
    source_rules = _klean_source_rules(domain_rules, 0)
    export_module_name = f"{module.rsplit('-', 1)[0]}-KLEAN-EXPORT"
    package_name = f"klean-{problem.lower()}"
    library_name = lib_name(package_name)
    environment = dict(os.environ)

    publish_staging = Path(
        tempfile.mkdtemp(prefix=f".{destination.name}.", dir=destination.parent)
    )
    try:
        with tempfile.TemporaryDirectory(prefix=f"klean-{problem}-") as temporary:
            scratch = Path(temporary)
            export_k = stage_definition_driver(
                scratch,
                frozen_input,
                resolution,
                transformed,
                export_module(module, functions),
            )
            source_inventory_path = scratch / "source-rule-inventory.json"
            _write_json(
                source_inventory_path,
                {"schema_version": 1, "source_rules": source_rules},
            )
            definition = scratch / "kompiled"
            command = [
                "kompile",
                str(export_k),
                "--backend",
                "haskell",
                "--main-module",
                export_module_name,
                "--syntax-module",
                resolution.syntax_module,
                "--output-definition",
                str(definition),
            ]
            code, output = run_command(
                command,
                cwd=scratch,
                timeout=KOMPILE_TIMEOUT,
                env=environment,
            )
            if code != 0:
                raise KleanExportError(f"kompile failed ({code}): {output[-600:]}")
            lean_output = scratch / "lean-output"
            lean_output.mkdir()
            command = [
                sys.executable,
                str(KLEAN),
                str(definition),
                package_name,
                "-o",
                str(lean_output),
                "-r",
                "kxExport",
                "--lemmas",
                "--lemma-source",
                verification.name,
                "--source-rule-inventory",
                str(source_inventory_path),
            ]
            for function in functions:
                command.extend(("--spec-func", function.name))
            code, output = run_command(
                command,
                cwd=scratch,
                timeout=KLEAN_TIMEOUT,
                env=environment,
            )
            package = lean_output / package_name
            if code != 0 or not package.is_dir():
                raise KleanExportError(f"klean failed ({code}): {output[-600:]}")
            obligation_map = _bind_obligation_provenance(
                package, domain_rules, source_rules
            )
            (package / "lean-toolchain").write_text(lock["lean_toolchain"] + "\n")
            _patch_lake_build_directory(package)

            function_file = package / library_name / "Func.lean"
            modeled_collection_hooks: tuple[str, ...] = ()
            modeled_operational_hooks: tuple[str, ...] = ()
            modeled_recursive_functions: tuple[str, ...] = ()
            if function_file.is_file():
                modeled_text, modeled_collection_hooks = (
                    model_collection_hooks(function_file.read_text())
                )
                modeled_text, modeled_operational_hooks = (
                    model_core_operational_hooks(modeled_text)
                )
                modeled_text, modeled_recursive_functions = (
                    model_recursive_build_is(modeled_text)
                )
                _assert_no_unmodeled_hook_axioms(modeled_text)
                function_file.write_text(modeled_text)
            axiomatized: set[str] = set()
            noncomputable_repair = False
            build_code = 1
            build_output = ""
            for _attempt in range(8):
                build_code, build_output = run_command(
                    ["lake", "build"],
                    cwd=package,
                    timeout=BUILD_TIMEOUT,
                    env=environment,
                )
                if build_code == 0:
                    break
                if not function_file.is_file():
                    break
                newly_flagged = (
                    termination_failures(build_output)
                    | elaboration_failures(
                        function_file.read_text(), build_output
                    )
                ) - axiomatized
                if newly_flagged:
                    axiomatized.update(newly_flagged)
                    function_file.write_text(
                        axiomatize(function_file.read_text(), axiomatized)
                    )
                    continue
                if (
                    not noncomputable_repair
                    and needs_noncomputable(build_output)
                ):
                    noncomputable_repair = True
                    function_file.write_text(
                        mark_all_noncomputable(function_file.read_text())
                    )
                    continue
                break
            if build_code != 0:
                raise KleanExportError(
                    f"lake build failed ({build_code}): {build_output[-600:]}"
                )
            if tree_digest(frozen_input) != before_hash:
                raise KleanExportError("frozen input changed during export")
            if discovery_manifest.read_bytes() != discovery_bytes:
                raise KleanExportError(
                    "validated Stage 3 discovery manifest changed during export"
                )

            generated = publish_staging / "generated"
            shutil.copytree(
                package,
                generated,
                ignore=shutil.ignore_patterns(".lake", "build"),
            )
            inventory = _trust_inventory(
                generated,
                axiomatized=axiomatized,
                noncomputable_repair=noncomputable_repair,
                modeled_collection_hooks=modeled_collection_hooks,
                modeled_operational_hooks=modeled_operational_hooks,
                modeled_recursive_functions=modeled_recursive_functions,
            )
            input_manifest = {
                "schema_version": 3,
                "problem": problem,
                "frozen_input_sha256": before_hash,
                "stage1_workspace_sha256": before_hash,
                "stage3_discovery_manifest_sha256": (
                    discovery_manifest_sha256
                ),
                "verification_sha256": hashlib.sha256(
                    verification.read_bytes()
                ).hexdigest(),
                "verification_module": module,
                "syntax_module": resolution.syntax_module,
                "required_k_files": [
                    str(path) for path in resolution.required_files
                ],
                "inventory_sha256": validated["inventory_sha256"],
                "summary_functions": [
                    {
                        "name": function.name,
                        "return_sort": function.ret,
                        "argument_sorts": function.args,
                    }
                    for function in functions
                ],
                "promoted_structural_definitions": list(
                    promoted_structural_definitions
                ),
                "lowered_structural_definition_rules": list(
                    lowered_structural_definition_rules
                ),
                "modeled_collection_hooks": list(modeled_collection_hooks),
                "modeled_operational_hooks": list(
                    modeled_operational_hooks
                ),
                "modeled_recursive_functions": list(
                    modeled_recursive_functions
                ),
                "definitions": validated["definitions"],
                "operational_rules": validated["operational_rules"],
                "proved_derived_lemmas": validated[
                    "proved_derived_lemmas"
                ],
                "source_rules": domain_rules,
            }
            obligations = obligation_map.get("obligations")
            if not isinstance(obligations, list):
                raise KleanExportError("generated obligations are malformed")
            target = target_statement(generated)
            generator_manifest = {
                "schema_version": 3,
                "toolchain": lock,
                "klean_py_sha256": hashlib.sha256(KLEAN.read_bytes()).hexdigest(),
                "exporter_sha256": hashlib.sha256(
                    Path(__file__).read_bytes()
                ).hexdigest(),
                "modeled_collection_hooks": list(modeled_collection_hooks),
                "modeled_operational_hooks": list(
                    modeled_operational_hooks
                ),
                "modeled_recursive_functions": list(
                    modeled_recursive_functions
                ),
                "generated_tree_sha256": tree_digest(generated),
                "obligation_count": len(obligations),
                "obligation_map_sha256": hashlib.sha256(
                    (generated / "obligation-map.json").read_bytes()
                ).hexdigest(),
                "target": target,
                "provenance": {
                    "stage1_workspace_sha256": before_hash,
                    "stage3_discovery_manifest_sha256": (
                        discovery_manifest_sha256
                    ),
                    "inventory_sha256": validated["inventory_sha256"],
                    "generator_image_id": generator_image_id,
                },
            }
            result = {
                "schema_version": 3,
                "status": (
                    "OK" if obligations else "KLEAN_NO_OBLIGATIONS"
                ),
                "problem": problem,
                "generated_tree_sha256": generator_manifest[
                    "generated_tree_sha256"
                ],
                "frozen_input_sha256": before_hash,
                "stage3_discovery_manifest_sha256": (
                    discovery_manifest_sha256
                ),
                "trust_inventory_sha256": "",
                "obligation_count": len(obligations),
            }
            _write_json(publish_staging / "input-manifest.json", input_manifest)
            _write_json(
                publish_staging / "generator-manifest.json",
                generator_manifest,
            )
            _write_json(publish_staging / "trust-inventory.json", inventory)
            result["trust_inventory_sha256"] = hashlib.sha256(
                (publish_staging / "trust-inventory.json").read_bytes()
            ).hexdigest()
            _write_json(publish_staging / "export-result.json", result)
        publish_staging.rename(destination)
        return result
    except BaseException:
        if publish_staging.exists():
            shutil.rmtree(publish_staging)
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--discovery-manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--problem", required=True)
    parser.add_argument("--generator-image-id")
    parser.add_argument(
        "--toolchain-lock",
        type=Path,
        default=REPO / "data/klean-toolchain.lock.json",
    )
    arguments = parser.parse_args(argv)
    try:
        result = export_frozen(
            arguments.input,
            arguments.discovery_manifest,
            arguments.output,
            problem=arguments.problem,
            toolchain_lock=arguments.toolchain_lock,
            generator_image_id=arguments.generator_image_id,
        )
    except KleanExportError as error:
        print(f"Klean export failed: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
