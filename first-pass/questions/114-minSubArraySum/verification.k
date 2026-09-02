// verification.k — summary for the minSubArraySum (Kadane, minimum) proof, UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module MIN-SUBARRAY-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // Kadane's two coupled accumulators for the MINIMUM sub-array sum, threaded with a FIRST
  // flag so the seed (nums[0]) is skipped (cur/best already = nums[0]).
  //   first=true  : skip this element (flip first only).
  //   first=false : newCur = min(X, CUR+X); newBest = min(newCur, BEST).
  // cur/best are Vals: the `cur = x` branch keeps the RAW element X (the semantics assigns
  // it unprojected), the `cur = cur + x` branch yields the Int projectIntTotal(CUR) +Int
  // projectIntTotal(X). Comparisons project. curK/bestK share the recursion, differ only in
  // the base case. Both are scope-map values, so both [total].

  syntax Val ::= curK(ValSeq, Val, Val, Bool) [function, total]
  rule curK(.ValSeq, CUR:Val, _BEST:Val, _F:Bool) => CUR [simplification]
  rule curK(vCons(_X:Val, R:ValSeq), CUR:Val, BEST:Val, true) => curK(R, CUR, BEST, false) [simplification]
  rule curK(vCons(X:Val, R:ValSeq), CUR:Val, BEST:Val, false) => curK(R, X, X, false)
    requires projectIntTotal(X) <Int (projectIntTotal(CUR) +Int projectIntTotal(X)) andBool projectIntTotal(X) <Int projectIntTotal(BEST) [simplification]
  rule curK(vCons(X:Val, R:ValSeq), CUR:Val, BEST:Val, false) => curK(R, X, BEST, false)
    requires projectIntTotal(X) <Int (projectIntTotal(CUR) +Int projectIntTotal(X)) andBool notBool (projectIntTotal(X) <Int projectIntTotal(BEST)) [simplification]
  rule curK(vCons(X:Val, R:ValSeq), CUR:Val, BEST:Val, false) => curK(R, projectIntTotal(CUR) +Int projectIntTotal(X), projectIntTotal(CUR) +Int projectIntTotal(X), false)
    requires notBool (projectIntTotal(X) <Int (projectIntTotal(CUR) +Int projectIntTotal(X))) andBool (projectIntTotal(CUR) +Int projectIntTotal(X) <Int projectIntTotal(BEST)) [simplification]
  rule curK(vCons(X:Val, R:ValSeq), CUR:Val, BEST:Val, false) => curK(R, projectIntTotal(CUR) +Int projectIntTotal(X), BEST, false)
    requires notBool (projectIntTotal(X) <Int (projectIntTotal(CUR) +Int projectIntTotal(X))) andBool notBool (projectIntTotal(CUR) +Int projectIntTotal(X) <Int projectIntTotal(BEST)) [simplification]

  syntax Val ::= bestK(ValSeq, Val, Val, Bool) [function, total]
  rule bestK(.ValSeq, _CUR:Val, BEST:Val, _F:Bool) => BEST [simplification]
  rule bestK(vCons(_X:Val, R:ValSeq), CUR:Val, BEST:Val, true) => bestK(R, CUR, BEST, false) [simplification]
  rule bestK(vCons(X:Val, R:ValSeq), CUR:Val, BEST:Val, false) => bestK(R, X, X, false)
    requires projectIntTotal(X) <Int (projectIntTotal(CUR) +Int projectIntTotal(X)) andBool projectIntTotal(X) <Int projectIntTotal(BEST) [simplification]
  rule bestK(vCons(X:Val, R:ValSeq), CUR:Val, BEST:Val, false) => bestK(R, X, BEST, false)
    requires projectIntTotal(X) <Int (projectIntTotal(CUR) +Int projectIntTotal(X)) andBool notBool (projectIntTotal(X) <Int projectIntTotal(BEST)) [simplification]
  rule bestK(vCons(X:Val, R:ValSeq), CUR:Val, BEST:Val, false) => bestK(R, projectIntTotal(CUR) +Int projectIntTotal(X), projectIntTotal(CUR) +Int projectIntTotal(X), false)
    requires notBool (projectIntTotal(X) <Int (projectIntTotal(CUR) +Int projectIntTotal(X))) andBool (projectIntTotal(CUR) +Int projectIntTotal(X) <Int projectIntTotal(BEST)) [simplification]
  rule bestK(vCons(X:Val, R:ValSeq), CUR:Val, BEST:Val, false) => bestK(R, projectIntTotal(CUR) +Int projectIntTotal(X), BEST, false)
    requires notBool (projectIntTotal(X) <Int (projectIntTotal(CUR) +Int projectIntTotal(X))) andBool notBool (projectIntTotal(CUR) +Int projectIntTotal(X) <Int projectIntTotal(BEST)) [simplification]
endmodule
