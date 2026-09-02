// Reviewer body-sensitivity mutation of the proof's executed program term:
// only the first invalid return changes from -1 to -2.
requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  syntax Program ::= "solutionProgram" [function]
  syntax Rat ::= heronRadicand(Int, Int, Int) [function]

  rule heronRadicand(A, B, C) =>
    (((A +Int B +Int C) /Rat 2)
      *Rat (((A +Int B +Int C) /Rat 2) -Rat A)
      *Rat (((A +Int B +Int C) /Rat 2) -Rat B)
      *Rat (((A +Int B +Int C) /Rat 2) -Rat C))

  rule solutionProgram =>
    Module(
      FuncDef("triangle_area", Params("a", "b", "c"),
        If(Compare(BinOp("+", Name("a"), Name("b")), CmpOp("<=", Name("c"))),
          Return(UnaryOp("-", Int(2))),
          )
        If(Compare(BinOp("+", Name("a"), Name("c")), CmpOp("<=", Name("b"))),
          Return(UnaryOp("-", Int(1))),
          )
        If(Compare(BinOp("+", Name("b"), Name("c")), CmpOp("<=", Name("a"))),
          Return(UnaryOp("-", Int(1))),
          )
        Assign(
          Name("semiperimeter"),
          BinOp(
            "/",
            BinOp("+", BinOp("+", Name("a"), Name("b")), Name("c")),
            Int(2)))
        Assign(
          Name("area"),
          BinOp(
            "**",
            BinOp(
              "*",
              BinOp(
                "*",
                BinOp(
                  "*",
                  Name("semiperimeter"),
                  BinOp("-", Name("semiperimeter"), Name("a"))),
                BinOp("-", Name("semiperimeter"), Name("b"))),
              BinOp("-", Name("semiperimeter"), Name("c"))),
            Float(0.5)))
        Return(Call(Name("round"), Name("area"), Int(2)))))
endmodule
