requires "verification.k"

module AUDIT-SUMMARY
  imports VERIFICATION-BASE

  syntax Module ::= "summaryEmpty" | "summaryBaAb" | "insertAB"

  rule <k> #loadAll(summaryEmpty)
        => str(antiFinish(.IntSeq, .IntSeq, .IntSeq)) ... </k>

  rule <k> #loadAll(summaryBaAb)
        => str(antiFinish(
             .IntSeq,
             .IntSeq,
             iCons(98, iCons(97, iCons(32, iCons(97, iCons(98, .IntSeq))))))) ... </k>

  rule <k> #loadAll(insertAB)
        => str(insertFinish(.IntSeq, 97, iCons(98, .IntSeq))) ... </k>
endmodule
