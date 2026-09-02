requires "verification.k"

module BODY-MUTANT
  imports VERIFICATION

  syntax Stmts ::= "mutantLoopBody" [macro]
  rule mutantLoopBody
    => Expr(
         Call(
           Attribute(Name("result"), "append"),
           Name("string")))

  syntax Stmts ::= "mutantFunctionBody" [macro]
  rule mutantFunctionBody
    => Assign(Name("result"), ListExpr(.Exprs))
       Assign(Name("string"), Str(""))
       For(Name("string"), Name("strings"), mutantLoopBody)
       Return(Name("result"))

  syntax Module ::= "filterByPrefixMutantProgram" [macro]
  rule filterByPrefixMutantProgram
    => Module(
         ImportFrom("typing", "List")
         FuncDef(
           "filter_by_prefix",
           Params("strings", "prefix"),
           mutantFunctionBody))
endmodule
