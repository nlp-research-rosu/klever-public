requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: the satisfying input [] returns true, not false.
  claim [empty-is-false]:
    <k>
      #run(solutionProgram, listVal(nil))
      => boolVal(false)
    </k>
endmodule
