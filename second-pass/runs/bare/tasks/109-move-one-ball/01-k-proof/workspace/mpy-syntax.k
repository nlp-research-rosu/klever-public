module HUMAN-EVAL-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  // The source fragment emitted by py2mpy.py for solution.py.
  syntax Pgm ::= Module(Stmts)
  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= FuncDef(String, Params, Stmts)
                | Return(Expr)
                | Assign(Expr, Expr)
                | If(Expr, Stmts, Stmts)
                | For(Expr, Expr, Stmts)
  syntax Params ::= Params(String)

  syntax Expr ::= Name(String)
                | Int(Int)
                | Bool(Bool)
                | UnaryOp(String, Expr)
                | BinOp(String, Expr, Expr)
                | Compare(Expr, CmpOp)
                | Call(Expr, Expr)
                | Subscript(Expr, Expr)
  syntax CmpOp ::= CmpOp(String, Expr)

  // External input notation used with -cINPUT, e.g. 3 :: 4 :: .IList.
  syntax IList ::= ".IList"
                 | Int "::" IList

  // Name for the exact translated constructor tree, used by symbolic claims.
  syntax Pgm ::= "theSolution" [function, total]
  rule theSolution =>
    Module(
      FuncDef("move_one_ball", Params("arr"),
        If(Compare(Call(Name("len"), Name("arr")), CmpOp("==", Int(0))),
          Return(Bool(true)) .Stmts,
          .Stmts)
        Assign(Name("drops"), Int(0))
        Assign(Name("previous"),
          Subscript(Name("arr"), UnaryOp("-", Int(1))))
        For(Name("value"), Name("arr"),
          If(Compare(Name("previous"), CmpOp(">", Name("value"))),
            Assign(Name("drops"),
              BinOp("+", Name("drops"), Int(1))) .Stmts,
            .Stmts)
          Assign(Name("previous"), Name("value")) .Stmts)
        Return(Compare(Name("drops"), CmpOp("<=", Int(1)))) .Stmts))
endmodule
