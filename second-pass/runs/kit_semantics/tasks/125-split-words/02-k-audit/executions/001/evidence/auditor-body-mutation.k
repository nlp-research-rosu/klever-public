requires "verification.k"

module AUDITOR-BODY-MUTATION
  imports VERIFICATION

  // Materially replace the actual function body term by a constant return.
  syntax Stmts ::= "auditorMutatedBody" [function, total]
  rule auditorMutatedBody => Return(Int(0)) .Stmts
endmodule
