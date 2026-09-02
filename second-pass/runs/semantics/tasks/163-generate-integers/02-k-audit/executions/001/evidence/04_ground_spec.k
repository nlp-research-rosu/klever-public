requires "verification.k"

module SPEC-GROUND
  imports VERIFICATION

  // Satisfying witness for the entry precondition: A = 3 and B = 7.
  // The claimed mathematical result is the concrete sequence [4, 6].
  claim
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("generate_integers"), (Int(3), Int(7), .Exprs))
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
      0 |-> list(vCons(4, vCons(6, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
