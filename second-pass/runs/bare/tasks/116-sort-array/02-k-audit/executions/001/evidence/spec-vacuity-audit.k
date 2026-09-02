requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh reviewer mutation.  The true first element is 1, not 0.
  claim [false-example-one]:
    <k> #run(solutionProgram, listV(1 :: 5 :: 2 :: 3 :: 4 :: .Ints))
      => listV(0 :: 2 :: 4 :: 3 :: 5 :: .Ints) </k>
endmodule
