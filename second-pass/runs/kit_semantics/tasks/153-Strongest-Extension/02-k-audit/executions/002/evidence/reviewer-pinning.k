requires "reference-semantics/semantics.k"

module REVIEWER-PINNING
  imports MPY

  syntax Stmts ::= "REVIEWED-PROGRAM-BODY" [macro]
  rule REVIEWED-PROGRAM-BODY
    => Assign(Name("strongest"), Str(""))
       Assign(Name("best_strength"), NoneVal)
       Assign(Name("extension"), Str(""))
       Assign(Name("character"), Str(""))
       For(
         Name("extension"),
         Name("extensions"),
         Assign(Name("strength"), Int(0))
         For(
           Name("character"),
           Name("extension"),
           If(
             Call(Attribute(Name("character"), "isupper"), .Exprs),
             AugAssign(Name("strength"), "+", Int(1)) .Stmts,
             If(
               Call(Attribute(Name("character"), "islower"), .Exprs),
               AugAssign(Name("strength"), "-", Int(1)) .Stmts,
               .Stmts
             ) .Stmts
           ) .Stmts
         )
         If(
           BoolOp(
             "or",
             Compare(Name("best_strength"), CmpOp("is", NoneVal)),
             Compare(Name("strength"), CmpOp(">", Name("best_strength"))),
             .Exprs
           ),
           Assign(Name("strongest"), Name("extension"))
           Assign(Name("best_strength"), Name("strength"))
           .Stmts,
           .Stmts
         )
         .Stmts
       )
       Return(
         BinOp(
           "+",
           BinOp("+", Name("class_name"), Str(".")),
           Name("strongest")
         )
       )
       .Stmts
endmodule
