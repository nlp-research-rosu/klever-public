requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Reviewer mutation: the final 5 is changed to 6.  For this concrete,
  // satisfiable input both trusted Python implementations return
  // [1, 2, 4, 3, 5], so this obligation is deliberately false.
  claim [false-example-result]:
    <k> #run(solutionProgram, listV(1 :: 5 :: 2 :: 3 :: 4 :: .Ints))
      => listV(1 :: 2 :: 4 :: 3 :: 6 :: .Ints) </k>
endmodule
