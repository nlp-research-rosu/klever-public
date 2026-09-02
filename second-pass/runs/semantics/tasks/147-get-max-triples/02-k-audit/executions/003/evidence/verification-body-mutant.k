requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-MUTANT
  imports MPY

  // The actually executed body is deliberately changed to return one too much.
  syntax Stmts ::= "getMaxTriplesBodyMutant" [function]
  rule getMaxTriplesBodyMutant
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
       Return(
         BinOp(
           "+",
           BinOp("+", Name("zero_triples"), Name("one_triples")),
           Int(1)))
       .Stmts

  syntax Int ::= chooseThreeMutant(Int) [function]
  rule chooseThreeMutant(C:Int)
    => (C *Int (C -Int 1) *Int (C -Int 2)
        -Int pyMod(C *Int (C -Int 1) *Int (C -Int 2), 6)) /Int 6

  syntax Int ::= zeroResiduesMutant(Int) [function]
  rule zeroResiduesMutant(N:Int)
    => (N +Int 1 -Int pyMod(N +Int 1, 3)) /Int 3

  syntax Int ::= tripleCountMutant(Int) [function]
  rule tripleCountMutant(N:Int)
    => chooseThreeMutant(zeroResiduesMutant(N))
       +Int chooseThreeMutant(N -Int zeroResiduesMutant(N))
endmodule
