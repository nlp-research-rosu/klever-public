requires "/tmp/audit-work/verification.k"

module SPEC-WITNESSES
  imports VERIFICATION

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

  claim
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("generate_integers"), (Int(10), Int(14), .Exprs))
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
      0 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("generate_integers"), (Int(8), Int(2), .Exprs))
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
      0 |-> list(vCons(2, vCons(4, vCons(6, vCons(8, .ValSeq)))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
