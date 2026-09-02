requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // This macro is the exact constructor tree generated in solution.mpy
  // (the generated empty argument list is written explicitly as .Exprs here).
  syntax Stmts ::= "flipCaseBody" [macro]
  rule flipCaseBody
    => Return(Call(Attribute(Name("string"), "swapcase"), .Exprs)) .Stmts

  syntax Module ::= "solutionModule" [macro]
  rule solutionModule
    => Module(
         FuncDef(
           "flip_case",
           Params("string"),
           flipCaseBody))

  // Load the submitted module, then call its required entry point.
  syntax KItem ::= "#runFlipCase" "(" IntSeq ")"
  rule <k> #runFlipCase(S:IntSeq)
        => #loadAll(solutionModule)
        ~> Call(Name("flip_case"), str(S)) ... </k>
endmodule
