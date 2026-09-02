requires "reference-semantics/semantics.k"

module TRIANGLE-VERIFICATION
  imports MPY

  // This is the translated body from solution.mpy, packaged as a value so the
  // claims can call it directly without depending on a module-scope map entry.
  syntax Stmts ::= "triangleAreaBody" [function]
  rule triangleAreaBody
    => If(
         BoolOp(
           "or",
           Compare(BinOp("+", Name("a"), Name("b")),
                   CmpOp("<=", Name("c"))),
           Compare(BinOp("+", Name("a"), Name("c")),
                   CmpOp("<=", Name("b"))),
           Compare(BinOp("+", Name("b"), Name("c")),
                   CmpOp("<=", Name("a")))),
         Return(UnaryOp("-", Int(1))),
         .Stmts)
       Assign(
         Name("s"),
         BinOp(
           "/",
           BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c")),
           Int(2)))
       Return(
         Call(
           Name("round"),
           BinOp(
             "**",
             BinOp(
               "*",
               BinOp(
                 "*",
                 BinOp("*", Name("s"),
                       BinOp("-", Name("s"), Name("a"))),
                 BinOp("-", Name("s"), Name("b"))),
               BinOp("-", Name("s"), Name("c"))),
             Float(1.0)),
           Int(2)))

  syntax Val ::= "triangleAreaClosure" [function]
  rule triangleAreaClosure
    => closureVal(("a", "b", "c"), triangleAreaBody, 0)

  syntax Module ::= "triangleAreaModule" [function]
  rule triangleAreaModule
    => Module(
         FuncDef(
           "triangle_area",
           Params("a", "b", "c"),
           triangleAreaBody))

  // The exact proof-domain value of Heron's formula.  The supplied reference
  // semantics deliberately keeps float operations opaque under kprove, so
  // correctness is structural at these trusted float primitives.
  syntax Float ::= semiPerimeter(Int, Int, Int) [function]
  rule semiPerimeter(A, B, C) => divII(A +Int B +Int C, 2)

  syntax Float ::= expectedArea(Int, Int, Int) [function]
  rule expectedArea(A, B, C)
    => roundFN(
         powF(
           mulF(
             mulF(
               mulF(
                 semiPerimeter(A, B, C),
                 subF(semiPerimeter(A, B, C), intToF(A))),
               subF(semiPerimeter(A, B, C), intToF(B))),
             subF(semiPerimeter(A, B, C), intToF(C))),
           0.5),
         2)
endmodule
