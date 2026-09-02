requires "verification.k"

module BODY-MUTATED-VERIFICATION
  imports VERIFICATION

  // Reviewer mutation: same binding, but a materially different body.
  syntax Function ::= "mutatedCanArrangeFunction" [macro]
  rule mutatedCanArrangeFunction =>
    function(Params("arr"), Return(Int(0)))

endmodule
