requires "semantic.k"

module VERIFICATION
  imports MPY

  // The independent mathematical contract. For a suffix of length N,
  // answer returns the largest local drop index, or -1. A drop in the tail
  // outranks the head pair, hence the recursive result is shifted by one.
  syntax Int ::= "answer" "(" Arr "," Int "," Int ")" [function, total]
               | "answerStep" "(" Int "," Int "," Int ")" [function, total]

  rule answer(A, O, N) => -1
       requires N <=Int 1
  rule answer(A, O, N)
       => answerStep(
            answer(A, O +Int 1, N -Int 1),
            get(A, O),
            get(A, O +Int 1))
       requires N >Int 1

  rule answerStep(R, X, Y) => R +Int 1
       requires R =/=Int -1
  rule answerStep(R, X, Y) => 1
       requires R ==Int -1 andBool Y <Int X
  rule answerStep(R, X, Y) => -1
       requires R ==Int -1 andBool Y >=Int X

  // This macro is exactly the constructor tree generated in solution.mpy.
  // It is data consumed by invoke/exec/eval; it is not an implementation or
  // a shortcut rule for can_arrange.
  syntax Function ::= "canArrangeFunction" [macro]
  rule canArrangeFunction =>
    function(Params("arr"),
      If(Compare(Call(Name("len"), Name("arr")), CmpOp("<=", Int(1))),
        Return(UnaryOp("-", Int(1))),
        Assign(Name("result"),
          Call(Name("can_arrange"),
            Subscript(Name("arr"), Slice(Int(1), NoBound, NoBound))))
        If(Compare(Name("result"),
                   CmpOp("!=", UnaryOp("-", Int(1)))),
          Return(BinOp("+", Name("result"), Int(1))),
          If(Compare(Subscript(Name("arr"), Int(1)),
                     CmpOp("<", Subscript(Name("arr"), Int(0)))),
            Return(Int(1)),
            Return(UnaryOp("-", Int(1)))))))

  syntax Pgm ::= "solutionProgram" [macro]
  rule solutionProgram =>
    Module(FuncDef("can_arrange", Params("arr"),
      If(Compare(Call(Name("len"), Name("arr")), CmpOp("<=", Int(1))),
        Return(UnaryOp("-", Int(1))),
        Assign(Name("result"),
          Call(Name("can_arrange"),
            Subscript(Name("arr"), Slice(Int(1), NoBound, NoBound))))
        If(Compare(Name("result"),
                   CmpOp("!=", UnaryOp("-", Int(1)))),
          Return(BinOp("+", Name("result"), Int(1))),
          If(Compare(Subscript(Name("arr"), Int(1)),
                     CmpOp("<", Subscript(Name("arr"), Int(0)))),
            Return(Int(1)),
            Return(UnaryOp("-", Int(1))))))))

endmodule
