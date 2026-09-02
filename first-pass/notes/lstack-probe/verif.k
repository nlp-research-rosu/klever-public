// verif.k — a MINIMAL probe to isolate why a counter loop proof stalled under <lstack>.
//
// It has TWO loops that share BYTE-IDENTICAL loop-control machinery (same <lstack>, same
// #iterEnd / #loopDone). The ONLY structural difference is how each advances:
//   - cLoop(I, N)  : a COUNTER (I climbs to N)           — arithmetic recursion
//   - sLoop(S)     : a cons-list S                        — structural recursion
//
// And it defines FOUR summaries, so the spec files can vary exactly one thing at a time:
//   - sumTo(I,N)            : counter recursion, additive — [function] (NOT total: increasing arg)
//   - seqSum(S)             : list recursion,    additive — [function, total]
//   - seqSumNT(S)           : list recursion,    additive — [function] (the SAME rules as seqSum,
//                                                            just NOT marked total — the control)
//   - sumToAcc(I,N,ACC)     : counter recursion, THREADED — [function] (non-total, accumulator-passing)
//
// Build:
//   kompile verif.k --backend haskell --main-module VERIF --syntax-module VERIF \
//     --output-definition verif-kompiled

module VERIF
  imports INT
  imports BOOL
  imports LIST
  imports K-EQUAL

  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
  syntax LFrame ::= lframe(K, K)                      // (after-loop continuation, next-iteration resume)
  syntax KItem  ::= "#iterEnd" | "#loopDone" | cLoop(Int, Int) | sLoop(IntSeq)

  configuration <k> $PGM:K </k> <acc> 0 </acc> <lstack> .List </lstack>

  // ---- COUNTER loop: advance = a counter (I -> I+1 until I >= N) ----
  rule <k> cLoop(I:Int, N:Int) => #iterEnd ... </k>
       <acc> A:Int => A +Int I </acc>
       <lstack> ListItem(lframe(D:K, _) => lframe(D, cLoop(I +Int 1, N))) ... </lstack>
       requires I <Int N
  rule <k> cLoop(I:Int, N:Int) => #loopDone ... </k> requires notBool (I <Int N)

  // ---- SEQUENCE loop: advance = structural cons (R is structurally smaller than iCons(X,R)) ----
  rule <k> sLoop(iCons(X:Int, R:IntSeq)) => #iterEnd ... </k>
       <acc> A:Int => A +Int X </acc>
       <lstack> ListItem(lframe(D:K, _) => lframe(D, sLoop(R))) ... </lstack>
  rule <k> sLoop(.IntSeq) => #loopDone ... </k>

  // ---- IDENTICAL loop control for BOTH (this is the RV-style <lstack> resume model) ----
  rule <k> #iterEnd  => RESUME </k> <lstack> ListItem(lframe(_, RESUME:K)) ... </lstack>
  rule <k> #loopDone => DONE   </k> <lstack> ListItem(lframe(DONE:K, _)) => .List ... </lstack>

  // ==== summaries ============================================================
  // sumTo: sum of [I, N). Recurses on the INCREASING arg I+1 -> K cannot accept [total].
  syntax Int ::= sumTo(Int, Int) [function]
  rule sumTo(I:Int, N:Int) => 0 requires notBool (I <Int N) [simplification]
  rule sumTo(I:Int, N:Int) => I +Int sumTo(I +Int 1, N) requires I <Int N [simplification]
  rule #Ceil(sumTo(_:Int, _:Int)) => #Top [simplification]

  // seqSum: sum of a list. Recurses on the SMALLER arg R -> [total].
  syntax Int ::= seqSum(IntSeq) [function, total]
  rule seqSum(.IntSeq) => 0 [simplification]
  rule seqSum(iCons(X:Int, R:IntSeq)) => X +Int seqSum(R) [simplification]

  // seqSumNT: IDENTICAL rules to seqSum, but NOT marked [total] (the control variable).
  syntax Int ::= seqSumNT(IntSeq) [function]
  rule seqSumNT(.IntSeq) => 0 [simplification]
  rule seqSumNT(iCons(X:Int, R:IntSeq)) => X +Int seqSumNT(R) [simplification]
  rule #Ceil(seqSumNT(_:IntSeq)) => #Top [simplification]

  // sumToAcc: same counter sum, but THREADED (accumulator passed in), so the inductive step's
  // term equals the unfold syntactically — no associativity is ever needed.
  syntax Int ::= sumToAcc(Int, Int, Int) [function]
  rule sumToAcc(I:Int, N:Int, ACC:Int) => ACC requires notBool (I <Int N) [simplification]
  rule sumToAcc(I:Int, N:Int, ACC:Int) => sumToAcc(I +Int 1, N, ACC +Int I) requires I <Int N [simplification]
  rule #Ceil(sumToAcc(_:Int, _:Int, _:Int)) => #Top [simplification]
endmodule
