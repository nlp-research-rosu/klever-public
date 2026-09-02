requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh auditor mutation: the real execution returns A + B, not A + B + 1.
  // A = 0 and B = 0 is a concrete satisfying witness.
  claim <k>
          runDoAlgebra(
            vCons(plusV, .ValSeq),
            vCons(A:Int, vCons(B:Int, .ValSeq)))
          => (A +Int B) +Int 1
        </k>
        <env> 0 </env>
        <scopes>
          (0 |-> scope(.Map, parent(-1)))
          (-1 |-> builtinsScope)
          => ?FINAL_SCOPES:Map
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    requires A >=Int 0 andBool B >=Int 0
    [label(auditor-false-plus)]
endmodule
