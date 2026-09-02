requires "semantic.k"

module VERIFICATION-BODY-MUTATION
  imports MPY

  // Reviewer mutation: the compared literal is 1 instead of the submitted 0.
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
                        CmpOp("!=", Int(1)))))))))

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
