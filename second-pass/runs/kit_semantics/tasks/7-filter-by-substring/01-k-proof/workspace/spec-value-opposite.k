requires "verification.k"

module SPEC-VALUE-OPPOSITE
  imports VERIFICATION

  // Deliberately wrong interpretation of the proof-local projection.
  claim [wrong-codes-a]:
    <k>
      strCodes(str(iCons(97, .IntSeq)))
      =>
      .IntSeq
    </k>
endmodule
