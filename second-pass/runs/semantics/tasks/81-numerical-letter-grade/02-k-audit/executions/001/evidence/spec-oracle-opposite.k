requires "verification.k"

module SPEC-ORACLE-OPPOSITE
  imports VERIFICATION

  // In the candidate theory, gpaEqFour is unconstrained.  This interpretation
  // makes the equality test false at the real input 4.0.  The bridge then
  // permits the actual function body to return "A" instead of Python's "A+".
  claim [wrong-result-at-four-is-provable]:
    <k> runGrades(vCons(F:Float, .ValSeq)) => ref(0) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map
      => 0 |-> list(vCons(letter("A"), .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    requires notBool gpaEqFour(F)
             andBool above(F, 3.7)

endmodule
