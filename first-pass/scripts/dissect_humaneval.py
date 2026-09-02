#!/usr/bin/env python3
"""Dissect the HumanEval dataset into one workable folder per problem.

Each HumanEval record bundles four useful pieces that this script splits into
separate files so each problem can be worked on in isolation:

    <out>/<num>-<entry-point-dashed>/
        meta.json            task_id, entry_point, num, name
        prompt.py            the question: signature + docstring, no body
        canonical_solution   the reference body fragment (completes prompt.py)
        solution.py          prompt + canonical_solution = full runnable function
        test.py              the dataset `test` section (defines check(), no call)
        run.py               solution + test + check(<entry_point>) = runnable script

Folder naming mirrors the pre-existing convention (e.g. HumanEval/3 ->
`3-below-zero`). Running `python run.py` exits 0 iff the canonical solution
passes its own tests.

Usage:
    python scripts/dissect_humaneval.py                 # all 164 problems
    python scripts/dissect_humaneval.py --only 0 3 9    # just these task numbers
"""
from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = REPO_ROOT / "data/humaneval/HumanEval.jsonl"
DEFAULT_OUT = REPO_ROOT / "data/humaneval/problems"


def load_records(dataset: Path):
    """Yield each problem dict. Accepts plain .jsonl or gzipped .jsonl.gz."""
    opener = gzip.open if dataset.suffix == ".gz" else open
    with opener(dataset, "rt", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield json.loads(line)


def folder_name(rec: dict) -> str:
    num = rec["task_id"].split("/")[-1]
    return f"{num}-{rec['entry_point'].replace('_', '-')}"


def assemble_run(rec: dict) -> str:
    """Full runnable script: solution + test + the call to check()."""
    return (
        rec["prompt"]
        + rec["canonical_solution"]
        + "\n\n"
        + rec["test"]
        + f"\ncheck({rec['entry_point']})\n"
    )


def write_problem(rec: dict, out_dir: Path) -> Path:
    d = out_dir / folder_name(rec)
    d.mkdir(parents=True, exist_ok=True)

    (d / "meta.json").write_text(
        json.dumps(
            {
                "task_id": rec["task_id"],
                "entry_point": rec["entry_point"],
                "num": int(rec["task_id"].split("/")[-1]),
                "name": folder_name(rec),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (d / "prompt.py").write_text(rec["prompt"], encoding="utf-8")
    (d / "canonical_solution").write_text(rec["canonical_solution"], encoding="utf-8")
    (d / "solution.py").write_text(rec["prompt"] + rec["canonical_solution"], encoding="utf-8")
    (d / "test.py").write_text(rec["test"], encoding="utf-8")
    (d / "run.py").write_text(assemble_run(rec), encoding="utf-8")
    return d


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dataset", type=Path, default=DEFAULT_DATASET,
                    help=f"HumanEval .jsonl or .jsonl.gz (default: {DEFAULT_DATASET})")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT,
                    help=f"output directory (default: {DEFAULT_OUT})")
    ap.add_argument("--only", nargs="*", type=int, metavar="N",
                    help="only emit these task numbers (e.g. --only 0 3 9)")
    args = ap.parse_args()

    if not args.dataset.exists():
        raise SystemExit(f"dataset not found: {args.dataset}")

    only = set(args.only) if args.only else None
    count = 0
    for rec in load_records(args.dataset):
        num = int(rec["task_id"].split("/")[-1])
        if only is not None and num not in only:
            continue
        write_problem(rec, args.out)
        count += 1

    print(f"wrote {count} problem folder(s) under {args.out}")


if __name__ == "__main__":
    main()
