requires "verification.k"

module AUDIT-FIXED-LENGTH-WITNESS
  imports VERIFICATION-BASE

  claim [fixed-one]:
    <k> seqLen(str(iCons(97, .IntSeq))) => 1 </k>

  claim [fixed-two]:
    <k> seqLen(str(iCons(98, iCons(98, .IntSeq)))) => 2 </k>

  claim [twin-one]:
    <k> seqLenString(projectString(str(iCons(97, .IntSeq)))) => 1 </k>

  claim [twin-two]:
    <k>
      seqLenString(projectString(str(iCons(98, iCons(98, .IntSeq)))))
      => 2
    </k>
endmodule
