requires "reference-semantics/semantics.k"

module FILTER-VERIFICATION
  imports MPY

  syntax Stmt ::= "FILTER-LOOP-BODY" [macro]
  rule FILTER-LOOP-BODY
    => If(
         Call(Name("isinstance"), Name("value"), Name("int")),
         Expr(Call(Attribute(Name("result"), "append"), Name("value"))),
         .Stmts)

  syntax Stmts ::= "FILTER-FUNCTION-BODY" [macro]
  rule FILTER-FUNCTION-BODY
    => Expr(Str("Filter values, retaining only integers in their original order."))
       Assign(Name("result"), ListExpr(.Exprs))
       For(Name("value"), Name("values"), FILTER-LOOP-BODY)
       Return(Name("result"))

  syntax Val ::= "FILTER-CLOSURE" [macro]
  rule FILTER-CLOSURE
    => closureVal(("values", .ParamNames), FILTER-FUNCTION-BODY, 0)

  syntax Module ::= "FILTER-PROGRAM" [macro]
  rule FILTER-PROGRAM
    => Module(
         ImportFrom("typing", "List", "Any")
         FuncDef("filter_integers", Params("values"), FILTER-FUNCTION-BODY))
endmodule
