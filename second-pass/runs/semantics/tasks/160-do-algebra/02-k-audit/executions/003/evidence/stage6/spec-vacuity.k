requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh reviewer mutation: the real plus result is A + B, not A + B + 1.
  // Ground witness A=4, B=7 satisfies the precondition and gives 11 != 12.
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
    [label(false-plus-off-by-one)]
endmodule
