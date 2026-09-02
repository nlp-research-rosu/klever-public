#!/usr/bin/env python3
"""Create reviewer-authored false-result and body-sensitivity K specs."""

from pathlib import Path


source_path = Path("/tmp/audit-work/reconstruction/spec.k")
source = source_path.read_text(encoding="utf-8")

false_result = source.replace("module SPEC\n", "module AUDIT-FALSE-RESULT\n", 1)
old_post = "=> searchSummary(INPUT, INPUT, -1) ~> .K"
new_post = "=> 0 ~> .K"
if false_result.count(old_post) != 1:
    raise SystemExit("unexpected whole-program postcondition count")
false_result = false_result.replace(old_post, new_post, 1)
old_pre = "requires INPUT =/=K .ValSeq andBool allPositive(INPUT)"
new_pre = (
    "requires INPUT ==K vCons(1, .ValSeq) andBool allPositive(INPUT)"
)
if false_result.count(old_pre) != 1:
    raise SystemExit("unexpected whole-program precondition count")
false_result = false_result.replace(old_pre, new_pre, 1)
false_output = Path("/audit-output/evidence/audit_false_result.k")
false_output.write_text(false_result, encoding="utf-8")

body_mutation = source.replace("module SPEC\n", "module AUDIT-BODY-MUTATION\n", 1)
old_compare = 'CmpOp(">=", Name("candidate")))'
new_compare = 'CmpOp(">", Name("candidate")))'
head, separator, tail = body_mutation.rpartition(old_compare)
if not separator or old_compare in tail:
    raise SystemExit("could not isolate last >= comparison")
body_mutation = head + new_compare + tail
body_output = Path("/audit-output/evidence/audit_body_mutation.k")
body_output.write_text(body_mutation, encoding="utf-8")

print(f"false_result={false_output}")
print("false_result_witness=[1], actual=1, mutated_target=0")
print(f"body_mutation={body_output}")
print("body_mutation_witness=[1], original=1, mutated=-1")
