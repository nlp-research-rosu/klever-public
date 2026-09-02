requires "verification.k"

module FRESH-FALSE-MUTATION
  imports VERIFICATION

  // Satisfiable input [1, 2], delimiter 4. The real result is [1, 4, 2].
  // This mutation deliberately swaps the two input elements.
  claim [swapped-result-must-fail]:
    <k> Call(Name("intersperse"),
             list(vCons(1, vCons(2, .ValSeq))), 4)
        => ref(0) </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
              "intersperse" |->
                closureVal("numbers", "delimeter", .ParamNames,
                  Assign(Name("result"), ListExpr(.Exprs))
                  For(Name("number"), Name("numbers"), INTERSPERSE-BODY)
                  Return(Name("result"))
                  .Stmts,
                  0),
              parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map => 0 |-> list(vCons(2, vCons(4, vCons(1, .ValSeq))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
