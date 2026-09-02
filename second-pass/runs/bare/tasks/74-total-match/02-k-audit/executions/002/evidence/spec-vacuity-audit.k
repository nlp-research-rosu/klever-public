requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: under a strict smaller-first total, demand list2.
  claim [false-first-result]:
    <k>
      run(solutionProgram, args(pyList(LIST1), pyList(LIST2)))
      => pyList(LIST2)
    </k>
    requires totalChars(LIST1) <Int totalChars(LIST2)
endmodule
