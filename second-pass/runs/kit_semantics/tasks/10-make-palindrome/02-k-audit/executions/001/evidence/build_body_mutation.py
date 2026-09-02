#!/usr/bin/env python3
"""Create a fresh body mutation that changes the term loaded by solutionModule."""

from pathlib import Path


WORK = Path("/tmp/audit-work/candidate-clean")
source = (WORK / "verification.k").read_text(encoding="utf-8")
start_marker = "  rule makePalindromeBody\n"
end_marker = "\n\n  rule isPalindromeClosure"
start = source.index(start_marker)
end = source.index(end_marker, start)
replacement = '  rule makePalindromeBody\n    => Return(Str(""))'
mutated = source[:start] + replacement + source[end:]
(WORK / "verification-body-mutated.k").write_text(mutated, encoding="utf-8")

cat = "iCons(99, iCons(97, iCons(116, .IntSeq)))"
catac = "iCons(99, iCons(97, iCons(116, iCons(97, iCons(99, .IntSeq)))))"
spec = f'''requires "verification-body-mutated.k"

module BODY-MUTATION-GROUND
  imports VERIFICATION

  claim [changed-body-cat]:
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("make_palindrome"), (str({cat}), .Exprs))
      =>
      str({catac})
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> (scope(.Map, parent(-1))
             => scope(
                  "is_palindrome" |-> isPalindromeClosure
                  "make_palindrome" |-> makePalindromeClosure,
                  parent(-1)))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
'''
(WORK / "body-mutation-ground.k").write_text(spec, encoding="utf-8")

assert 'rule makePalindromeBody\n    => Return(Str(""))' in mutated
assert "For(Name(\"char\"), Name(\"string\"), reverseLoopBody)" not in (
    mutated[start : start + len(replacement) + 20]
)
print("mutation=makePalindromeBody now executes Return(Str(\"\"))")
print("executed_term_changed=solutionModule still references mutated makePalindromeBody")
print("false_witness_input=cat expected_original=catac mutated_result=empty")
