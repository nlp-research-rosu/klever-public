requires "/tmp/audit-work/verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the real result for (2, 8) includes the final digit 8.
  claim
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("generate_integers"), (Int(2), Int(8), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      ( 0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope
      )
      =>
      ( 0  |-> scope(
                  "generate_integers" |-> generateIntegersClosure,
                  parent(-1)
                )
        -1 |-> builtinsScope
      )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(2, vCons(4, vCons(6, .ValSeq))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
