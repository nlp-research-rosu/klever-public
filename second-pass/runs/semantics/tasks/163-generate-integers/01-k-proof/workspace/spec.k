requires "verification.k"

module SPEC
  imports VERIFICATION

  claim
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("generate_integers"), (Int(A), Int(B), .Exprs))
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
      0 |-> list(evenDigits(A, B))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires A >Int 0 andBool B >Int 0
endmodule
