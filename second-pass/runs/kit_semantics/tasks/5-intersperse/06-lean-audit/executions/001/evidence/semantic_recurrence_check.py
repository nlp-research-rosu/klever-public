#!/usr/bin/env python3
"""Independent executable check of the frozen recurrence against loop behavior."""

import itertools
import json


def operational_continuation(acc, rest, delimiter):
    """Behavior induced by If(result), two list.append calls, and list truthiness."""
    result = list(acc)
    for number in rest:
        if result:
            result.append(delimiter)
        result.append(number)
    return result


def frozen_summary(acc, rest, delimiter):
    """The three intersperseAcc clauses from frozen verification.k."""
    if not rest:
        return list(acc)
    head, *tail = rest
    if not acc:
        return frozen_summary([head], tail, delimiter)
    return frozen_summary(list(acc) + [delimiter] + [head], tail, delimiter)


def omit_delimiter_mutation(acc, rest, delimiter):
    result = list(acc)
    for number in rest:
        result.append(number)
    return result


def always_delimiter_mutation(acc, rest, delimiter):
    result = list(acc)
    for number in rest:
        result.extend([delimiter, number])
    return result


def post_delimiter_mutation(acc, rest, delimiter):
    result = list(acc)
    for number in rest:
        result.extend([number, delimiter])
    return result


values = [-1, 0, 2]
delimiter = 9
cases = []
for acc_len in range(3):
    for rest_len in range(4):
        for acc in itertools.product(values, repeat=acc_len):
            for rest in itertools.product(values, repeat=rest_len):
                cases.append((list(acc), list(rest), delimiter))

mismatches = []
for acc, rest, delim in cases:
    operational = operational_continuation(acc, rest, delim)
    summary = frozen_summary(acc, rest, delim)
    if operational != summary:
        mismatches.append(
            {
                "acc": acc,
                "rest": rest,
                "delimiter": delim,
                "operational": operational,
                "summary": summary,
            }
        )

mutations = {
    "constant_empty": lambda _acc, _rest, _delimiter: [],
    "identity_acc": lambda acc, _rest, _delimiter: list(acc),
    "identity_rest": lambda _acc, rest, _delimiter: list(rest),
    "omit_delimiter": omit_delimiter_mutation,
    "always_delimiter": always_delimiter_mutation,
    "append_delimiter_after_number": post_delimiter_mutation,
}
mutation_results = {}
for name, mutation in mutations.items():
    failures = []
    for acc, rest, delim in cases:
        expected = operational_continuation(acc, rest, delim)
        observed = mutation(acc, rest, delim)
        if expected != observed:
            failures.append(
                {
                    "acc": acc,
                    "rest": rest,
                    "delimiter": delim,
                    "expected": expected,
                    "mutated": observed,
                }
            )
    mutation_results[name] = {
        "mismatch_count": len(failures),
        "first_witness": failures[0] if failures else None,
    }

explicit_witnesses = [
    {
        "acc": acc,
        "rest": rest,
        "delimiter": delim,
        "operational": operational_continuation(acc, rest, delim),
        "summary": frozen_summary(acc, rest, delim),
    }
    for acc, rest, delim in [
        ([], [], 4),
        ([], [1], 4),
        ([], [1, 2, 3], 4),
        ([8], [1, 2], 4),
        ([8, 7], [1], 4),
    ]
]

print(
    json.dumps(
        {
            "semantic_sources": {
                "truthiness": (
                    "core.k: truthy(list(V)) is true iff V is nonempty"
                ),
                "if": "controls.k: If selects by truthy(condition)",
                "append": (
                    "list.k: append writes valSeqConcat(VS, vCons(V,.ValSeq))"
                ),
                "loop": (
                    "controls.k/list.k: list iteration yields each element in order"
                ),
            },
            "tested_case_count": len(cases),
            "frozen_summary_mismatch_count": len(mismatches),
            "frozen_summary_first_mismatch": mismatches[0] if mismatches else None,
            "explicit_witnesses": explicit_witnesses,
            "counterfactual_mutations": mutation_results,
        },
        indent=2,
        sort_keys=True,
    )
)
