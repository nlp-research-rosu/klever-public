requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The number still to be added when CS remains to be iterated and LAST is
  // the previous one-character string (or .IntSeq before the first step).
  // These equations are exhaustive and constructor-disjoint on IntSeq.
  syntax Int ::= vowelsTail(IntSeq, IntSeq) [function, total]

  rule vowelsTail(.IntSeq, LAST)
    => intOf(LAST ==K iCons(121, .IntSeq))
       +Int intOf(LAST ==K iCons(89, .IntSeq))

  rule vowelsTail(iCons(C, REST), _LAST)
    => intOf(strContains(
         iCons(C, .IntSeq),
         iCons(97,
         iCons(101,
         iCons(105,
         iCons(111,
         iCons(117,
         iCons(65,
         iCons(69,
         iCons(73,
         iCons(79,
         iCons(85, .IntSeq))))))))))))
       +Int vowelsTail(REST, iCons(C, .IntSeq))
endmodule
