requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Mutation: the second append uses delimeter instead of number.
  // For input [1] and delimiter 4, the mutated body returns [4], not [1].
  claim [wrong-body-rejected]:
    <k> Call(Name("intersperse"), list(vCons(1, .ValSeq)), 4)
        => ref(0) </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
              "intersperse" |->
                closureVal("numbers", "delimeter", .ParamNames,
                  Assign(Name("result"), ListExpr(.Exprs))
                  For(Name("number"), Name("numbers"),
                    If(Name("result"),
                      Expr(Call(Attribute(Name("result"), "append"),
                                Name("delimeter"))) .Stmts,
                      .Stmts)
                    Expr(Call(Attribute(Name("result"), "append"),
                              Name("delimeter")))
                    .Stmts)
                  Return(Name("result"))
                  .Stmts,
                  0),
              parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(1, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
