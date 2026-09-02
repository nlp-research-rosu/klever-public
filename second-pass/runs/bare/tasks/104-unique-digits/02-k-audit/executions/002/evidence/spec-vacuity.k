requires "/tmp/audit-work/104-unique-digits-audit-002/source/verification.k"

module AUDIT-SPEC-VACUITY
  imports VERIFICATION

  // False result mutation for the satisfying positive input [15, 2].
  // The correct result is [15], not [16].
  claim <k> solutionProgram ~> invoke("unique_digits",
          pyList(cons(15, cons(2, .Ints))))
        => pyList(cons(16, .Ints)) ... </k>
endmodule
