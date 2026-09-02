requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [filter-loop]:
    <k>
      #loop(
        list(VS:ValSeq),
        Name("x"),
        If(
          Compare(Name("x"), CmpOp(">", Float(0.0))),
          Expr(Call(Attribute(Name("positive"), "append"), Name("x"))),
          .Stmts))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |->
        scope(
          "l" |-> INPUT:Val
          "positive" |-> ref(H)
          "x" |-> (X:Val => ?X:Val),
          parent(0))
      ...
    </scopes>
    <heap>
      ...
      H:Int |-> list(ACC:ValSeq => filterPositive(ACC, VS))
      ...
    </heap>
    requires numericVals(VS)

  claim [get-positive]:
    <k>
      FuncDef(
        "get_positive",
        Params("l"),
        Expr(Str("Return only positive numbers in the list."))
        Assign(Name("positive"), ListExpr(.Exprs))
        Assign(Name("x"), Int(0))
        For(
          Name("x"),
          Name("l"),
          If(
            Compare(Name("x"), CmpOp(">", Float(0.0))),
            Expr(Call(Attribute(Name("positive"), "append"), Name("x"))),
            .Stmts))
        Return(Name("positive")))
      ~> Call(Name("get_positive"), list(VS:ValSeq))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "get_positive" |->
             closureVal(
               "l",
               Expr(Str("Return only positive numbers in the list."))
               Assign(Name("positive"), ListExpr(.Exprs))
               Assign(Name("x"), Int(0))
               For(
                 Name("x"),
                 Name("l"),
                 If(
                   Compare(Name("x"), CmpOp(">", Float(0.0))),
                   Expr(Call(Attribute(Name("positive"), "append"), Name("x"))),
                   .Stmts))
               Return(Name("positive")),
               0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map => 0 |-> list(filterPositive(.ValSeq, VS))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires numericVals(VS)
endmodule
