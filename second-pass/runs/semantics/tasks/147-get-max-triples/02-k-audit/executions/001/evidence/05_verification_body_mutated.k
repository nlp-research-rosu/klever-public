requires "reference-semantics/semantics.k"

module AUDIT-BODY-MUTATED
  imports MPY

  // Exact submitted body except for a deliberate +1 in the returned value.
  syntax Stmts ::= "auditMutatedBody" [function]
  rule auditMutatedBody
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

  syntax Int ::= auditChooseThree(Int) [function]
  rule auditChooseThree(C:Int)
    => (C *Int (C -Int 1) *Int (C -Int 2)
        -Int pyMod(C *Int (C -Int 1) *Int (C -Int 2), 6)) /Int 6

  syntax Int ::= auditZeroResidues(Int) [function]
  rule auditZeroResidues(N:Int)
    => (N +Int 1 -Int pyMod(N +Int 1, 3)) /Int 3

  syntax Int ::= auditTripleCount(Int) [function]
  rule auditTripleCount(N:Int)
    => auditChooseThree(auditZeroResidues(N))
       +Int auditChooseThree(N -Int auditZeroResidues(N))
endmodule
