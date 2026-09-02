// verification.k — is_sorted on the UNIFIED semantics. Two SEQUENTIAL adjacent-scans over a
// list of symbolic ints (element comparisons via the isInt applyCmp echo, no dict): a list is
// "sorted" iff it is non-decreasing AND no value occurs > 2 times. For a non-decreasing list the
// latter is exactly "no 3 CONSECUTIVE equal" — so solution.py drops the canonical Counter dict
// for two adjacent scans. See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module IS-SORTED-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // non-decreasing scan: nondec becomes false on any l[i-1] > l[i] (i in [I, N)).
  syntax Bool ::= nondecFold(Int, Int, ValSeq, Bool) [function, total]
  rule nondecFold(I:Int, N:Int, _VS:ValSeq, ND:Bool) => ND requires I >=Int N [simplification]
  rule nondecFold(I:Int, N:Int, VS:ValSeq, _ND:Bool) => nondecFold(I +Int 1, N, VS, false)
    requires I <Int N andBool projectIntTotal(valSeqAt(VS, I -Int 1)) >Int projectIntTotal(valSeqAt(VS, I)) [simplification]
  rule nondecFold(I:Int, N:Int, VS:ValSeq, ND:Bool) => nondecFold(I +Int 1, N, VS, ND)
    requires I <Int N andBool projectIntTotal(valSeqAt(VS, I -Int 1)) <=Int projectIntTotal(valSeqAt(VS, I)) [simplification]

  // no-3-consecutive-equal scan: no3 becomes false when l[i-2]==l[i-1] AND l[i-1]==l[i] (i in [I, N)).
  syntax Bool ::= no3Fold(Int, Int, ValSeq, Bool) [function, total]
  rule no3Fold(I:Int, N:Int, _VS:ValSeq, N3:Bool) => N3 requires I >=Int N [simplification]
  rule no3Fold(I:Int, N:Int, VS:ValSeq, _N3:Bool) => no3Fold(I +Int 1, N, VS, false)
    requires I <Int N
     andBool projectIntTotal(valSeqAt(VS, I -Int 2)) ==Int projectIntTotal(valSeqAt(VS, I -Int 1))
     andBool projectIntTotal(valSeqAt(VS, I -Int 1)) ==Int projectIntTotal(valSeqAt(VS, I)) [simplification]
  rule no3Fold(I:Int, N:Int, VS:ValSeq, N3:Bool) => no3Fold(I +Int 1, N, VS, N3)
    requires I <Int N
     andBool notBool (projectIntTotal(valSeqAt(VS, I -Int 2)) ==Int projectIntTotal(valSeqAt(VS, I -Int 1))
              andBool projectIntTotal(valSeqAt(VS, I -Int 1)) ==Int projectIntTotal(valSeqAt(VS, I))) [simplification]

  // result: non-decreasing AND no value > 2 times.
  syntax Bool ::= isSortedRes(ValSeq) [function]
  rule isSortedRes(VS:ValSeq) => nondecFold(1, vsLen(VS), VS, true) andBool no3Fold(2, vsLen(VS), VS, true) [simplification]
endmodule
