requires "/tmp/audit-work/86-anti-shuffle/verification.k"

module MODEL-WITNESSES
  imports VERIFICATION

  claim <k> antiShuffleCodes(.IntSeq) => .IntSeq </k>

  claim <k> antiShuffleCodes(iCons(98, iCons(97, .IntSeq)))
     => iCons(97, iCons(98, .IntSeq)) </k>

  claim <k> antiShuffleCodes(
          iCons(97, iCons(32, iCons(32, iCons(98, .IntSeq)))))
     => iCons(97, iCons(32, iCons(32, iCons(98, .IntSeq)))) </k>

  claim <k> antiShuffleCodes(
          iCons(72, iCons(101, iCons(108, iCons(108, iCons(111,
          iCons(32, iCons(87, iCons(111, iCons(114, iCons(108,
          iCons(100, iCons(33, iCons(33, iCons(33, .IntSeq)))))))))))))))
     => iCons(72, iCons(101, iCons(108, iCons(108, iCons(111,
        iCons(32, iCons(33, iCons(33, iCons(33, iCons(87,
        iCons(100, iCons(108, iCons(111, iCons(114, .IntSeq)))))))))))))) </k>
endmodule
