requires "semantic.k"

module SOLUTION-PROGRAM
  imports MPY-SYNTAX

  syntax Program ::= "solutionProgram"
  rule solutionProgram =>
    Module(
      FuncDef("bf", Params("planet1", "planet2"),
        If(Compare(Name("planet1"), CmpOp("==", Str("Mercury"))),
          If(Compare(Name("planet2"), CmpOp("==", Str("Earth"))),
            Return(TupleExpr(Str("Venus"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Mars"))),
            Return(TupleExpr(Str("Venus"), Str("Earth"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Jupiter"))),
            Return(TupleExpr(Str("Venus"), Str("Earth"), Str("Mars"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Saturn"))),
            Return(
              TupleExpr(
                Str("Venus"),
                Str("Earth"),
                Str("Mars"),
                Str("Jupiter"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Uranus"))),
            Return(
              TupleExpr(
                Str("Venus"),
                Str("Earth"),
                Str("Mars"),
                Str("Jupiter"),
                Str("Saturn"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Neptune"))),
            Return(
              TupleExpr(
                Str("Venus"),
                Str("Earth"),
                Str("Mars"),
                Str("Jupiter"),
                Str("Saturn"),
                Str("Uranus"))),
            .Stmts)
          Return(TupleExpr(.Exprs)),
          .Stmts)
        If(Compare(Name("planet1"), CmpOp("==", Str("Venus"))),
          If(Compare(Name("planet2"), CmpOp("==", Str("Mars"))),
            Return(TupleExpr(Str("Earth"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Jupiter"))),
            Return(TupleExpr(Str("Earth"), Str("Mars"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Saturn"))),
            Return(TupleExpr(Str("Earth"), Str("Mars"), Str("Jupiter"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Uranus"))),
            Return(
              TupleExpr(
                Str("Earth"),
                Str("Mars"),
                Str("Jupiter"),
                Str("Saturn"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Neptune"))),
            Return(
              TupleExpr(
                Str("Earth"),
                Str("Mars"),
                Str("Jupiter"),
                Str("Saturn"),
                Str("Uranus"))),
            .Stmts)
          Return(TupleExpr(.Exprs)),
          .Stmts)
        If(Compare(Name("planet1"), CmpOp("==", Str("Earth"))),
          If(Compare(Name("planet2"), CmpOp("==", Str("Mercury"))),
            Return(TupleExpr(Str("Venus"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Jupiter"))),
            Return(TupleExpr(Str("Mars"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Saturn"))),
            Return(TupleExpr(Str("Mars"), Str("Jupiter"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Uranus"))),
            Return(TupleExpr(Str("Mars"), Str("Jupiter"), Str("Saturn"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Neptune"))),
            Return(
              TupleExpr(
                Str("Mars"),
                Str("Jupiter"),
                Str("Saturn"),
                Str("Uranus"))),
            .Stmts)
          Return(TupleExpr(.Exprs)),
          .Stmts)
        If(Compare(Name("planet1"), CmpOp("==", Str("Mars"))),
          If(Compare(Name("planet2"), CmpOp("==", Str("Mercury"))),
            Return(TupleExpr(Str("Venus"), Str("Earth"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Venus"))),
            Return(TupleExpr(Str("Earth"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Saturn"))),
            Return(TupleExpr(Str("Jupiter"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Uranus"))),
            Return(TupleExpr(Str("Jupiter"), Str("Saturn"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Neptune"))),
            Return(TupleExpr(Str("Jupiter"), Str("Saturn"), Str("Uranus"))),
            .Stmts)
          Return(TupleExpr(.Exprs)),
          .Stmts)
        If(Compare(Name("planet1"), CmpOp("==", Str("Jupiter"))),
          If(Compare(Name("planet2"), CmpOp("==", Str("Mercury"))),
            Return(TupleExpr(Str("Venus"), Str("Earth"), Str("Mars"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Venus"))),
            Return(TupleExpr(Str("Earth"), Str("Mars"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Earth"))),
            Return(TupleExpr(Str("Mars"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Uranus"))),
            Return(TupleExpr(Str("Saturn"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Neptune"))),
            Return(TupleExpr(Str("Saturn"), Str("Uranus"))),
            .Stmts)
          Return(TupleExpr(.Exprs)),
          .Stmts)
        If(Compare(Name("planet1"), CmpOp("==", Str("Saturn"))),
          If(Compare(Name("planet2"), CmpOp("==", Str("Mercury"))),
            Return(
              TupleExpr(
                Str("Venus"),
                Str("Earth"),
                Str("Mars"),
                Str("Jupiter"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Venus"))),
            Return(TupleExpr(Str("Earth"), Str("Mars"), Str("Jupiter"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Earth"))),
            Return(TupleExpr(Str("Mars"), Str("Jupiter"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Mars"))),
            Return(TupleExpr(Str("Jupiter"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Neptune"))),
            Return(TupleExpr(Str("Uranus"))),
            .Stmts)
          Return(TupleExpr(.Exprs)),
          .Stmts)
        If(Compare(Name("planet1"), CmpOp("==", Str("Uranus"))),
          If(Compare(Name("planet2"), CmpOp("==", Str("Mercury"))),
            Return(
              TupleExpr(
                Str("Venus"),
                Str("Earth"),
                Str("Mars"),
                Str("Jupiter"),
                Str("Saturn"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Venus"))),
            Return(
              TupleExpr(
                Str("Earth"),
                Str("Mars"),
                Str("Jupiter"),
                Str("Saturn"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Earth"))),
            Return(TupleExpr(Str("Mars"), Str("Jupiter"), Str("Saturn"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Mars"))),
            Return(TupleExpr(Str("Jupiter"), Str("Saturn"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Jupiter"))),
            Return(TupleExpr(Str("Saturn"))),
            .Stmts)
          Return(TupleExpr(.Exprs)),
          .Stmts)
        If(Compare(Name("planet1"), CmpOp("==", Str("Neptune"))),
          If(Compare(Name("planet2"), CmpOp("==", Str("Mercury"))),
            Return(
              TupleExpr(
                Str("Venus"),
                Str("Earth"),
                Str("Mars"),
                Str("Jupiter"),
                Str("Saturn"),
                Str("Uranus"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Venus"))),
            Return(
              TupleExpr(
                Str("Earth"),
                Str("Mars"),
                Str("Jupiter"),
                Str("Saturn"),
                Str("Uranus"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Earth"))),
            Return(
              TupleExpr(
                Str("Mars"),
                Str("Jupiter"),
                Str("Saturn"),
                Str("Uranus"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Mars"))),
            Return(TupleExpr(Str("Jupiter"), Str("Saturn"), Str("Uranus"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Jupiter"))),
            Return(TupleExpr(Str("Saturn"), Str("Uranus"))),
            .Stmts)
          If(Compare(Name("planet2"), CmpOp("==", Str("Saturn"))),
            Return(TupleExpr(Str("Uranus"))),
            .Stmts)
          Return(TupleExpr(.Exprs)),
          .Stmts)
        Return(TupleExpr(.Exprs))))
endmodule
