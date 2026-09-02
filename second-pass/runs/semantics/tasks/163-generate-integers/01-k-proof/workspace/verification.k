requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The exact statement body emitted in solution.mpy.
  syntax Stmts ::= "generateIntegersBody" [macro]
  rule generateIntegersBody =>
    Assign(Name("result"), ListExpr(.Exprs))
    If(
      BoolOp(
        "or",
        ( BoolOp(
            "and",
            ( Compare(Name("a"), CmpOp("<=", Int(2))),
              Compare(Int(2), CmpOp("<=", Name("b"))),
              .Exprs
            )
          ),
          BoolOp(
            "and",
            ( Compare(Name("b"), CmpOp("<=", Int(2))),
              Compare(Int(2), CmpOp("<=", Name("a"))),
              .Exprs
            )
          ),
          .Exprs
        )
      ),
      Expr(Call(Attribute(Name("result"), "append"), (Int(2), .Exprs))),
      .Stmts
    )
    If(
      BoolOp(
        "or",
        ( BoolOp(
            "and",
            ( Compare(Name("a"), CmpOp("<=", Int(4))),
              Compare(Int(4), CmpOp("<=", Name("b"))),
              .Exprs
            )
          ),
          BoolOp(
            "and",
            ( Compare(Name("b"), CmpOp("<=", Int(4))),
              Compare(Int(4), CmpOp("<=", Name("a"))),
              .Exprs
            )
          ),
          .Exprs
        )
      ),
      Expr(Call(Attribute(Name("result"), "append"), (Int(4), .Exprs))),
      .Stmts
    )
    If(
      BoolOp(
        "or",
        ( BoolOp(
            "and",
            ( Compare(Name("a"), CmpOp("<=", Int(6))),
              Compare(Int(6), CmpOp("<=", Name("b"))),
              .Exprs
            )
          ),
          BoolOp(
            "and",
            ( Compare(Name("b"), CmpOp("<=", Int(6))),
              Compare(Int(6), CmpOp("<=", Name("a"))),
              .Exprs
            )
          ),
          .Exprs
        )
      ),
      Expr(Call(Attribute(Name("result"), "append"), (Int(6), .Exprs))),
      .Stmts
    )
    If(
      BoolOp(
        "or",
        ( BoolOp(
            "and",
            ( Compare(Name("a"), CmpOp("<=", Int(8))),
              Compare(Int(8), CmpOp("<=", Name("b"))),
              .Exprs
            )
          ),
          BoolOp(
            "and",
            ( Compare(Name("b"), CmpOp("<=", Int(8))),
              Compare(Int(8), CmpOp("<=", Name("a"))),
              .Exprs
            )
          ),
          .Exprs
        )
      ),
      Expr(Call(Attribute(Name("result"), "append"), (Int(8), .Exprs))),
      .Stmts
    )
    Return(Name("result"))

  syntax Module ::= "solutionModule" [macro]
  rule solutionModule =>
    Module(
      FuncDef(
        "generate_integers",
        Params("a", "b"),
        generateIntegersBody
      )
    )

  syntax Val ::= "generateIntegersClosure" [macro]
  rule generateIntegersClosure =>
    closureVal(("a", "b"), generateIntegersBody, 0)

  // Mathematical result: retain each even decimal digit exactly when it lies
  // in the inclusive interval whose endpoints are A and B.
  syntax Bool ::= betweenEndpoints(Int, Int, Int) [function, total]
  rule betweenEndpoints(A, B, D) =>
    (A <=Int D andBool D <=Int B)
      orBool (B <=Int D andBool D <=Int A)

  syntax ValSeq ::= keepDigit(Bool, Int, ValSeq) [function, total]
  rule keepDigit(true,  D, REST) => vCons(D, REST)
  rule keepDigit(false, _, REST) => REST

  syntax ValSeq ::= evenDigits(Int, Int) [function, total]
  rule evenDigits(A, B) =>
    keepDigit(
      betweenEndpoints(A, B, 2),
      2,
      keepDigit(
        betweenEndpoints(A, B, 4),
        4,
        keepDigit(
          betweenEndpoints(A, B, 6),
          6,
          keepDigit(
            betweenEndpoints(A, B, 8),
            8,
            .ValSeq
          )
        )
      )
    )
endmodule
