requires "/tmp/audit-work/verification.k"

module VERIFICATION-BODY-MUTATION
  imports VERIFICATION

  // Materially changed executable body: always return a newly allocated empty list.
  syntax Stmts ::= "mutatedGenerateIntegersBody" [macro]
  rule mutatedGenerateIntegersBody =>
    Assign(Name("result"), ListExpr(.Exprs))
    Return(Name("result"))

  syntax Module ::= "mutatedSolutionModule" [macro]
  rule mutatedSolutionModule =>
    Module(
      FuncDef(
        "generate_integers",
        Params("a", "b"),
        mutatedGenerateIntegersBody
      )
    )

  syntax Val ::= "mutatedGenerateIntegersClosure" [macro]
  rule mutatedGenerateIntegersClosure =>
    closureVal(("a", "b"), mutatedGenerateIntegersBody, 0)
endmodule
