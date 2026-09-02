requires "verification.k"

module AUDIT-OPPOSITE-LENGTH
  imports VERIFICATION-BASE

  claim [false-opposite]:
    <k>
      seqLenString(projectString(str(iCons(97, .IntSeq))))
      => 0
    </k>
endmodule
