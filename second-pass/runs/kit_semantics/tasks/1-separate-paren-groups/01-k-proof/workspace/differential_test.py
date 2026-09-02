"""Independent finite oracle for the HumanEval contract.

The oracle constructs balanced groups from the grammar
    group := "(" group* ")"
and therefore knows the expected top-level partition before rendering the
input or injecting spaces.
"""

import ast
from itertools import product
from pathlib import Path

from solution import separate_paren_groups


def translated_function_source_matches():
    def target_function(path):
        tree = ast.parse(Path(path).read_text(encoding="utf-8"))
        return next(node for node in tree.body
                    if isinstance(node, ast.FunctionDef)
                    and node.name == "separate_paren_groups")

    return ast.dump(target_function("solution.py"), include_attributes=False) == (
        ast.dump(target_function("concrete-tests.py"), include_attributes=False)
    )


def groups_with_pairs(pairs):
    if pairs == 1:
        return {"()"}

    result = set()

    def inner_sequences(remaining):
        if remaining == 0:
            return {()}
        sequences = set()
        for first_size in range(1, remaining + 1):
            for first in groups_with_pairs(first_size):
                for rest in inner_sequences(remaining - first_size):
                    sequences.add((first,) + rest)
        return sequences

    for children in inner_sequences(pairs - 1):
        result.add("(" + "".join(children) + ")")
    return result


def top_level_sequences(max_pairs):
    yield ()
    for total_pairs in range(1, max_pairs + 1):
        for sizes_length in range(1, total_pairs + 1):
            for sizes in product(range(1, total_pairs + 1), repeat=sizes_length):
                if sum(sizes) != total_pairs:
                    continue
                choices = [sorted(groups_with_pairs(size)) for size in sizes]
                yield from product(*choices)


def spaced_variants(text):
    yield text
    yield " ".join(text)
    yield "  " + text + "   "
    yield "".join((" " if index % 2 == 0 else "") + char
                  for index, char in enumerate(text))
    yield "".join(char + ("  " if index % 3 == 0 else "")
                  for index, char in enumerate(text))


checked = 0
mismatches = []
for expected_tuple in top_level_sequences(5):
    expected = list(expected_tuple)
    compact = "".join(expected)
    for source in spaced_variants(compact):
        checked += 1
        actual = separate_paren_groups(source)
        if actual != expected:
            mismatches.append((source, expected, actual))

print(f"DIFFERENTIAL_CASES={checked}")
print(f"MISMATCHES={len(mismatches)}")
print(f"CONCRETE_SOURCE_BODY_MATCH={translated_function_source_matches()}")
if mismatches:
    raise AssertionError(mismatches[:5])
if not translated_function_source_matches():
    raise AssertionError("concrete-tests.py drifted from solution.py")
