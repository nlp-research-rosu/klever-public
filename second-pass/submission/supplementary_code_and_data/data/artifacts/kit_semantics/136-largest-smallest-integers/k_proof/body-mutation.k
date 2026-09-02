requires "verification-core.k"

module BODY-MUTATION-SYNTAX
  imports VERIFICATION-CORE-SYNTAX

  syntax Stmts ::= "lsiMutantLoopBody" [macro]
  syntax Stmts ::= "lsiMutantBody" [macro]
endmodule

module BODY-MUTATION
  imports VERIFICATION-CORE
  imports BODY-MUTATION-SYNTAX

  // Mutation: among later negative values, choose a smaller value instead of
  // the larger (closer-to-zero) value.
  rule lsiMutantLoopBody
    => If(Compare(Name("value"), CmpOp("<", Int(0))),
         If(BoolOp("or",
              Compare(Name("largest_negative"), CmpOp("==", Int(0))),
              Compare(Name("value"), CmpOp("<", Name("largest_negative")))),
            Assign(Name("largest_negative"), Name("value")),
            .Stmts),
         .Stmts)
       If(Compare(Name("value"), CmpOp(">", Int(0))),
         If(BoolOp("or",
              Compare(Name("smallest_positive"), CmpOp("==", Int(0))),
              Compare(Name("value"), CmpOp("<", Name("smallest_positive")))),
            Assign(Name("smallest_positive"), Name("value")),
            .Stmts),
         .Stmts)

  rule lsiMutantBody
    => Assign(Name("largest_negative"), Int(0))
       Assign(Name("smallest_positive"), Int(0))
       Assign(Name("value"), Int(0))
       For(Name("value"), Name("lst"), lsiMutantLoopBody)
       Return(TupleExpr(
         IfExp(Compare(Name("largest_negative"), CmpOp("==", Int(0))),
               NoneVal,
               Name("largest_negative")),
         IfExp(Compare(Name("smallest_positive"), CmpOp("==", Int(0))),
               NoneVal,
               Name("smallest_positive"))))
endmodule
