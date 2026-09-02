requires "/tmp/audit-work/candidate-src/mutation.k"

module BODY-MUTANT-VERIFICATION
  imports MUTATION

  // Reviewer mutation: this is the complete entry-program term, with the
  // actually executed loop body changed to MUTANT-STEP (append "Z").
  syntax Module ::= "MUTANT-PROGRAM" [macro]
  rule MUTANT-PROGRAM
    => Module(
         FuncDef("numerical_letter_grade", Params("grades"),
           Assign(Name("letter_grades"), ListExpr(.Exprs))
           Assign(Name("grade"), Float(0.0))
           For(Name("grade"), Name("grades"), MUTANT-STEP)
           Return(Name("letter_grades"))
         )
       )
endmodule
