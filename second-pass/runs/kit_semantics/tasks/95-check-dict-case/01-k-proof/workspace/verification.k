requires "proof-theory.k"

module VERIFICATION
  imports PROOF-THEORY

  // Definitional AST aliases used by the invariant.  They expand to the
  // literal translated loop body and return expression.
  syntax Stmts ::= checkDictLoopBody() [function, total]
  rule checkDictLoopBody()
    => Assign(Name("seen_key"), Bool(true))
       Assign(
         Name("is_string"),
         BoolOp(
           "and",
           BoolOp("or", Name("all_lower"), Name("all_upper")),
           Call(Name("isinstance"), Name("key"), Name("str"))))
       Assign(
         Name("all_lower"),
         BoolOp(
           "and",
           Name("all_lower"),
           Name("is_string"),
           Call(Attribute(Name("key"), "islower"), .Exprs)))
       Assign(
         Name("all_upper"),
         BoolOp(
           "and",
           Name("all_upper"),
           Name("is_string"),
           Call(Attribute(Name("key"), "isupper"), .Exprs)))

  syntax Expr ::= checkDictReturn() [function, total]
  rule checkDictReturn()
    => BoolOp(
         "and",
         Name("seen_key"),
         BoolOp("or", Name("all_lower"), Name("all_upper")))

  syntax Stmts ::= checkDictBody() [function, total]
  rule checkDictBody()
    => Assign(Name("all_lower"), Bool(true))
       Assign(Name("all_upper"), Bool(true))
       Assign(Name("seen_key"), Bool(false))
       Assign(Name("key"), NoneVal)
       Assign(Name("is_string"), Bool(false))
       For(
         Name("key"),
         Call(Attribute(Name("dict"), "keys"), .Exprs),
         checkDictLoopBody())
       Return(checkDictReturn())

  // isStringKey's true domain is exactly str(CS); connection-spec.k proves
  // the frozen method result for every CS and arbitrary continuation.
  rule applyMethod(V:Val, "islower", .Vals)
    => lowerKeyCodes(stringCodes(V))
    requires isStringKey(V) andBool notBool isRefV(V)
    [simplification]
  rule applyMethod(V:Val, "isupper", .Vals)
    => upperKeyCodes(stringCodes(V))
    requires isStringKey(V) andBool notBool isRefV(V)
    [simplification]

  // The frozen builtin produces isStrV(V).  This bridge replaces it with the
  // exhaustively defined twin only after normal lookup and argument evaluation.
  // Reference arguments remain on the frozen heap-dereference path.
  rule <k> #applyK(
              toCall(builtinV("isinstance")),
              (V:Val, typeV("str"), .Vals))
        => isStringKey(V) ... </k>
    requires notBool isRefV(V)
    [priority(40)]
endmodule
