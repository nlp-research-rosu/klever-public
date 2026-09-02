requires "semantic.k"

module SOLUTION
  imports MPY
  syntax Program ::= "solutionProgram" [function]
  rule solutionProgram => Module(
  FuncDef("same_chars", Params("s0", "s1"),
    Return(
      Compare(
        Call(Name("set"), Name("s0")),
        CmpOp("==", Call(Name("set"), Name("s1")))))))
endmodule
