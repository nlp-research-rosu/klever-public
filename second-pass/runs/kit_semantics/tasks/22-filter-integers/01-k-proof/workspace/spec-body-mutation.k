requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately mutated implementation: it always returns an empty list.
  // The expected result is still the correct result for input [1].
  claim [removed-loop]:
    <k>
      Call(
        Name("filter_integers"),
        (list(vCons(1, .ValSeq)), .Exprs))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "filter_integers" |->
          closureVal(
            ("values", .ParamNames),
            (Assign(Name("result"), ListExpr(.Exprs))
             Return(Name("result"))
             .Stmts),
            0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(1, .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
