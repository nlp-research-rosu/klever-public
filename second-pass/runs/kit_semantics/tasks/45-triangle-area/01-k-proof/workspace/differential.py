from decimal import Decimal
from pathlib import Path
import subprocess
import sys
import tempfile

from solution import triangle_area


ROOT = Path(__file__).resolve().parent
VALUES = (-4, -1.5, 0, 0.5, 2, 3.5, 5)


def oracle(a, h):
    # Decimal supplies an implementation independent of Python binary-float
    # multiplication/division and of the K FLOAT hooks.
    return float((Decimal(str(a)) * Decimal(str(h))) / Decimal(2))


def main():
    cases = [(a, h, oracle(a, h)) for a in VALUES for h in VALUES]
    mismatches = [
        (a, h, expected, triangle_area(a, h))
        for a, h, expected in cases
        if triangle_area(a, h) != expected
    ]
    if mismatches:
        print(f"python_cases={len(cases)} mismatches={len(mismatches)}")
        for mismatch in mismatches:
            print(mismatch)
        return 1

    assertions = "\n".join(
        f"assert triangle_area({a!r}, {h!r}) == {expected!r}"
        for a, h, expected in cases
    )
    source = (ROOT / "solution.py").read_text() + "\n\n" + assertions + "\n"

    with tempfile.TemporaryDirectory(prefix="triangle-area-") as tmp:
        tmp_path = Path(tmp)
        py_path = tmp_path / "differential_smoke.py"
        mpy_path = tmp_path / "differential_smoke.mpy"
        py_path.write_text(source)

        with mpy_path.open("w") as output:
            translated = subprocess.run(
                [sys.executable, str(ROOT / "py2mpy.py"), str(py_path)],
                stdout=output,
                text=True,
            )
        if translated.returncode != 0:
            return translated.returncode

        executed = subprocess.run(
            [
                "krun",
                str(mpy_path),
                "--definition",
                str(ROOT / "runtime-kompiled"),
            ],
            capture_output=True,
            text=True,
        )
        if executed.returncode != 0:
            print(executed.stdout)
            print(executed.stderr, file=sys.stderr)
            return executed.returncode

    print(
        f"python_cases={len(cases)} k_cases={len(cases)} "
        "oracle=Decimal mismatches=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
