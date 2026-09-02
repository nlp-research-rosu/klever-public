requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // These macros are the exact constructor translation in solution.mpy,
  // factored so the specifications can also name the installed closure.
  syntax Stmts ::= "stringToMd5Body" [macro]
  rule stringToMd5Body
    => If(UnaryOp("not", Name("text")),
         Return(NoneVal),
         .Stmts)
       Return(
         Call(
           Attribute(
             Call(
               Attribute(Name("hashlib"), "md5"),
               Call(Attribute(Name("text"), "encode"), Str("utf-8"))),
             "hexdigest"),
           .Exprs))

  syntax Module ::= "solutionModule" [macro]
  rule solutionModule
    => Module(
         Import("hashlib")
         FuncDef("string_to_md5", Params("text"), stringToMd5Body))

  syntax Val ::= "stringToMd5Closure" [macro]
  rule stringToMd5Closure
    => closureVal("text", stringToMd5Body, 0)
endmodule
