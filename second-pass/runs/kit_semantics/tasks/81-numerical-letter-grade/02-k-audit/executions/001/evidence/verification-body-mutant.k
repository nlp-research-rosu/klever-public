requires "verification.k"

module AUDIT-BODY-MUTANT
  imports VERIFICATION

  // Material mutation of the executed loop body: append "Q" unconditionally.
  syntax Stmts ::= "AUDIT-MUTANT-STEP" [macro]
  rule AUDIT-MUTANT-STEP
    => Expr(
         Call(
           Attribute(Name("letter_grades"), "append"),
           Str("Q")
         )
       )
endmodule
