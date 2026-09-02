requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // These two wrappers expose the exact definition emitted in solution.mpy.
  // Keeping loading and invocation separate gives small, compositional claims.
  syntax KItem ::= "#loadCountDistinct"
                 | "#callCountDistinct" "(" IntSeq ")"

  rule #loadCountDistinct
    => FuncDef(
         "count_distinct_characters",
         Params("string"),
         Return(
           Call(
             Name("len"),
             Call(
               Name("set"),
               Call(Attribute(Name("string"), "lower"), .Exprs)))))

  rule #callCountDistinct(CS:IntSeq)
    => #applyK(
         toCall(
           closureVal(
             ("string", .ParamNames),
             Return(
               Call(
                 Name("len"),
                 Call(Attribute(Name("string"), "lower"), .Exprs)))
             .Stmts,
             0)),
         (str(CS), .Vals))
endmodule
