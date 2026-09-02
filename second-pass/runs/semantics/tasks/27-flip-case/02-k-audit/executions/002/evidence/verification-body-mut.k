requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-MUT
  imports MPY

  // Reviewer mutation: execute an identity body, not swapcase.
  syntax Stmts ::= "flipCaseBodyMut" [macro]
  rule flipCaseBodyMut
    => Return(Name("string")) .Stmts

  syntax Module ::= "solutionModuleMut" [macro]
  rule solutionModuleMut
    => Module(
         FuncDef(
           "flip_case",
           Params("string"),
           flipCaseBodyMut))

  syntax KItem ::= "#runFlipCaseMut" "(" IntSeq ")"
  rule <k> #runFlipCaseMut(S:IntSeq)
        => #loadAll(solutionModuleMut)
        ~> Call(Name("flip_case"), str(S)) ... </k>
endmodule
