requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: a realizably positive singleton is claimed to
  // produce an empty list.
  claim [false-result]:
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
      ~> Call(
           Name("get_positive"),
           list(vCons(I:Int, .ValSeq)))
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
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires positiveNumeric(I)
endmodule
