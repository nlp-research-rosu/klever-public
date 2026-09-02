requires "/tmp/audit-work/27-flip-case/candidate/reference-semantics/semantics.k"

module UNICODE-MODEL-WITNESS
  imports MPY

  // The supplied map is deliberately ASCII-only: U+00E9 and U+00DF remain
  // unchanged even though Python's Unicode swapcase changes them.
  claim
    <k> mapSwap(iCons(233, .IntSeq)) => iCons(233, .IntSeq) </k>
  claim
    <k> mapSwap(iCons(223, .IntSeq)) => iCons(223, .IntSeq) </k>
endmodule
