codes = [-100, 0, 64, 65, 66, 89, 90, 91, 96, 97, 122, 123, 127, 128, 1000]


def is_upper(code):
    return 65 <= code <= 90


def is_lower(code):
    return 97 <= code <= 122


def operational_one_char(code):
    return code if is_upper(code) and not is_lower(code) else 0


def digit_sum_is_step(code):
    return code if is_upper(code) and not is_lower(code) else 0


print("code operational summary equal const0 identity lt90 lowercase")
for code in codes:
    operational = operational_one_char(code)
    summary = digit_sum_is_step(code)
    mutations = [
        0,
        code,
        code if 65 <= code < 90 else 0,
        code if is_lower(code) else 0,
    ]
    print(
        code,
        operational,
        summary,
        operational == summary,
        *(operational == mutation for mutation in mutations),
    )
print(
    "all_exact_matches",
    all(operational_one_char(code) == digit_sum_is_step(code) for code in codes),
)
print(
    "counterfactual_constant_zero_rejected_at_65",
    operational_one_char(65) != 0,
)
print(
    "counterfactual_identity_rejected_at_64",
    operational_one_char(64) != 64,
)
print(
    "counterfactual_lt90_rejected_at_90",
    operational_one_char(90) != (90 if 65 <= 90 < 90 else 0),
)
print(
    "counterfactual_lowercase_rejected_at_97",
    operational_one_char(97) != (97 if is_lower(97) else 0),
)
