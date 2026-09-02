#!/usr/bin/env python3
"""Read-only provenance checks for the 68-pluck audit."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import stat
import sys


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
TRACE_ROOT = Path("/generation-evidence/codex-trace")


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path} is not a JSON object")
    return value


def file_hash(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def regular(path: Path) -> bool:
    return stat.S_ISREG(path.lstat().st_mode)


def real_directory(path: Path) -> bool:
    return stat.S_ISDIR(path.lstat().st_mode)


def pipeline_tree_hash(root: Path) -> str:
    """Reproduce /opt/humaneval/tools/pipeline_contract.py:sha256_tree."""
    if not real_directory(root):
        raise AssertionError(f"not a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in directory.iterdir():
            mode = child.lstat().st_mode
            relative = child.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", child))
                pending.append(child)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", child))
            else:
                raise AssertionError(f"linked or unsupported entry: {child}")
    digest = sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def require_hash(label: str, path: Path, expected: str) -> None:
    actual = file_hash(path)
    print(f"{label}: actual={actual} expected={expected} match={actual == expected}")
    if actual != expected:
        raise AssertionError(f"hash mismatch: {label}")


def main() -> int:
    audit = read_json(AUDIT)
    lock = read_json(LOCK)
    run = read_json(Path("/run.json"))
    task = read_json(Path("/task.json"))
    result = read_json(Path("/generation-result.json"))
    invocation = read_json(Path("/generation-evidence/invocation.json"))
    metrics = read_json(Path("/generation-evidence/metrics.json"))
    usage = read_json(Path("/generation-evidence/usage.json"))

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"campaign_match={audit['audit_campaign'] == lock}")
    assert audit["audit_campaign"] == lock
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    assert not Path("/reference/reference-semantics").exists()

    required_files = (
        AUDIT,
        LOCK,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    )
    required_dirs = (Path("/candidate"), Path("/generation-evidence"), TRACE_ROOT)
    for path in required_files:
        print(f"regular_file {path}={regular(path)}")
        assert regular(path)
    for path in required_dirs:
        print(f"real_directory {path}={real_directory(path)}")
        assert real_directory(path)
    for root in (Path("/candidate"), Path("/reference"), Path("/generation-evidence")):
        for path in root.rglob("*"):
            mode = path.lstat().st_mode
            if not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
                raise AssertionError(f"linked or unsupported entry: {path}")

    hashes = audit["hashes"]
    direct_checks = (
        ("audit_campaign_lock_sha256", LOCK),
        ("canonical_sha256", Path("/reference/canonical.py")),
        ("trusted_prompt_sha256", Path("/reference/prompt.py")),
        ("trusted_translator_sha256", Path("/reference/py2mpy.py")),
        ("run_manifest_sha256", Path("/run.json")),
        ("task_manifest_sha256", Path("/task.json")),
        ("stage1_result_sha256", Path("/generation-result.json")),
        ("stage1_invocation_sha256", Path("/generation-evidence/invocation.json")),
        ("generation_metrics_sha256", Path("/generation-evidence/metrics.json")),
        ("generation_usage_sha256", Path("/generation-evidence/usage.json")),
        ("generation_codex_last_sha256", Path("/generation-evidence/codex-last.txt")),
        ("generation_codex_output_sha256", Path("/generation-evidence/codex-output.log")),
        ("generation_prompt_sha256", Path("/generation-evidence/prompt.txt")),
    )
    for label, path in direct_checks:
        require_hash(label, path, hashes[label])

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print("candidate_prompt_byte_identity=True")
    print("candidate_translator_byte_identity=True")

    for relative, expected in result["outputs"]["evidence"].items():
        require_hash(
            f"generation_result.outputs.evidence[{relative}]",
            Path("/generation-evidence") / relative,
            expected,
        )

    candidate_pipeline_hash = pipeline_tree_hash(Path("/candidate"))
    trace_pipeline_hash = pipeline_tree_hash(TRACE_ROOT)
    print(f"candidate_pipeline_tree_hash={candidate_pipeline_hash}")
    print(f"stage1_workspace_hash={result['outputs']['workspace_sha256']}")
    print(
        "candidate_matches_retained_stage1="
        f"{candidate_pipeline_hash == result['outputs']['workspace_sha256']}"
    )
    assert candidate_pipeline_hash == result["outputs"]["workspace_sha256"]
    print(f"trace_pipeline_tree_hash={trace_pipeline_hash}")
    print(f"usage_source_trace_hash={usage['source_trace_sha256']}")
    print(
        "trace_matches_usage_source="
        f"{trace_pipeline_hash == usage['source_trace_sha256']}"
    )
    assert trace_pipeline_hash == usage["source_trace_sha256"]
    print(
        "launcher_candidate_tree_record="
        f"{hashes['candidate_tree_sha256']} (launcher-specific aggregate)"
    )
    print(
        "launcher_trace_tree_record="
        f"{hashes['generation_codex_trace_sha256']} (launcher-specific aggregate)"
    )

    assert task["problem_id"] == audit["problem_id"] == "68-pluck"
    assert task["condition"]["name"] == audit["condition"] == "bare"
    assert result["session_id"] == invocation["session_id"]
    assert invocation["status"] == metrics["status"] == "SUCCEEDED"
    assert invocation["prompt_sha256"] == hashes["generation_prompt_sha256"]
    assert result["outputs"]["workspace_sha256"] == invocation["retained_workspace_sha256"]
    print("cross_record_consistency=True")

    trace_files = sorted(TRACE_ROOT.rglob("*.jsonl"))
    assert len(trace_files) == 1
    top_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    function_names: Counter[str] = Counter()
    exec_commands: list[str] = []
    invalid_lines: list[int] = []
    last_line = 0
    for line_number, line in enumerate(
        trace_files[0].read_text(encoding="utf-8").splitlines(), start=1
    ):
        last_line = line_number
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            invalid_lines.append(line_number)
            continue
        top_types[str(record.get("type"))] += 1
        payload = record.get("payload")
        if isinstance(payload, dict):
            payload_type = str(payload.get("type"))
            payload_types[payload_type] += 1
            if payload_type == "function_call":
                name = str(payload.get("name"))
                function_names[name] += 1
                if name == "exec_command":
                    try:
                        arguments = json.loads(str(payload.get("arguments")))
                        exec_commands.append(str(arguments.get("cmd", "")))
                    except json.JSONDecodeError:
                        exec_commands.append("<malformed arguments>")
            elif payload_type == "custom_tool_call":
                name = str(payload.get("name"))
                function_names[f"custom:{name}"] += 1
                custom_input = str(payload.get("input", ""))
                # Legacy Codex nested the shell calls in JavaScript orchestration.
                marker = "tools.exec_command({cmd:"
                cursor = 0
                while True:
                    start = custom_input.find(marker, cursor)
                    if start < 0:
                        break
                    start += len(marker)
                    end = custom_input.find(",workdir:", start)
                    if end < 0:
                        end = min(len(custom_input), start + 1000)
                    exec_commands.append(custom_input[start:end])
                    cursor = end
    print(f"trace_line_count={last_line}")
    print(f"trace_invalid_json_lines={invalid_lines}")
    print(f"trace_top_types={dict(sorted(top_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
    print(f"trace_function_names={dict(sorted(function_names.items()))}")
    print(f"trace_exec_command_count={len(exec_commands)}")
    for index, command in enumerate(exec_commands, start=1):
        bounded = command.replace("\n", "\\n")
        if len(bounded) > 500:
            bounded = bounded[:500] + "...<bounded>"
        print(f"trace_exec[{index}]={bounded}")
    assert not invalid_lines
    assert usage["selected_event"]["line_number"] <= last_line

    output_text = Path("/generation-evidence/codex-output.log").read_text(
        encoding="utf-8"
    )
    print(f"codex_output_line_count={len(output_text.splitlines())}")
    print(f"codex_output_top_count={output_text.count('#Top')}")
    print(f"codex_output_stuck_count={output_text.count('WarnStuckClaimState')}")
    print(f"codex_output_kprove_mentions={output_text.count('kprove')}")
    print(f"generation_marker={result['result_marker']}")
    print("stage1_provenance_checks=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
