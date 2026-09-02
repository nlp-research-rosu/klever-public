requires "verification-body-mut.k"

module SPEC-BODY-MUT
  imports VERIFICATION-BODY-MUT

  claim [mutated-first-lt]:
    <k>
      run(mutatedSolutionProgram, args(pyList(LIST1), pyList(LIST2)))
      => pyList(LIST1)
    </k>
    requires totalCharsMut(LIST1) <Int totalCharsMut(LIST2)
endmodule
