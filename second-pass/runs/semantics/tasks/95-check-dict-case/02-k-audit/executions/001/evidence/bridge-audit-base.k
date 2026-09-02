requires "reference-semantics/semantics.k"

// Reviewer definition containing only the supplied fixed semantics.
module BRIDGE-AUDIT-BASE
  imports MPY

  syntax Stmts ::= auditLoopBody() [function, total]
  rule auditLoopBody()
    => Assign(Name("has_key"), Bool(true))
       If(UnaryOp("not",
                  Call(Name("isinstance"),
                       (Name("key"), Name("str"), .Exprs))),
          Assign(Name("all_lower"), Bool(false))
          Assign(Name("all_upper"), Bool(false)),
          If(UnaryOp("not",
                     Call(Attribute(Name("key"), "islower"), .Exprs)),
             Assign(Name("all_lower"), Bool(false)),
             .Stmts)
          If(UnaryOp("not",
                     Call(Attribute(Name("key"), "isupper"), .Exprs)),
             Assign(Name("all_upper"), Bool(false)),
             .Stmts))

  syntax Expr ::= auditResultExpr() [function, total]
  rule auditResultExpr()
    => BoolOp("and",
              (Name("has_key"),
               BoolOp("or",
                      (Name("all_lower"), Name("all_upper"), .Exprs)),
               .Exprs))

  syntax Stmts ::= auditBody() [function, total]
  rule auditBody()
    => Assign(Name("has_key"), Bool(false))
       Assign(Name("all_lower"), Bool(true))
       Assign(Name("all_upper"), Bool(true))
       Assign(Name("key"), NoneVal)
       For(Name("key"),
           Call(Attribute(Name("dict"), "keys"), .Exprs),
           auditLoopBody())
       Return(auditResultExpr())
endmodule
