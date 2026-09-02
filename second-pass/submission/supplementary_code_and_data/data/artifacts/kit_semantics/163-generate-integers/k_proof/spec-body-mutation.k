requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  claim [generate-integers]:
    <k>
      Call(Name("generate_integers"), Int(A:Int), Int(B:Int), .Exprs)
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "generate_integers" |->
          closureVal(
            "a", "b", .ParamNames,
            Assign(Name("result"), ListExpr(.Exprs))
            If(
              BoolOp(
                "or",
                BoolOp(
                  "and",
                  Compare(Name("a"), CmpOp("<=", Int(2))),
                  Compare(Int(2), CmpOp("<=", Name("b"))),
                  .Exprs),
                BoolOp(
                  "and",
                  Compare(Name("b"), CmpOp("<=", Int(2))),
                  Compare(Int(2), CmpOp("<=", Name("a"))),
                  .Exprs),
                .Exprs),
              Expr(Call(Attribute(Name("result"), "append"), Int(2), .Exprs)),
              .Stmts)
            If(
              BoolOp(
                "or",
                BoolOp(
                  "and",
                  Compare(Name("a"), CmpOp("<=", Int(4))),
                  Compare(Int(4), CmpOp("<=", Name("b"))),
                  .Exprs),
                BoolOp(
                  "and",
                  Compare(Name("b"), CmpOp("<=", Int(4))),
                  Compare(Int(4), CmpOp("<=", Name("a"))),
                  .Exprs),
                .Exprs),
              Expr(Call(Attribute(Name("result"), "append"), Int(4), .Exprs)),
              .Stmts)
            If(
              BoolOp(
                "or",
                BoolOp(
                  "and",
                  Compare(Name("a"), CmpOp("<=", Int(6))),
                  Compare(Int(6), CmpOp("<=", Name("b"))),
                  .Exprs),
                BoolOp(
                  "and",
                  Compare(Name("b"), CmpOp("<=", Int(6))),
                  Compare(Int(6), CmpOp("<=", Name("a"))),
                  .Exprs),
                .Exprs),
              Expr(Call(Attribute(Name("result"), "append"), Int(6), .Exprs)),
              .Stmts)
            If(
              BoolOp(
                "or",
                BoolOp(
                  "and",
                  Compare(Name("a"), CmpOp("<=", Int(8))),
                  Compare(Int(8), CmpOp("<=", Name("b"))),
                  .Exprs),
                BoolOp(
                  "and",
                  Compare(Name("b"), CmpOp("<=", Int(8))),
                  Compare(Int(8), CmpOp("<=", Name("a"))),
                  .Exprs),
                .Exprs),
              Expr(Call(Attribute(Name("result"), "append"), Int(7), .Exprs)),
              .Stmts)
            Return(Name("result"))
            .Stmts,
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(expectedDigits(A, B)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires A >Int 0 andBool B >Int 0
endmodule
