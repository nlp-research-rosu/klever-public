requires "verification.k"

module IS-SORTED-GROUND-SPEC
  imports IS-SORTED-VERIFICATION

  claim <k> scanResult(scanAll(true, 0, 0, .IntSeq)) => true </k>
  claim <k> scanResult(scanAll(true, 0, 0,
          iCons(0, iCons(0, .IntSeq)))) => true </k>
  claim <k> scanResult(scanAll(true, 0, 0,
          iCons(0, iCons(0, iCons(0, .IntSeq))))) => false </k>
  claim <k> scanResult(scanAll(true, 0, 0,
          iCons(1, iCons(0, .IntSeq)))) => false </k>
  claim <k> scanResult(scanAll(true, 0, 0,
          iCons(1, iCons(2, iCons(2, .IntSeq))))) => true </k>
endmodule
