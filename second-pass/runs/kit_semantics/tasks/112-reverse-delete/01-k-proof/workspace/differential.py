#!/usr/bin/env python3
import argparse
import importlib.util
import itertools
import re
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def oracle(s, c):
    deleted = set(c)
    result = "".join(ch for ch in s if ch not in deleted)
    return result, result == result[::-1]


def words(alphabet, maximum):
    yield ""
    for length in range(1, maximum + 1):
        for chars in itertools.product(alphabet, repeat=length):
            yield "".join(chars)


def load_solution():
    spec = importlib.util.spec_from_file_location(
        "verified_solution", ROOT / "solution.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.reverse_delete


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--definition",
        default="runtime-kompiled",
        help="LLVM definition used by krun",
    )
    args = parser.parse_args()

    ascii_cases = [
        (s, c)
        for s in words("ab", 3)
        for c in words("ab", 2)
    ]
    ascii_cases += [
        ("abcde", "ae"),
        ("abcdef", "b"),
        ("abcdedcba", "ab"),
        ("a b a", " "),
        ("!00!", "x"),
    ]
    python_cases = ascii_cases + [
        ("réifier", "é"),
        ("🙂a🙂", "a"),
        ("नमन", ""),
    ]

    reverse_delete = load_solution()
    python_mismatches = [
        (s, c, reverse_delete(s, c), oracle(s, c))
        for s, c in python_cases
        if reverse_delete(s, c) != oracle(s, c)
    ]
    print(
        f"CPython oracle cases: {len(python_cases)}; "
        f"mismatches: {len(python_mismatches)}"
    )
    if python_mismatches:
        print(python_mismatches[:3])
        return 1

    source = (ROOT / "solution.py").read_text(encoding="utf-8")
    for s, c in ascii_cases:
        source += (
            f"\nassert reverse_delete({s!r}, {c!r}) "
            f"== {oracle(s, c)!r}\n"
        )

    with tempfile.TemporaryDirectory(prefix="reverse-delete-") as directory:
        directory = Path(directory)
        source_path = directory / "differential.py"
        mpy_path = directory / "differential.mpy"
        source_path.write_text(source, encoding="utf-8")
        with mpy_path.open("w", encoding="utf-8") as output:
            translated = subprocess.run(
                ["python3", str(ROOT / "py2mpy.py"), str(source_path)],
                stdout=output,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
        if translated.returncode != 0:
            print(translated.stderr)
            return translated.returncode

        executed = subprocess.run(
            [
                "krun",
                str(mpy_path),
                "--definition",
                str(ROOT / args.definition),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        normal = (
            executed.returncode == 0
            and re.search(
                r"<exc>\s*NoExc\s*</exc>", executed.stdout
            )
            and re.search(
                r"<exit-code>\s*0\s*</exit-code>", executed.stdout
            )
        )
        print(
            f"K differential cases: {len(ascii_cases)}; "
            f"mismatches: {0 if normal else 1}"
        )
        if not normal:
            print(executed.stdout)
            print(executed.stderr)
            return executed.returncode or 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
