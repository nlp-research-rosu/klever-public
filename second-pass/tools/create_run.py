#!/usr/bin/env python3
"""Create one immutable, stage-oriented Codex benchmark run."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools.pipeline_contract import PipelineContractError, create_run


def _selected_problem_ids(repo: Path) -> list[str]:
    try:
        document = json.loads((repo / "data/selection.json").read_text())
        values = [entry["id"] for entry in document["selected"]]
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise PipelineContractError(f"cannot read selected problems: {error}") from error
    return values


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_id")
    parser.add_argument("--config", required=True)
    parser.add_argument("--problem", action="append", default=[])
    parser.add_argument("--all-selected", action="store_true")
    arguments = parser.parse_args(argv)
    if arguments.all_selected and arguments.problem:
        parser.error("--all-selected and --problem are mutually exclusive")
    problems = (
        _selected_problem_ids(REPO) if arguments.all_selected else arguments.problem
    )
    try:
        destination = create_run(
            REPO,
            run_id=arguments.run_id,
            config=arguments.config,
            problem_ids=problems,
        )
    except PipelineContractError as error:
        print(f"run creation failed: {error}", file=sys.stderr)
        return 2
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
