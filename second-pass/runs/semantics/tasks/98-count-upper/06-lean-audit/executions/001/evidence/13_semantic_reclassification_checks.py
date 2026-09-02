#!/usr/bin/env python3
import itertools
import json

VOWEL_CODES = (65, 69, 73, 79, 85)


def count_upper_from(codes: tuple[int, ...], even: bool) -> int:
    if not codes:
        return 0
    current = 1 if even and codes[0] in VOWEL_CODES else 0
    return current + count_upper_from(codes[1:], not even)


def operational_scan(codes: tuple[int, ...], initial_even: bool) -> int:
    count = 0
    even = initial_even
    for code in codes:
        member = code in VOWEL_CODES
        bool_value = even and member
        count += 1 if bool_value else 0
        even = not even
    return count


alphabet = (65, 66, 69, 97, 85, 937)
cases = [
    (),
    (65,),
    (66, 65),
    (65, 66, 69),
    (97, 65, 937, 85),
    VOWEL_CODES,
]
cases.extend(
    sequence
    for length in range(5)
    for sequence in itertools.product(alphabet, repeat=length)
)

mismatches = []
for codes in cases:
    for even in (False, True):
        summary = count_upper_from(tuple(codes), even)
        operational = operational_scan(tuple(codes), even)
        if summary != operational:
            mismatches.append(
                {
                    "codes": codes,
                    "even": even,
                    "summary": summary,
                    "operational": operational,
                }
            )


def constant_zero(codes: tuple[int, ...]) -> int:
    return 0


def all_indices(codes: tuple[int, ...]) -> int:
    return sum(code in VOWEL_CODES for code in codes)


def toggle_before(codes: tuple[int, ...]) -> int:
    count = 0
    even = True
    for code in codes:
        even = not even
        count += int(even and code in VOWEL_CODES)
    return count


def include_lowercase(codes: tuple[int, ...]) -> int:
    extended = VOWEL_CODES + (97, 101, 105, 111, 117)
    return sum(index % 2 == 0 and code in extended for index, code in enumerate(codes))


mutations = {
    "constant_zero": constant_zero,
    "count_all_indices": all_indices,
    "toggle_before": toggle_before,
    "include_lowercase": include_lowercase,
}
mutation_mismatches = {
    name: sum(
        implementation(tuple(codes)) != operational_scan(tuple(codes), True)
        for codes in cases
    )
    for name, implementation in mutations.items()
}

result = {
    "status": "PASS" if not mismatches else "FAIL",
    "checked_sequences": len(cases),
    "checked_initial_parities": 2,
    "comparison_count": len(cases) * 2,
    "mismatches": mismatches,
    "counterfactual_mutation_mismatch_counts": mutation_mismatches,
    "adversarial_examples": [
        {
            "codes": list(codes),
            "operational_result": operational_scan(tuple(codes), True),
            "summary_result": count_upper_from(tuple(codes), True),
        }
        for codes in [
            (),
            (65,),
            (66, 65),
            (65, 66, 69),
            (97, 65, 937, 85),
            VOWEL_CODES,
        ]
    ],
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if not mismatches else 1)
