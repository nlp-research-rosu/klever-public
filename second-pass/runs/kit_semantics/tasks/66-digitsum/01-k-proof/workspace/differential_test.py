#!/usr/bin/env python3
import random
import subprocess
import tempfile
from pathlib import Path

from solution import digitSum


def ascii_contract_oracle(text):
    codes = map(ord, text)
    return sum(code for code in codes if 65 <= code <= 90)


def cases():
    fixed = [
        "",
        "abAB",
        "abcCd",
        "helloE",
        "woArBld",
        "aAaaaXa",
        "".join(chr(code) for code in range(32, 127)),
        "AZ@[`az",
    ]
    rng = random.Random(108)
    alphabet = [chr(code) for code in range(32, 127)]
    random_cases = [
        "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 65)))
        for _ in range(200)
    ]
    return fixed + random_cases


def main():
    samples = cases()
    mismatches = [
        (sample, digitSum(sample), ascii_contract_oracle(sample))
        for sample in samples
        if digitSum(sample) != ascii_contract_oracle(sample)
    ]
    if mismatches:
        raise AssertionError(f"CPython mismatches: {mismatches[:3]!r}")

    source = Path("solution.py").read_text(encoding="utf-8")
    assertions = "\n".join(
        f"assert digitSum({sample!r}) == {ascii_contract_oracle(sample)}"
        for sample in samples
    )

    with tempfile.TemporaryDirectory(prefix="digit-sum-diff-") as temp_dir:
        temp = Path(temp_dir)
        py_path = temp / "differential_smoke.py"
        mpy_path = temp / "differential_smoke.mpy"
        py_path.write_text(source + "\n\n" + assertions + "\n", encoding="utf-8")

        with mpy_path.open("w", encoding="utf-8") as output:
            subprocess.run(
                ["python3", "py2mpy.py", str(py_path)],
                check=True,
                stdout=output,
            )
        result = subprocess.run(
            ["krun", str(mpy_path), "--definition", "runtime-kompiled"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if result.returncode != 0:
            raise AssertionError(
                f"krun exited {result.returncode}:\n{result.stdout[-4000:]}"
            )
        if "<k>\n    .K\n  </k>" not in result.stdout:
            raise AssertionError("krun did not terminate with an empty <k> cell")

    print(
        f"cases={len(samples)} "
        "python_mismatches=0 "
        "krun_assertion_failures=0 "
        "krun_exit=0"
    )


if __name__ == "__main__":
    main()
