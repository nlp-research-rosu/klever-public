from pathlib import Path
import hashlib
import json
import subprocess

from tools.klean_preflight import check_generation


def recording_run(command, *, cwd, timeout):
    print("SUBCOMMAND:", json.dumps(command))
    print("CWD:", cwd)
    print("TIMEOUT:", timeout)
    try:
        process = subprocess.run(
            command,
            cwd=cwd,
            timeout=timeout,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        code, output = process.returncode, process.stdout
    except subprocess.TimeoutExpired as error:
        code, output = 124, (error.stdout or "") + (error.stderr or "")
    print("EXIT_CODE:", code)
    print("OUTPUT_BEGIN")
    print(output, end="" if output.endswith("\n") or not output else "\n")
    print("OUTPUT_END")
    print("OUTPUT_SHA256:", hashlib.sha256(output.encode()).hexdigest())
    return code, output


print(
    "COMMAND: tools.klean_preflight.check_generation(/reference/k-proof, "
    "/reference/lemma-discovery.json, /reference/klean-generation, "
    "toolchain_lock=/reference/klean-toolchain.lock.json)"
)
result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=recording_run,
)
print("CHECK_GENERATION_RESULT_BEGIN")
print(json.dumps(result, indent=2, sort_keys=True))
print("CHECK_GENERATION_RESULT_END")
