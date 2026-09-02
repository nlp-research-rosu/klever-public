#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import json
import subprocess

REPO = Path("/home/yuqing/Documents/Code/humaneval-benchmark")
RUN = "codex-gpt-5.6-sol-xhigh-semantics"
IMAGE = "sha256:88f9bc14390ad09f165862a1f8d7167fa1aacf5ac30803c1d5c8e18b4d396816"
PROBLEMS = (
    "100-make-a-pile 106-f 114-minSubArraySum 120-maximum 130-tri "
    "131-digits 24-largest-divisor 29-filter-by-prefix 37-sort-even "
    "38-decode-cyclic 51-remove-vowels 59-largest-prime-factor "
    "63-fibfib 79-decimal-to-binary 94-skjkasdkd"
).split()


def run_one(problem: str) -> dict[str, object]:
    task = REPO / "runs" / RUN / "tasks" / problem
    stage4 = task / "04-klean-generation"
    selected = json.loads((stage4 / "selected.json").read_text())
    generation = (stage4 / selected["relative_path"]).resolve()
    candidate = (task / "05-lean-proof/workspace").resolve()
    command = [
        "docker", "run", "--rm", "--network", "none", "--pull=never",
        "--read-only", "--tmpfs", "/tmp:rw,exec,nosuid,size=8g",
        "--memory", "8g", "--memory-swap", "8g",
        "--mount", f"type=bind,src={generation},dst=/generation,readonly",
        "--mount", f"type=bind,src={candidate},dst=/candidate,readonly",
        "--entrypoint", "python3", IMAGE,
        "/opt/humaneval/tools/stage5_mechanical_check.py",
        "--generation", "/generation", "--candidate", "/candidate",
    ]
    print(f"START {problem}", flush=True)
    process = subprocess.run(
        command, cwd=REPO, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    result: dict[str, object] = {
        "problem": problem,
        "returncode": process.returncode,
        "stderr": process.stderr[-4000:],
    }
    try:
        result["document"] = json.loads(process.stdout)
    except (TypeError, ValueError):
        result["stdout"] = process.stdout[-4000:]
    print(
        f"DONE {problem} rc={process.returncode} "
        f"status={getattr(result.get('document'), 'get', lambda *_: None)('status')}",
        flush=True,
    )
    return result


def main() -> int:
    results = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(run_one, problem) for problem in PROBLEMS]
        for future in as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda item: str(item["problem"]))
    Path("/tmp/semantics-stage5-existing-mechanical-scan.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n"
    )
    bad = [
        item for item in results
        if item["returncode"] != 0
        or not isinstance(item.get("document"), dict)
        or item["document"].get("status") != "PASS"
    ]
    print(f"SUMMARY completed={len(results)} bad={len(bad)}", flush=True)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
