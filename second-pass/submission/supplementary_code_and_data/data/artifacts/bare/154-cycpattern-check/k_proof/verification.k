requires "semantic.k"
requires "solution-program.k"

module VERIFICATION
  imports MPY
  imports SOLUTION-PROGRAM

  // The loop pattern used by the circular invariant.  solutionProgram() is
  // generated mechanically from solution.mpy in solution-program.k.
  syntax Stmt ::= solutionLoop() [macro]
  rule solutionLoop() =>
    While(
      Compare(Name("i"), CmpOp("<", Call(Name("len"), Name("b")))),
      If(
        Compare(
          BinOp("+",
            Subscript(Name("b"), Slice(Name("i"), NoBound, NoBound)),
            Subscript(Name("b"), Slice(NoBound, Name("i"), NoBound))),
          CmpOp("in", Name("a"))),
        Return(Bool(true)),
        .Stmts)
      Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
  // A mathematical reference function for the contract: inspect each cyclic
  // rotation of B in order and ask whether it occurs in A.
  syntax Bool ::= cyclicContains(String, String) [function, total]
                | cyclicContainsFrom(String, String, Int) [function, total]

  rule cyclicContains(A, B) => cyclicContainsFrom(A, B, 0)
  rule cyclicContainsFrom(_A, B, I) => false
    requires I >=Int lengthString(B)
  rule cyclicContainsFrom(A, B, I)
    => true
    requires I <Int lengthString(B)
     andBool indexOf(A,
                     substrString(B, I, lengthString(B))
                     +String substrString(B, 0, I),
                     0) >=Int 0
  rule cyclicContainsFrom(A, B, I)
    => cyclicContainsFrom(A, B, I +Int 1)
    requires I <Int lengthString(B)
     andBool indexOf(A,
                     substrString(B, I, lengthString(B))
                     +String substrString(B, 0, I),
                     0) <Int 0
endmodule

module VERIFICATION-SYNTAX
  imports VERIFICATION
endmodule
