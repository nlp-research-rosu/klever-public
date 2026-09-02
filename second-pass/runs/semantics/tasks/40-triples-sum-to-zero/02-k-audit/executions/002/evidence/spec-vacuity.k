requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Reviewer mutation: the real result is hasZeroTriple(VS), so its Boolean
  // complement is false for every satisfying length-three entry state.
  claim <k> #runTriples(
            vCons(A:Int, vCons(B:Int, vCons(C:Int, .ValSeq))))
          => notBool hasZeroTriple(
            vCons(A, vCons(B, vCons(C, .ValSeq)))) ... </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    [label(false-complement)]
endmodule
