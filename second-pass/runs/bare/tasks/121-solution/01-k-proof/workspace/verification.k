requires "semantic.k"

module VERIFICATION
  imports MPY

  // Exact AST emitted in solution.mpy, given a short name for specifications.
  syntax Pgm ::= "solutionProgram" [function]
  rule solutionProgram =>
    Module(
      FuncDef("solution", Params("lst"),
        Return(
          Call(
            Name("sum"),
            ListComp(Name("x"),
              CompFor(
                Name("x"),
                Subscript(Name("lst"), Slice(NoBound, NoBound, Int(2))),
                Compare(BinOp("%", Name("x"), Int(2)),
                        CmpOp("!=", Int(0)))))))))

  // Independent mathematical contract: consume positions 0, 2, 4, ... and
  // add the current integer exactly when Python's remainder modulo 2 is nonzero.
  syntax Int ::= "expected" "(" Ints "," Int ")" [function]
  rule expected(nil, ACC) => ACC
  rule expected(cons(I, nil), ACC) => ACC +Int I
    requires I modInt 2 =/=Int 0
  rule expected(cons(I, nil), ACC) => ACC
    requires I modInt 2 ==Int 0
  rule expected(cons(I, cons(_, IS)), ACC) => expected(IS, ACC +Int I)
    requires I modInt 2 =/=Int 0
  rule expected(cons(I, cons(_, IS)), ACC) => expected(IS, ACC)
    requires I modInt 2 ==Int 0
endmodule
