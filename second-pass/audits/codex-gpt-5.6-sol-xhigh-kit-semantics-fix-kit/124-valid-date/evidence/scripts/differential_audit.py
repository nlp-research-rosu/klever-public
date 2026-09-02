#!/usr/bin/env python3
"""Independent candidate/canonical differential test for HumanEval 124."""

import argparse
import importlib.util
import json
import random
import string


def load_entry(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.valid_date


DAYS = {
    1: 31,
    2: 29,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}


def prompt_oracle(value):
    """Literal contract: exactly ASCII mm-dd-yyyy with the stated bounds."""
    if len(value) != 10 or value[2] != "-" or value[5] != "-":
        return False
    digit_positions = (0, 1, 3, 4, 6, 7, 8, 9)
    if any(value[index] not in string.digits for index in digit_positions):
        return False
    month = int(value[:2])
    day = int(value[3:5])
    return month in DAYS and 1 <= day <= DAYS[month]


def build_cases():
    cases = {}

    def add(value, category):
        cases.setdefault(value, set()).add(category)

    examples = (
        "03-11-2000",
        "15-01-2012",
        "04-0-2040",
        "06-04-2020",
        "06/04/2020",
    )
    for value in examples:
        add(value, "documented-example")

    for value in (
        "",
        "-",
        "00-00-0000",
        "01-01-0000",
        "01-29-2000",
        "01-30-2000",
        "01-31-2000",
        "01-32-2000",
        "02-00-2000",
        "02-01-2000",
        "02-28-2000",
        "02-29-2000",
        "02-30-2000",
        "03-31-2000",
        "04-29-2000",
        "04-30-2000",
        "04-31-2000",
        "06-30-2000",
        "06-31-2000",
        "11-30-2000",
        "11-31-2000",
        "12-31-9999",
        "12-32-9999",
        "13-01-2000",
        "99-99-9999",
        "03-11-200",
        "03-11-20000",
        "3-11-2000",
        "03-1-2000",
        " 03-11-2000",
        "03-11-2000 ",
        "\t03-11-2000\n",
        "+3-11-2000",
        "03-11-+2000",
        "٠٣-١١-٢٠٠٠",
        "０３-１１-２０００",
    ):
        add(value, "empty-or-boundary")

    for year in ("0000", "2000", "9999"):
        for month in range(100):
            for day in range(100):
                add(f"{month:02d}-{day:02d}-{year}", "exhaustive-month-day")

    seed = "03-11-2000"
    for index in range(len(seed)):
        for code in range(32, 127):
            add(seed[:index] + chr(code) + seed[index + 1 :], "printable-single-mutation")

    rng = random.Random(124)
    alphabet = string.ascii_letters + string.digits + "-/+ _\t\n"
    for _ in range(5000):
        length = rng.randrange(0, 17)
        add("".join(rng.choice(alphabet) for _ in range(length)), "seeded-generated-ascii")

    unicode_alphabet = "٠١٢٣٤٥٦٧٨٩０１２３４５６７８９- /"
    for _ in range(1000):
        length = rng.randrange(0, 14)
        add("".join(rng.choice(unicode_alphabet) for _ in range(length)), "seeded-generated-unicode")

    return sorted((value, sorted(categories)) for value, categories in cases.items())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", required=True)
    parser.add_argument("--generated", required=True)
    parser.add_argument("--inputs-out", required=True)
    parser.add_argument("--results-out", required=True)
    args = parser.parse_args()

    canonical = load_entry("trusted_canonical_124", args.canonical)
    generated = load_entry("generated_solution_124", args.generated)
    cases = build_cases()

    with open(args.inputs_out, "w", encoding="utf-8") as stream:
        json.dump(
            [{"input": value, "categories": categories} for value, categories in cases],
            stream,
            ensure_ascii=True,
            indent=2,
        )
        stream.write("\n")

    canonical_generated = []
    canonical_prompt = []
    generated_prompt = []
    for value, categories in cases:
        canonical_result = canonical(value)
        generated_result = generated(value)
        prompt_result = prompt_oracle(value)
        record = {
            "input": value,
            "categories": categories,
            "canonical": canonical_result,
            "generated": generated_result,
            "prompt_oracle": prompt_result,
        }
        if canonical_result != generated_result:
            canonical_generated.append(record)
        if canonical_result != prompt_result:
            canonical_prompt.append(record)
        if generated_result != prompt_result:
            generated_prompt.append(record)

    print(f"cases={len(cases)}")
    print(f"canonical_generated_mismatches={len(canonical_generated)}")
    print(f"canonical_prompt_mismatches={len(canonical_prompt)}")
    print(f"generated_prompt_mismatches={len(generated_prompt)}")
    print("canonical_generated_first_30=")
    for record in canonical_generated[:30]:
        print(json.dumps(record, ensure_ascii=True, sort_keys=True))

    with open(args.results_out, "w", encoding="utf-8") as stream:
        json.dump(
            {
                "case_count": len(cases),
                "canonical_generated_mismatches": canonical_generated,
                "canonical_prompt_mismatches": canonical_prompt,
                "generated_prompt_mismatches": generated_prompt,
            },
            stream,
            ensure_ascii=True,
            indent=2,
            sort_keys=True,
        )
        stream.write("\n")

    raise SystemExit(1 if canonical_generated or generated_prompt else 0)


if __name__ == "__main__":
    main()
