requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  syntax Bool ::= sameIntLists(ValSeq, ValSeq) [function, total]
  rule sameIntLists(.ValSeq, PREDICTIONS:ValSeq)
    => PREDICTIONS ==K .ValSeq
  rule sameIntLists(vCons(_:Val, _:ValSeq), .ValSeq) => false
  rule sameIntLists(
         vCons(SCORE:Val, SCORES:ValSeq),
         vCons(PREDICTED:Val, PREDICTIONS:ValSeq))
    => isInt(SCORE)
       andBool isInt(PREDICTED)
       andBool notBool isRefV(SCORE)
       andBool notBool isRefV(PREDICTED)
       andBool notBool isRefV(applyBin("-", SCORE, PREDICTED))
       andBool sameIntLists(SCORES, PREDICTIONS)

  syntax ValSeq ::= compareAcc(ValSeq, ValSeq, ValSeq) [function]
  rule compareAcc(ACC:ValSeq, .ValSeq, .ValSeq) => ACC
  rule compareAcc(ACC:ValSeq,
                  vCons(SCORE:Val, SCORES:ValSeq),
                  vCons(PREDICTED:Val, PREDICTIONS:ValSeq))
    => compareAcc(
         valSeqConcat(
           ACC,
           vCons(
             applyBuiltin(
               "abs",
               applyBin("-", SCORE, PREDICTED),
               .Vals),
             .ValSeq)),
         SCORES,
         PREDICTIONS)
endmodule
