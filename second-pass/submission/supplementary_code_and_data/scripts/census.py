#!/usr/bin/env python3
"""Tally stage-6 (independent Lean audit) statuses.

Two modes:

1. Against a live runs tree (the layout produced by the pipeline):

       python3 scripts/census.py --runs-tree src/runs/<run-id>/tasks

   Reads every tasks/<task>/06-lean-audit/selected.json and tallies the
   recorded "status" field. Tasks without a stage-6 selection are counted
   as NOT_REACHED.

2. Against a packaged results summary (no runs tree required):

       python3 scripts/census.py --results data/results/results_kit_semantics.csv
       python3 scripts/census.py --results data/results/results_bare.csv --column stage2_status
       python3 scripts/census.py --results data/results/results_semantics.csv --column stage2_status

   Re-tallies a per-task CSV shipped with this package over the given
   status column (default stage6_status — the kit_semantics arm's primary
   verdict; the control arms' primary verdict column is stage2_status).
   The outputs should match data/results/census.json and the files in
   expected_results/.

Only the Python standard library is used.
"""

import argparse
import collections
import csv
import json
import os
import sys


def census_runs_tree(tasks_root: str) -> collections.Counter:
    counts: collections.Counter = collections.Counter()
    for task_dir in sorted(os.listdir(tasks_root)):
        full = os.path.join(tasks_root, task_dir)
        if not os.path.isdir(full):
            continue
        selected = os.path.join(full, "06-lean-audit", "selected.json")
        if os.path.exists(selected):
            with open(selected, "r", encoding="utf-8") as fh:
                status = json.load(fh).get("status", "UNKNOWN")
        else:
            status = "NOT_REACHED"
        counts[status] += 1
    return counts


def census_results_csv(csv_path: str, column: str) -> collections.Counter:
    counts: collections.Counter = collections.Counter()
    with open(csv_path, "r", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            counts[row[column]] += 1
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--runs-tree", help="path to runs/<run-id>/tasks")
    group.add_argument("--results", help="path to a results_<arm>.csv")
    parser.add_argument(
        "--column",
        default="stage6_status",
        help="status column to tally in --results mode (default: stage6_status)",
    )
    args = parser.parse_args()

    if args.runs_tree:
        counts = census_runs_tree(args.runs_tree)
    else:
        counts = census_results_csv(args.results, args.column)

    total = sum(counts.values())
    print(f"total tasks: {total}")
    for status in sorted(counts):
        print(f"{status}: {counts[status]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
