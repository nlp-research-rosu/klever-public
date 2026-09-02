requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: the real result is LIST1 whenever its total is no
  // greater, but this mutation requires LIST2 under the original precondition.
  claim [false-first-result]:
    <k>
      run(solutionProgram, args(pyList(LIST1), pyList(LIST2)))
      => pyList(LIST2)
    </k>
    requires totalChars(LIST1) <=Int totalChars(LIST2)
endmodule
