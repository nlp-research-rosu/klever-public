requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // sequenceAcc(ACC, I, N) is the exact character-code accumulator after
  // running the source loop from counter I through bound N.
  syntax IntSeq ::= sequenceAcc(IntSeq, Int, Int) [function, total]

  rule sequenceAcc(ACC, I, N) => ACC
    requires I >Int N
    [concrete, simplification]

  rule sequenceAcc(ACC, I, N)
    => sequenceAcc(
         seqConcat(
           seqConcat(ACC, iCons(32, .IntSeq)),
           strToCodes(Int2String(I))),
         I +Int 1,
         N)
    requires I <=Int N
    [concrete, simplification]

  // Symbolic base and inductive fold.  The recursive defining equation above
  // is concrete-only so it cannot unfold forever on a symbolic counter.
  rule sequenceAcc(ACC, I, N) => ACC
    requires I >Int N
    [simplification]

  rule sequenceAcc(
         seqConcat(
           seqConcat(ACC, iCons(32, .IntSeq)),
           strToCodes(Int2String(I))),
         I +Int 1,
         N)
    => sequenceAcc(ACC, I, N)
    requires I <=Int N
    [simplification]

  // Complete result for every integer input.  The negative case matches
  // Python's range(n + 1) convention and makes the source contract total.
  syntax IntSeq ::= stringSequenceCodes(Int) [function, total]

  rule stringSequenceCodes(N) => .IntSeq
    requires N <Int 0

  rule stringSequenceCodes(N)
    => sequenceAcc(iCons(48, .IntSeq), 1, N)
    requires N >=Int 0
endmodule
