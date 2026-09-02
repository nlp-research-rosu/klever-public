#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
from pathlib import Path


def load_source_prompts(source_root: Path) -> dict[int, bytes]:
    prompts: dict[int, bytes] = {}
    for meta_path in sorted(source_root.glob("*/meta.json")):
        meta = json.loads(meta_path.read_text())
        task_id = meta["task_id"]
        match = re.fullmatch(r"HumanEval/(\d+)", task_id)
        if not match:
            raise ValueError(f"invalid task id in {meta_path}: {task_id}")
        number = int(match.group(1))
        prompt_path = meta_path.with_name("prompt.py")
        if not prompt_path.is_file():
            raise FileNotFoundError(prompt_path)
        if number in prompts:
            raise ValueError(f"duplicate HumanEval/{number}")
        prompts[number] = prompt_path.read_bytes()
    expected = set(range(164))
    if set(prompts) != expected:
        missing = sorted(expected - set(prompts))
        extra = sorted(set(prompts) - expected)
        raise ValueError(f"prompt task mismatch: missing={missing}, extra={extra}")
    return prompts


def question_directories(repo_root: Path) -> dict[int, Path]:
    result: dict[int, Path] = {}
    for path in sorted((repo_root / "data/questions").iterdir()):
        if not path.is_dir():
            continue
        match = re.match(r"(\d+)-", path.name)
        if not match:
            continue
        number = int(match.group(1))
        if number in result:
            raise ValueError(f"duplicate question number {number}")
        result[number] = path
    if set(result) != set(range(164)):
        raise ValueError("benchmark must contain question directories 0..163")
    return result


def import_prompts(source_root: Path, repo_root: Path) -> dict[str, object]:
    prompts = load_source_prompts(source_root)
    directories = question_directories(repo_root)
    tasks: dict[str, dict[str, str]] = {}
    for number in range(164):
        target = directories[number] / "prompt.py"
        target.write_bytes(prompts[number])
        tasks[f"HumanEval/{number}"] = {
            "directory": directories[number].name,
            "sha256": hashlib.sha256(prompts[number]).hexdigest(),
        }
    lock: dict[str, object] = {
        "schema_version": 1,
        "dataset": "openai/openai_humaneval",
        "tasks": tasks,
    }
    lock_path = repo_root / "data/humaneval-prompts.lock.json"
    lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n")
    return lock


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root", type=Path)
    parser.add_argument(
        "--repo-root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    args = parser.parse_args()
    import_prompts(args.source_root.resolve(), args.repo_root.resolve())


if __name__ == "__main__":
    main()
