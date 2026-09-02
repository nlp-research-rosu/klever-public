requires "verification.k"

module PROJECTION-OPPOSITE-SPEC
  imports VERIFICATION-BASE

  // Deliberately false opposite interpretation: project("A") is not "".
  claim [projection-opposite]:
    <k>
      projectStrTotal(str(iCons(65, .IntSeq)))
      => str(.IntSeq)
    </k>
endmodule
