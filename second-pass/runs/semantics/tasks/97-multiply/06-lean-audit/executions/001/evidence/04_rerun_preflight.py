#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

from tools import klean_preflight


commands = []


def logged_run(command, *, cwd, timeout):
    result = subprocess.run(
        command,
        cwd=cwd,
        timeout=timeout,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    commands.append(
        {
            "command": command,
            "cwd": str(cwd),
            "timeout": timeout,
            "exit_code": result.returncode,
            "output": result.stdout,
        }
    )
    return result.returncode, result.stdout


result = klean_preflight.check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=logged_run,
)
recorded = json.loads(
    Path("/reference/klean-generation/preflight.json").read_text()
)
embedded = json.loads(Path("/audit-input.json").read_text())[
    "resolution"
]["stage4_preflight"]
print("CHECK_GENERATION_RETURNED_EVIDENCE")
print(json.dumps(result, indent=2, sort_keys=True))
print(f"RETURN_MATCHES_RECORDED_PREFLIGHT={result == recorded}")
print(f"RETURN_MATCHES_AUDIT_INPUT_PREFLIGHT={result == embedded}")
stable_fields = (
    "schema_version",
    "status",
    "frozen_input_sha256",
    "stage1_workspace_sha256",
    "stage3_discovery_manifest_sha256",
    "generated_tree_sha256",
    "target",
    "obligation_count",
    "trust_declaration_count",
    "designated_sorry_count",
)
for field in stable_fields:
    if result[field] != recorded[field] or result[field] != embedded[field]:
        raise SystemExit(f"rerun preflight stable field differs: {field}")
print("STABLE_PREFLIGHT_FIELDS_MATCH_RECORDED_AND_AUDIT_INPUT=True")
for index, diagnostic in enumerate(result["diagnostics"]):
    recorded_diagnostic = recorded["diagnostics"][index]
    embedded_diagnostic = embedded["diagnostics"][index]
    stable_diagnostic = {
        "command": diagnostic["command"],
        "exit_code": diagnostic["exit_code"],
    }
    if (
        stable_diagnostic
        != {
            "command": recorded_diagnostic["command"],
            "exit_code": recorded_diagnostic["exit_code"],
        }
        or stable_diagnostic
        != {
            "command": embedded_diagnostic["command"],
            "exit_code": embedded_diagnostic["exit_code"],
        }
    ):
        raise SystemExit(f"rerun preflight command result differs: {index}")
    rerun_lines = sorted(line for line in diagnostic["output_tail"].splitlines() if line)
    recorded_lines = sorted(
        line for line in recorded_diagnostic["output_tail"].splitlines() if line
    )
    if rerun_lines != recorded_lines:
        raise SystemExit(f"rerun preflight build messages differ: {index}")
print("PREFLIGHT_COMMAND_EXIT_CODES_AND_OUTPUT_LINE_MULTISETS_MATCH=True")
print("COMPLETE_COMMAND_OUTPUTS")
for index, record in enumerate(commands):
    print(f"COMMAND_RECORD {index}")
    print(json.dumps({key: value for key, value in record.items() if key != "output"}, sort_keys=True))
    print("OUTPUT_BEGIN")
    print(record["output"], end="" if record["output"].endswith("\n") else "\n")
    print("OUTPUT_END")
if result["status"] != "KLEAN_NO_OBLIGATIONS":
    raise SystemExit(
        f"unexpected preflight status for independently empty domain set: {result['status']}"
    )
if result["obligation_count"] != 0 or result["target"] is not None:
    raise SystemExit("zero-domain preflight generated obligations or a target")
print("RERUN_PREFLIGHT_PASS")
