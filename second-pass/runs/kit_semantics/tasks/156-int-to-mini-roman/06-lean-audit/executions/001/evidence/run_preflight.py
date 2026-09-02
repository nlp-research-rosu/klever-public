import json
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation

runs = []

def record(command, *, cwd, timeout):
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            timeout=timeout,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        code, output = result.returncode, result.stdout
    except subprocess.TimeoutExpired as error:
        code = 124
        captured = error.stdout or ""
        if isinstance(captured, bytes):
            captured = captured.decode(errors="replace")
        output = captured + f"\nTIMEOUT after {timeout}s\n"
    runs.append({
        "command": command,
        "cwd": str(cwd),
        "timeout": timeout,
        "exit_code": code,
        "complete_output": output,
    })
    return code, output

returned = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=record,
)
print(json.dumps({"returned_evidence": returned, "complete_runs": runs}, indent=2, sort_keys=True))

