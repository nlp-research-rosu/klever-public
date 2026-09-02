requires "verification.k"

module PINNING-COMPARE
  imports VERIFICATION

  // Expected constructors independently transcribed from the trusted
  // regeneration of solution.mpy.
  claim [loop-body]:
    <k>
      #fixSpacesLoopBody
      =>
      If(
        Compare(Name("char"), CmpOp("==", Str(" "))),
        If(
          Compare(Name("spaces"), CmpOp("==", Str("__"))),
          Assign(Name("spaces"), Str("-")),
          If(
            Compare(Name("spaces"), CmpOp("!=", Str("-"))),
            AugAssign(Name("spaces"), "+", Str("_")),
            .Stmts)),
        AugAssign(
          Name("result"),
          "+",
          BinOp("+", Name("spaces"), Name("char")))
        Assign(Name("spaces"), Str("")))
    </k>

  claim [function-body]:
    <k>
      #fixSpacesBody
      =>
      Assign(Name("result"), Str(""))
      Assign(Name("spaces"), Str(""))
      Assign(Name("char"), Str(""))
      For(
        Name("char"),
        Name("text"),
        If(
          Compare(Name("char"), CmpOp("==", Str(" "))),
          If(
            Compare(Name("spaces"), CmpOp("==", Str("__"))),
            Assign(Name("spaces"), Str("-")),
            If(
              Compare(Name("spaces"), CmpOp("!=", Str("-"))),
              AugAssign(Name("spaces"), "+", Str("_")),
              .Stmts)),
          AugAssign(
            Name("result"),
            "+",
            BinOp("+", Name("spaces"), Name("char")))
          Assign(Name("spaces"), Str(""))))
      Return(BinOp("+", Name("result"), Name("spaces")))
    </k>
endmodule
