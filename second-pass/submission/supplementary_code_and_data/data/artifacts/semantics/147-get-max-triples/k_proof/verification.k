requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The statement sequence emitted in solution.mpy, named only to keep the
  // configuration claim readable.
  syntax Stmts ::= "getMaxTriplesBody" [function]
  rule getMaxTriplesBody
    => Assign(
         Name("zero_count"),
         BinOp("//", BinOp("+", Name("n"), Int(1)), Int(3)))
       Assign(
         Name("one_count"),
         BinOp("-", Name("n"), Name("zero_count")))
       Assign(
         Name("zero_triples"),
         BinOp(
           "//",
           BinOp(
             "*",
             BinOp(
               "*",
               Name("zero_count"),
               BinOp("-", Name("zero_count"), Int(1))),
             BinOp("-", Name("zero_count"), Int(2))),
           Int(6)))
       Assign(
         Name("one_triples"),
         BinOp(
           "//",
           BinOp(
             "*",
             BinOp(
               "*",
               Name("one_count"),
               BinOp("-", Name("one_count"), Int(1))),
             BinOp("-", Name("one_count"), Int(2))),
           Int(6)))
       Return(BinOp("+", Name("zero_triples"), Name("one_triples")))
       .Stmts

  // C(c, 3), written with the same floored-integer operation as Python.
  // The argument is always a non-negative population count.
  syntax Int ::= chooseThree(Int) [function]
  rule chooseThree(C:Int)
    => (C *Int (C -Int 1) *Int (C -Int 2)
        -Int pyMod(C *Int (C -Int 1) *Int (C -Int 2), 6)) /Int 6

  // Among 1,...,n, exactly floor((n+1)/3) indices are 2 modulo 3.
  syntax Int ::= zeroResidues(Int) [function]
  rule zeroResidues(N:Int)
    => (N +Int 1 -Int pyMod(N +Int 1, 3)) /Int 3

  syntax Int ::= tripleCount(Int) [function]
  rule tripleCount(N:Int)
    => chooseThree(zeroResidues(N))
       +Int chooseThree(N -Int zeroResidues(N))
endmodule
