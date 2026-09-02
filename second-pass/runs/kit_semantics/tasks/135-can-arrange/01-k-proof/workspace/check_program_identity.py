import re
from pathlib import Path


def normalize(text):
    # K's surface syntax permits empty statement-list tails to be written
    # explicitly as .Stmts; py2mpy omits them in juxtaposed sequences.
    text = text.replace(".Stmts", "")
    return re.sub(r"\s+", "", text)


program = normalize(Path("solution.mpy").read_text())
specification = normalize(Path("spec.k").read_text())

if program not in specification:
    raise SystemExit(
        "solution.mpy's translated Module term is not embedded in spec.k"
    )

print("program_identity=match")
