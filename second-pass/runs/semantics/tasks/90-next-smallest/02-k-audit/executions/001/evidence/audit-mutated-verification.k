requires "verification.k"

module AUDIT-MUTATED-VERIFICATION
  imports NEXT-SMALLEST-VERIFICATION

  // Operational-sensitivity mutation: when the inner branch records a new
  // second minimum, store value + 1.
  syntax Stmts ::= "auditMutatedLoopBody" [macro]
  rule auditMutatedLoopBody =>
    If(Compare(Name("count"), CmpOp("==", Int(0))),
       Assign(Name("smallest"), Name("value"))
       Assign(Name("count"), Int(1)),
       If(Compare(Name("value"), CmpOp("<", Name("smallest"))),
          Assign(Name("second"), Name("smallest"))
          Assign(Name("count"), Int(2))
          Assign(Name("smallest"), Name("value")),
          If(Compare(Name("value"), CmpOp("!=", Name("smallest"))),
             If(BoolOp("or",
                       (Compare(Name("count"), CmpOp("==", Int(1))),
                        Compare(Name("value"), CmpOp("<", Name("second"))),
                        .Exprs)),
                Assign(Name("second"),
                       BinOp("+", Name("value"), Int(1)))
                Assign(Name("count"), Int(2)),
                .Stmts) .Stmts,
             .Stmts) .Stmts))
endmodule
