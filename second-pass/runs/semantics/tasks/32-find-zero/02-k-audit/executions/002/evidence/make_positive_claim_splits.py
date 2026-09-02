#!/usr/bin/env python3
"""Split the two exact candidate claims so each can be reconstructed separately."""

from pathlib import Path
import textwrap


WORK = Path("/tmp/audit-work/candidate")
EVIDENCE = Path("/audit-output/evidence")


def main() -> int:
    source = (WORK / "spec.k").read_text()
    body = source.split("  imports VERIFICATION", 1)[1].rsplit("endmodule", 1)[0]
    separator = "\n  // The same execution, with its result fed to the postcondition checker."
    first, second_tail = body.split(separator, 1)
    claims = [
        (
            "AUDIT-SPEC-RESULT",
            textwrap.dedent(first).strip(),
            "audit-spec-result.k",
        ),
        (
            "AUDIT-SPEC-APPROX",
            textwrap.dedent(
                "// The same execution, with its result fed to the postcondition checker."
                + second_tail
            ).strip(),
            "audit-spec-approx.k",
        ),
    ]
    for module, claim_text, filename in claims:
        rendered = (
            'requires "verification.k"\n\n'
            f"module {module}\n"
            "  imports VERIFICATION\n\n"
            + "\n".join("  " + line if line else "" for line in claim_text.splitlines())
            + "\nendmodule\n"
        )
        (WORK / filename).write_text(rendered)
        (EVIDENCE / f"stage3-{filename}").write_text(rendered)
        print(f"{module}: {filename}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
