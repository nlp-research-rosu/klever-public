requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim [false-result-has-trailing-ten]:
   <py>
    <k>
      Module(
        FuncDef("generate_integers", Params("a", "b"),
          Assign(Name("result"), ListExpr(.Exprs))
          If(Compare(Name("a"), CmpOp("<=", Name("b"))),
            If(Compare(Name("a"), CmpOp("<=", Int(2))),
              If(Compare(Int(2), CmpOp("<=", Name("b"))),
                Assign(
                  Name("result"),
                  BinOp("+", Name("result"), ListExpr(Int(2)))),
                .Stmts),
              .Stmts)
            If(Compare(Name("a"), CmpOp("<=", Int(4))),
              If(Compare(Int(4), CmpOp("<=", Name("b"))),
                Assign(
                  Name("result"),
                  BinOp("+", Name("result"), ListExpr(Int(4)))),
                .Stmts),
              .Stmts)
            If(Compare(Name("a"), CmpOp("<=", Int(6))),
              If(Compare(Int(6), CmpOp("<=", Name("b"))),
                Assign(
                  Name("result"),
                  BinOp("+", Name("result"), ListExpr(Int(6)))),
                .Stmts),
              .Stmts)
            If(Compare(Name("a"), CmpOp("<=", Int(8))),
              If(Compare(Int(8), CmpOp("<=", Name("b"))),
                Assign(
                  Name("result"),
                  BinOp("+", Name("result"), ListExpr(Int(8)))),
                .Stmts),
              .Stmts),
            If(Compare(Name("b"), CmpOp("<=", Int(2))),
              If(Compare(Int(2), CmpOp("<=", Name("a"))),
                Assign(
                  Name("result"),
                  BinOp("+", Name("result"), ListExpr(Int(2)))),
                .Stmts),
              .Stmts)
            If(Compare(Name("b"), CmpOp("<=", Int(4))),
              If(Compare(Int(4), CmpOp("<=", Name("a"))),
                Assign(
                  Name("result"),
                  BinOp("+", Name("result"), ListExpr(Int(4)))),
                .Stmts),
              .Stmts)
            If(Compare(Name("b"), CmpOp("<=", Int(6))),
              If(Compare(Int(6), CmpOp("<=", Name("a"))),
                Assign(
                  Name("result"),
                  BinOp("+", Name("result"), ListExpr(Int(6)))),
                .Stmts),
              .Stmts)
            If(Compare(Name("b"), CmpOp("<=", Int(8))),
              If(Compare(Int(8), CmpOp("<=", Name("a"))),
                Assign(
                  Name("result"),
                  BinOp("+", Name("result"), ListExpr(Int(8)))),
                .Stmts),
              .Stmts))
          Return(Name("result"))))
      => .K
    </k>
    <input> pair(A, B) </input>
    <env> .Map =>
      "a" |-> intVal(A)
      "b" |-> intVal(B)
      "result" |-> listVal(expected(A, B))
    </env>
    <result>
      noResult => listVal(expected(A, B) ListItem(10))
    </result>
   </py>
  requires A >Int 0 andBool B >Int 0
endmodule
