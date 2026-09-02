requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Mathematical count of overlapping occurrences.  The empty pattern occurs
  // at every boundary; a nonempty pattern is tested at every successive suffix.
  syntax Int ::= overlapCount(IntSeq, IntSeq) [function, total]
  syntax IntSeq ::= tailIS(IntSeq) [function, total]

  rule tailIS(.IntSeq) => .IntSeq
  rule tailIS(iCons(_:Int, CS:IntSeq)) => CS

  rule overlapCount(S:IntSeq, P:IntSeq)
    => isLen(S) +Int 1
    requires P ==K .IntSeq

  rule overlapCount(.IntSeq, P:IntSeq)
    => 0
    requires notBool (P ==K .IntSeq)

  rule overlapCount(S:IntSeq, P:IntSeq)
    => (#if startsWith(P, S)
        #then 1 #else 0 #fi)
       +Int overlapCount(tailIS(S), P)
    requires notBool (S ==K .IntSeq)
     andBool notBool (P ==K .IntSeq)

  // Derived slice lemma: taking [1:] of a nonempty code sequence yields its
  // tail.  This is an induction consequence of buildIS/intSeqAt/isLen.
  rule buildIS(
         S:IntSeq,
         clampHi(1, isLen(S), 1),
         isLen(S),
         1)
    => tailIS(S)
    requires notBool (S ==K .IntSeq)
    [simplification]
endmodule
