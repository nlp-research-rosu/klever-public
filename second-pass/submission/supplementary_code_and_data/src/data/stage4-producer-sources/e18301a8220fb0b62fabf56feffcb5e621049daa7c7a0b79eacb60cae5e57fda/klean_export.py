#!/usr/bin/env python3
"""Deterministically export one frozen K proof workspace to a Lean project."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
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
_DEF_RE = re.compile(r"^(\s*)(?:noncomputable\s+)?def\s+(\S+)\b")
_NONCOMPUTABLE_RE = re.compile(r"(?m)^\s*noncomputable\s+def\s+(\S+)")
_LEAN_NAMESPACE_RE = re.compile(r"^\s*namespace\s+(\S+)\s*$")
_LEAN_END_RE = re.compile(r"^\s*end(?:\s+(\S+))?\s*$")
_LEAN_TRUST_DECL_RE = re.compile(
    r"^\s*(axiom|opaque)\s+(\S+)\s+(.+?)\s*$"
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
    modules: dict[str, tuple[Path, tuple[str, ...]]] = {}
    file_modules: dict[Path, tuple[str, ...]] = {}
    file_requires: dict[Path, tuple[Path, ...]] = {}
    for path in files:
        text = path.read_text()
        declared: list[str] = []
        for block in MODULE_BLOCK_RE.finditer(text):
            name = block.group("name")
            if name in modules:
                previous = modules[name][0]
                raise KleanExportError(
                    f"duplicate module definition {name}: {previous} and {path}"
                )
            imports = tuple(IMPORT_RE.findall(block.group("body")))
            modules[name] = (path, imports)
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
    reached_modules: set[str] = set()
    reached_files: set[Path] = set()
    pending_modules = [verification_module]
    pending_files = [verification_file]
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
        definition = modules.get(name)
        if definition is None:
            continue
        path, imports = definition
        if path not in reached_files:
            pending_files.append(path)
        pending_modules.extend(imports)

    syntax_modules = sorted(
        name
        for name in reached_modules
        if name.endswith("-SYNTAX") and name in modules
    )
    preferred = (
        verification_module.removesuffix("-VERIFICATION") + "-SYNTAX"
    )
    if preferred in syntax_modules:
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
    return DefinitionResolution(
        verification_file=verification_file,
        verification_module=verification_module,
        syntax_module=syntax_module,
        required_files=tuple(sorted(reached_files, key=str)),
    )


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
    setting = 'buildDir = "/tmp/klean-generated-build"\n'
    if setting in text:
        return
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
                    "deterministic termination repair"
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
    return [
        {
            "source_rule_id": rule["source_rule_id"],
            "start_line": rule["start_line"] + line_offset,
            "end_line": rule["end_line"] + line_offset,
            "normalized_sha256": rule["normalized_sha256"],
            "classification": "TRUST_OBLIGATION",
        }
        for rule in domain_rules
    ]


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
    _parsed_module, functions = parse_verification(verification_text)
    domain_rules = _domain_source_rules(
        validated, discovery_manifest_sha256
    )
    untagged_domain_rules = [
        rule
        for rule in domain_rules
        if "simplification" not in rule["attributes"]
    ]
    if untagged_domain_rules:
        raise KleanExportError(
            "untagged DOMAIN_LEMMA cannot be translated into a deterministic "
            "Lean obligation: "
            + untagged_domain_rules[0]["source_rule_id"]
        )
    if domain_rules and not functions:
        raise KleanExportError(
            "verification.k contains no declared summary function scope"
        )
    try:
        transformed = k_rule_inventory.desimplify_rule_ids(
            verification_text,
            [
                rule["source_rule_id"]
                for rule in validated["definitions"]
                if "simplification" in rule["attributes"]
            ],
        )
    except k_rule_inventory.KRuleInventoryError as error:
        raise KleanExportError(str(error)) from error
    dependencies = [
        path
        for path in resolution.required_files
        if path != resolution.verification_file
    ]
    if dependencies:
        preamble = "".join(
            f'requires "{path}"\n' for path in dependencies
        )
        transformed = preamble + transformed
    else:
        preamble = ""
    source_rules = _klean_source_rules(
        domain_rules, preamble.count("\n")
    )
    transformed += "\n" + export_module(module, functions)
    transformed = absolutize_requires(transformed, frozen_input)
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
            export_k = scratch / "export.k"
            export_k.write_text(transformed)
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
                export_k.name,
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
                    termination_failures(build_output) - axiomatized
                )
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
