requires "verification.k"

module MUTATION
  imports VERIFICATION

  // Materially wrong loop body used only by the body-sensitivity probe.
  syntax Stmts ::= "MUTANT-STEP" [macro]
  rule MUTANT-STEP
    => Expr(
         Call(
           Attribute(Name("letter_grades"), "append"),
           Str("Z")
         )
       )
endmodule
