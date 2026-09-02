// verification.k — Probe B: heap-list builders (de-escape rework Task 4/5).
// Two builder styles over the heap semantics: .append (in-place write, fixed ref,
// heap rest untouched) and `out = out + [i]` (two allocations per iteration —
// the invariant must absorb heap garbage via keysBelow).

requires "../../src/lemmas.k"

module HEAP-APPEND-PROBE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // squares appended for i in [I, N)
  syntax ValSeq ::= sqFold(Int, Int, ValSeq) [function, total]
  rule sqFold(I:Int, N:Int, ACC:ValSeq) => ACC
    requires I >=Int N
    [simplification]
  rule sqFold(I:Int, N:Int, ACC:ValSeq)
    => sqFold(I +Int 1, N, valSeqConcat(ACC, vCons(I *Int I, .ValSeq)))
    requires I <Int N
    [simplification]

  // indices concatenated for i in [I, N)
  syntax ValSeq ::= plusFold(Int, Int, ValSeq) [function, total]
  rule plusFold(I:Int, N:Int, ACC:ValSeq) => ACC
    requires I >=Int N
    [simplification]
  rule plusFold(I:Int, N:Int, ACC:ValSeq)
    => plusFold(I +Int 1, N, valSeqConcat(ACC, vCons(I, .ValSeq)))
    requires I <Int N
    [simplification]
endmodule
