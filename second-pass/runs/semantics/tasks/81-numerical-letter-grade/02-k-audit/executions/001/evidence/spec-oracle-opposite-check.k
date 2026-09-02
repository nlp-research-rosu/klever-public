requires "verification.k"

module SPEC-ORACLE-OPPOSITE-CHECK
  imports VERIFICATION

  // Same satisfiable interpretation as spec-oracle-opposite.k, but demand the
  // real Python result.  It must fail because the candidate bridge took "A".
  claim [real-result-is-rejected-under-opposite-interpretation]:
    <k> runGrades(vCons(F:Float, .ValSeq)) => ref(0) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map
      => 0 |-> list(vCons(letter("A+"), .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    requires notBool gpaEqFour(F)
             andBool above(F, 3.7)

endmodule
