requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // A named copy of the exact constructor tree emitted in solution.mpy.  The
  // macro gives specifications a compact way to run the translated program;
  // it adds no execution rule and therefore cannot bypass the interpreter.
  syntax Pgm ::= "solutionProgram" [macro]
  syntax Stmts ::= "solutionDefs" [macro]
  rule solutionProgram => Module(solutionDefs)
  rule solutionDefs =>
      FuncDef("count_ones", Params("n"),
        Return(Call(Attribute(Name("n"), "bit_count"), .Exprs)))
      FuncDef("comes_before", Params("a", "b"),
        Return(
          BoolOp(
            "or",
            Compare(
              Call(Name("count_ones"), Name("a")),
              CmpOp("<", Call(Name("count_ones"), Name("b")))),
            BoolOp(
              "and",
              Compare(
                Call(Name("count_ones"), Name("a")),
                CmpOp("==", Call(Name("count_ones"), Name("b")))),
              Compare(Name("a"), CmpOp("<=", Name("b")))))))
      FuncDef("insert_sorted", Params("x", "values"),
        If(Compare(Name("values"), CmpOp("==", ListExpr(.Exprs))),
          Return(ListExpr(Name("x"))),
          .Stmts)
        If(Call(
          Name("comes_before"),
          Name("x"),
          Subscript(Name("values"), Int(0))),
          Return(BinOp("+", ListExpr(Name("x")), Name("values"))),
          .Stmts)
        Return(
          BinOp(
            "+",
            ListExpr(Subscript(Name("values"), Int(0))),
            Call(
              Name("insert_sorted"),
              Name("x"),
              Subscript(Name("values"), Slice(Int(1), NoBound, NoBound))))))
      FuncDef("sort_array", Params("arr"),
        If(Compare(Name("arr"), CmpOp("==", ListExpr(.Exprs))),
          Return(ListExpr(.Exprs)),
          .Stmts)
        Return(
          Call(
            Name("insert_sorted"),
            Subscript(Name("arr"), Int(0)),
            Call(
              Name("sort_array"),
              Subscript(Name("arr"), Slice(Int(1), NoBound, NoBound))))))

  // Independent mathematical reference model for the prose contract.
  syntax Int ::= popcount(Int) [function]
  syntax Bool ::= beforeEq(Int, Int) [function]
                | ordered(Ints) [function]
                | allNonnegative(Ints) [function]
                | sameMultiplicity(Ints, Ints, Ints) [function]
  syntax Ints ::= insertModel(Int, Ints) [function]
                | sortModel(Ints) [function]
  syntax Int ::= occurrences(Int, Ints) [function]

  rule popcount(N) => bitCount(N)

  rule beforeEq(I, J)
    => (popcount(I) <Int popcount(J))
       orBool ((popcount(I) ==Int popcount(J)) andBool (I <=Int J))

  rule insertModel(I, .Ints) => I :: .Ints
  rule insertModel(I, J :: JS) => I :: J :: JS
    requires beforeEq(I, J)
  rule insertModel(I, J :: JS) => J :: insertModel(I, JS)
    requires notBool beforeEq(I, J)

  rule sortModel(.Ints) => .Ints
  rule sortModel(I :: IS) => insertModel(I, sortModel(IS))

  rule ordered(.Ints) => true
  rule ordered(I :: .Ints) => true
  rule ordered(I :: J :: IS) => beforeEq(I, J) andBool ordered(J :: IS)

  rule allNonnegative(.Ints) => true
  rule allNonnegative(I :: IS) => (I >=Int 0) andBool allNonnegative(IS)

  rule occurrences(I, .Ints) => 0
  rule occurrences(I, I :: JS) => 1 +Int occurrences(I, JS)
  rule occurrences(I, J :: JS) => occurrences(I, JS)
    requires I =/=Int J

  // The first argument is the finite set of values whose multiplicities are
  // compared.  Passing the original input is sufficient to establish that a
  // concrete output neither loses nor duplicates any input element.
  rule sameMultiplicity(.Ints, INPUT, OUTPUT) => true
  rule sameMultiplicity(I :: IS, INPUT, OUTPUT)
    => (occurrences(I, INPUT) ==Int occurrences(I, OUTPUT))
       andBool sameMultiplicity(IS, INPUT, OUTPUT)
endmodule
