import importlib.util
import math
import pathlib
import re
import subprocess
import tempfile


ROOT = pathlib.Path(__file__).resolve().parent


def oracle(n):
    if n < 2:
        return False
    for divisor in range(2, math.isqrt(n) + 1):
        if n % divisor == 0:
            return False
    return True


def load_solution():
    spec = importlib.util.spec_from_file_location("solution", ROOT / "solution.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def k_results(inputs):
    solution_source = (ROOT / "solution.py").read_text(encoding="utf-8")
    all_results = []

    with tempfile.TemporaryDirectory(dir=ROOT) as temp_name:
        temp = pathlib.Path(temp_name)
        for batch_index, start in enumerate(range(0, len(inputs), 100)):
            batch = inputs[start : start + 100]
            calls = ",\n".join(f"    is_prime({n})" for n in batch)
            source = solution_source + f"\n\nresults = [\n{calls},\n]\n"
            program_py = temp / f"differential-{batch_index}.py"
            program_mpy = temp / f"differential-{batch_index}.mpy"
            program_py.write_text(source, encoding="utf-8")

            translated = subprocess.run(
                ["python3", str(ROOT / "py2mpy.py"), str(program_py)],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            )
            program_mpy.write_text(translated.stdout, encoding="utf-8")
            executed = subprocess.run(
                [
                    "krun",
                    str(program_mpy),
                    "--definition",
                    str(ROOT / "runtime-kompiled"),
                ],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            )

            heap_match = re.search(
                r"<heap>\s*0 \|-> list \((.*?)\)\s*</heap>",
                executed.stdout,
                re.DOTALL,
            )
            if heap_match is None:
                raise RuntimeError("could not find result list in krun output")
            all_results.extend(
                token == "true"
                for token in re.findall(r"\b(?:true|false)\b", heap_match.group(1))
            )

    return all_results


def main():
    inputs = list(range(-100, 1001))
    for example in [6, 101, 11, 13441, 61, 4, 1]:
        if example not in inputs:
            inputs.append(example)

    expected = [oracle(n) for n in inputs]
    solution = load_solution()
    cpython_actual = [solution.is_prime(n) for n in inputs]
    k_actual = k_results(inputs)

    cpython_mismatches = [
        (n, actual, wanted)
        for n, actual, wanted in zip(inputs, cpython_actual, expected)
        if actual != wanted
    ]
    k_mismatches = [
        (n, actual, wanted)
        for n, actual, wanted in zip(inputs, k_actual, expected)
        if actual != wanted
    ]

    print(f"inputs={len(inputs)} range=-100..1000 extras=[13441]")
    print(f"cpython_mismatches={len(cpython_mismatches)}")
    print(f"k_mismatches={len(k_mismatches)}")
    if cpython_mismatches or k_mismatches:
        print(f"cpython_details={cpython_mismatches[:10]}")
        print(f"k_details={k_mismatches[:10]}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
