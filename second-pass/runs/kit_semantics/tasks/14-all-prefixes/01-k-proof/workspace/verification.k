requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Starting with a prefix P and an already-built output ACC, consume the
  // remaining character codes and append each successively longer prefix.
  syntax ValSeq ::= prefixesAcc(IntSeq, IntSeq, ValSeq) [function, total]
  rule prefixesAcc(_P:IntSeq, .IntSeq, ACC:ValSeq) => ACC
  rule prefixesAcc(P:IntSeq, iCons(C:Int, R:IntSeq), ACC:ValSeq)
    => prefixesAcc(
         seqConcat(P, iCons(C, .IntSeq)),
         R,
         valSeqConcat(
           ACC,
           vCons(str(seqConcat(P, iCons(C, .IntSeq))), .ValSeq)))

  // These two summaries describe the function-local variables left by a
  // completed for-loop. They do not replace execution.
  syntax IntSeq ::= finishPrefix(IntSeq, IntSeq) [function, total]
  rule finishPrefix(P:IntSeq, .IntSeq) => P
  rule finishPrefix(P:IntSeq, iCons(C:Int, R:IntSeq))
    => finishPrefix(seqConcat(P, iCons(C, .IntSeq)), R)

  syntax Val ::= finishChar(Val, IntSeq) [function, total]
  rule finishChar(CH:Val, .IntSeq) => CH
  rule finishChar(_CH:Val, iCons(C:Int, R:IntSeq))
    => finishChar(str(iCons(C, .IntSeq)), R)
endmodule
