requires "/audit-output/evidence/verification-body-mutation.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION-BODY-MUTATION

  claim
    <k>
      #loadAll(mutatedSolutionModule)
      ~> Call(Name("generate_integers"), (Int(8), Int(8), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      ( 0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope
      )
      =>
      ( 0  |-> scope(
                  "generate_integers" |-> mutatedGenerateIntegersClosure,
                  parent(-1)
                )
        -1 |-> builtinsScope
      )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(8, .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
