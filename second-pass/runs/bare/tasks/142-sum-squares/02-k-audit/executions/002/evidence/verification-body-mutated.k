requires "semantic.k"

module MPY-VERIFICATION-BODY-MUTATED
  imports MPY-SEMANTICS

  // Independent mathematical contract, phrased over the runtime integer-list
  // representation.  It consumes the list from the right so that the index of
  // the final element is exactly the length of its prefix.
  syntax Int ::= "elementContribution" "(" Int "," Int ")" [function]
  rule elementContribution(N, I) => N *Int N
    requires I %Int 3 ==Int 0 [simplification]
  rule elementContribution(N, I) => N *Int N *Int N
    requires notBool (I %Int 3 ==Int 0)
         andBool I %Int 4 ==Int 0 [simplification]
  rule elementContribution(N, I) => N
    requires notBool (I %Int 3 ==Int 0)
         andBool notBool (I %Int 4 ==Int 0) [simplification]

  syntax Int ::= "sumSquaresSpec" "(" Ints ")" [function]
  rule sumSquaresSpec(IS) => 0
    requires IS ==K .Ints
  rule sumSquaresSpec(IS)
    => sumSquaresSpec(initInts(IS))
       +Int elementContribution(lastInt(IS), lengthInts(IS) -Int 1)
    requires IS =/=K .Ints

  // The exact translated function body, shared by the loaded-function lemma
  // and the end-to-end program claim below.
  syntax Stmts ::= "sumSquaresBody" [function]
  rule sumSquaresBody =>
    If(Compare(Name("lst"), CmpOp("==", ListExpr(.Exprs))),
      Return(Int(0)),
      Assign(
        Name("index"),
        BinOp("-", Call(Name("len"), Name("lst")), Int(1)))
      Assign(
        Name("value"),
        Subscript(Name("lst"), UnaryOp("-", Int(1))))
      If(Compare(BinOp("%", Name("index"), Int(3)), CmpOp("==", Int(0))),
        Assign(
          Name("contribution"),
          BinOp("+", Name("value"), Name("value"))),
        If(Compare(BinOp("%", Name("index"), Int(4)), CmpOp("==", Int(0))),
          Assign(
            Name("contribution"),
            BinOp(
              "*",
              BinOp("*", Name("value"), Name("value")),
              Name("value"))),
          Assign(Name("contribution"), Name("value"))))
      Return(
        BinOp(
          "+",
          Call(
            Name("sum_squares"),
            Subscript(
              Name("lst"),
              Slice(NoBound, UnaryOp("-", Int(1)), NoBound))),
          Name("contribution"))))

  syntax Pgm ::= "solutionProgram" [function]
  rule solutionProgram =>
    Module(FuncDef("sum_squares", Params("lst"), sumSquaresBody))

  syntax Map ::= "solutionFunctions" [function]
  rule solutionFunctions =>
    "sum_squares" |-> function1("lst", sumSquaresBody)
endmodule
