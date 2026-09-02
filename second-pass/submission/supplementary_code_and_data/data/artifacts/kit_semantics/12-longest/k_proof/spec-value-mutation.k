requires "verification.k"

module SPEC-VALUE-MUTATION
  imports VERIFICATION-BASE

  // Deliberately false opposite interpretation: a one-code-point string does
  // not have length zero.
  claim [false-string-length]:
    <k>
      seqLenString(projectString(str(iCons(97, .IntSeq))))
      => 0
    </k>
endmodule
