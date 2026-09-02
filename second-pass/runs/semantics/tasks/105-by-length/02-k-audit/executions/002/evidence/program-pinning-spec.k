requires "verification.k"

module PROGRAM-PINNING-SPEC
  imports BY-LENGTH-VERIFICATION

  claim [body-constructor-identity]:
    <k>
      byLengthBody
    =>
Assign(
      Name("names"),
      ListExpr(
        Str("One"),
        Str("Two"),
        Str("Three"),
        Str("Four"),
        Str("Five"),
        Str("Six"),
        Str("Seven"),
        Str("Eight"),
        Str("Nine")))
    Assign(Name("values"), ListExpr(.Exprs))
    For(Name("value"), Name("arr"),
      If(BoolOp(
        "and",
        Compare(Name("value"), CmpOp(">=", Int(1))),
        Compare(Name("value"), CmpOp("<=", Int(9)))),
        Expr(Call(Attribute(Name("values"), "append"), Name("value"))),
        .Stmts))
    Assign(
      Name("values"),
      Call(Name("sorted"), Name("values"), KwArg("reverse", Bool(true))))
    Assign(Name("result"), ListExpr(.Exprs))
    For(Name("value"), Name("values"),
      Expr(
        Call(
          Attribute(Name("result"), "append"),
          Subscript(Name("names"), BinOp("-", Name("value"), Int(1))))))
    Return(Name("result"))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [closure-constructor-identity]:
    <k>
      byLengthClosure
    =>
      closureVal("arr", Assign(
      Name("names"),
      ListExpr(
        Str("One"),
        Str("Two"),
        Str("Three"),
        Str("Four"),
        Str("Five"),
        Str("Six"),
        Str("Seven"),
        Str("Eight"),
        Str("Nine")))
    Assign(Name("values"), ListExpr(.Exprs))
    For(Name("value"), Name("arr"),
      If(BoolOp(
        "and",
        Compare(Name("value"), CmpOp(">=", Int(1))),
        Compare(Name("value"), CmpOp("<=", Int(9)))),
        Expr(Call(Attribute(Name("values"), "append"), Name("value"))),
        .Stmts))
    Assign(
      Name("values"),
      Call(Name("sorted"), Name("values"), KwArg("reverse", Bool(true))))
    Assign(Name("result"), ListExpr(.Exprs))
    For(Name("value"), Name("values"),
      Expr(
        Call(
          Attribute(Name("result"), "append"),
          Subscript(Name("names"), BinOp("-", Name("value"), Int(1))))))
    Return(Name("result")), 0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

endmodule
