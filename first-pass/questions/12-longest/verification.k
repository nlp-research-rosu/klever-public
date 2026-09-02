// verification.k — summary for the longest proof, on the UNIFIED semantics.
// List-of-strings reduce with an Optional (None) accumulator: the first string of
// maximum length, or None if empty. Reuses the codesProj Str projection.

requires "../../reference/src/lemmas.k"

module LONGEST-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // select(B, V): keep V iff B is None or V is strictly longer than B, else keep B
  // (so a tie keeps the earlier B — the FIRST longest).
  // All-simplification so it fires during implication checking; branch on B ==K noneV
  // (partitions every Val, so [total]).
  syntax Val ::= select(Val, Val) [function, total]
  rule select(B:Val, V:Val) => V
    requires B ==K noneV [simplification]
  rule select(B:Val, V:Val) => V
    requires notBool (B ==K noneV) andBool isLen(codesProj(V)) >Int isLen(codesProj(B)) [simplification]
  rule select(B:Val, V:Val) => B
    requires notBool (B ==K noneV) andBool notBool (isLen(codesProj(V)) >Int isLen(codesProj(B))) [simplification]

  // longestReduce(VS, B) = fold select over VS from accumulator B.
  syntax Val ::= longestReduce(ValSeq, Val) [function, total]
  rule longestReduce(.ValSeq, B:Val) => B [simplification]
  rule longestReduce(vCons(V:Val, S:ValSeq), B:Val) => longestReduce(S, select(B, V)) [simplification]
endmodule
