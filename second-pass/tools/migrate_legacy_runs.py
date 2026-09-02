#!/usr/bin/env python3
"""Transactionally migrate the two approved legacy benchmark runs."""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools import legacy_migration, pipeline_contract


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=REPO)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    parser.add_argument("--report", type=Path)
    return parser


def _emit(document: dict[str, Any], report: Path | None) -> None:
    if report is not None:
        pipeline_contract.write_json_atomic(report, document)
    print(json.dumps(document, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    repo = arguments.repo
    try:
        with legacy_migration.migration_lock(repo):
            if arguments.apply:
                pending = legacy_migration._read_journal(repo)
                legacy_migration.recover_transaction(repo)
                if (
                    pending is not None
                    and pending["phase"] in {"VALIDATED", "COMPLETE"}
                ):
                    _emit(
                        {
                            "mode": "apply",
                            "phase": "COMPLETE",
                            "recovered": True,
                            "transaction_id": pending["transaction_id"],
                        },
                        arguments.report,
                    )
                    return 0
            elif legacy_migration._read_journal(repo) is not None:
                raise legacy_migration.LegacyMigrationError(
                    "an interrupted migration requires --apply recovery"
                )

            plan = legacy_migration.scan_legacy_sources(repo)
            activity = legacy_migration.source_activity_report(
                repo,
                plan,
                require_docker=arguments.apply,
            )
            legacy_migration.assert_publication_destinations_available(
                repo,
                plan,
            )
            document = legacy_migration.plan_document(plan)
            document["mode"] = "apply" if arguments.apply else "dry-run"
            document["activity"] = activity
            if arguments.dry_run:
                document["phase"] = "PLANNED"
                _emit(document, arguments.report)
                return 0

            transaction_id = str(uuid.uuid4())
            staged = legacy_migration.stage_migration(
                repo,
                plan,
                transaction_id,
            )
            legacy_migration.publish_migration(repo, staged, plan)
            document["phase"] = "COMPLETE"
            document["validation"] = {
                "runs": document["totals"]["runs"],
                "tasks": document["totals"]["tasks"],
                "succeeded": document["totals"]["succeeded"],
                "timeout": document["totals"]["timeout"],
                "blocked": document["totals"]["provenance_incomplete"],
                "pass": document["totals"]["pass"],
                "concerns": document["totals"]["concerns"],
                "fail": document["totals"]["fail"],
                "eligible": (
                    document["totals"]["pass"]
                    + document["totals"]["concerns"]
                ),
            }
            _emit(document, arguments.report)
            return 0
    except legacy_migration.LegacyMigrationRollbackError as error:
        print(f"legacy migration rollback error: {error}", file=sys.stderr)
        return 3
    except (
        legacy_migration.LegacyMigrationError,
        pipeline_contract.PipelineContractError,
        OSError,
        ValueError,
    ) as error:
        print(f"legacy migration error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
