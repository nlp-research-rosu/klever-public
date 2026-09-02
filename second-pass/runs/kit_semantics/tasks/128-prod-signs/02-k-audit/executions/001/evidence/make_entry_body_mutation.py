#!/usr/bin/env python3
"""Ground the entry claim at [1] and mutate its executed body: seen=1 -> 0."""

from pathlib import Path


source = Path("/tmp/audit-work/128-prod-signs/spec.k").read_text()
entry_start = source.index("  claim [prod-signs]:")
entry_end = source.rindex("endmodule")
entry = source[entry_start:entry_end]

needle = 'Assign(Name("seen"), Int(1))'
assert entry.count(needle) == 2  # loaded body and expected closure body
entry = entry.replace(needle, 'Assign(Name("seen"), Int(0))')

input_needle = "list(intVals(INPUT:IntSeq))"
assert entry.count(input_needle) == 1
entry = entry.replace(input_needle, "list(intVals(iCons(1, .IntSeq)))")

result_needle = "prodSignsResult(INPUT)"
assert entry.count(result_needle) == 1
entry = entry.replace(
    result_needle,
    "prodSignsResult(iCons(1, .IntSeq))",
)
entry = entry.replace(
    "claim [prod-signs]:",
    "claim [auditor-mutated-entry-body]:",
    1,
)

mutated = (
    'requires "verification.k"\n\n'
    "module AUDITOR-BODY-MUTATION-SPEC\n"
    "  imports VERIFICATION\n\n"
    f"{entry}"
    "endmodule\n"
)

scratch = Path("/tmp/audit-work/128-prod-signs/auditor-body-mutation-spec.k")
evidence = Path("/audit-output/evidence/auditor-body-mutation-spec.k")
scratch.write_text(mutated)
evidence.write_text(mutated)

print(f"SCRATCH_MUTATION={scratch}")
print(f"PRESERVED_MUTATION={evidence}")
print("EXECUTED_TERM_MUTATION=two_loaded_closure_body_occurrences_seen_1_to_0")
print("GROUND_INPUT=[1] ORIGINAL_RESULT=1 MUTATED_PROGRAM_RESULT=None")
