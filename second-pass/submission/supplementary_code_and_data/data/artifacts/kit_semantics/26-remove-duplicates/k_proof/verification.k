requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The HumanEval type annotation restricts the input elements to integers.
  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq)                => true
  rule allInts(vCons(V:Val, R:ValSeq)) => isInt(V) andBool allInts(R)

  // Mathematical result of processing REST while preserving the already-built
  // prefix ACC.  ALL is the complete original input used by list.count.
  syntax ValSeq ::= rdAcc(ValSeq, ValSeq, ValSeq) [function, total]
  rule rdAcc(ACC:ValSeq, .ValSeq, _ALL:ValSeq) => ACC
  rule rdAcc(ACC:ValSeq, vCons(V:Val, R:ValSeq), ALL:ValSeq)
    => #if 1 ==Int cntOccVS(ALL, V)
       #then rdAcc(valSeqConcat(ACC, vCons(V, .ValSeq)), R, ALL)
       #else rdAcc(ACC, R, ALL)
       #fi
endmodule
