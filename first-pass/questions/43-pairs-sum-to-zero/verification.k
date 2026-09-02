// verification.k — pairs_sum_to_zero on the UNIFIED semantics. First ELEMENT-based nested-loop
// proof: the inner comparison l[i]+l[j]==0 is arithmetic on SYMBOLIC list elements. That is the
// "isInt wall" — cracked here by the allInt-guarded applyBin ECHO (differential-proven in
// reference/notes/isint-bridge-probe). solution.py rewrites the early `return True` as a sticky
// `found` accumulator (index-based nested loop). See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module PAIRS-SUM-TO-ZERO-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // ---- inner fold over j in [J, N): found becomes true if any pair (i, j) sums to 0 (i fixed).
  // Case-split GUARDED rules (the primeAcc/#31 pattern) — the guard is the program's If condition
  // l[i]+l[j]==0 inlined (after the echo reduces the sum), so each If branch discharges the
  // matching rule's guard from its path condition. A single `F orBool (sum==0)` rule does NOT
  // work: kprove won't simplify orBool with a symbolic Bool in the implication check.
  syntax Bool ::= innerFold(Int, Int, Int, ValSeq, Bool) [function, total]
  rule innerFold(J:Int, N:Int, _I:Int, _VS:ValSeq, F:Bool) => F requires J >=Int N [simplification]
  rule innerFold(J:Int, N:Int, I:Int, VS:ValSeq, _F:Bool) => innerFold(J +Int 1, N, I, VS, true)
    requires J <Int N andBool (projectIntTotal(valSeqAt(VS, I)) +Int projectIntTotal(valSeqAt(VS, J))) ==Int 0 [simplification]
  rule innerFold(J:Int, N:Int, I:Int, VS:ValSeq, F:Bool) => innerFold(J +Int 1, N, I, VS, F)
    requires J <Int N andBool (projectIntTotal(valSeqAt(VS, I)) +Int projectIntTotal(valSeqAt(VS, J))) =/=Int 0 [simplification]

  // ---- outer fold over i in [I, N): each runs the inner fold over (i+1, N). -----------------
  syntax Bool ::= outerFold(Int, Int, ValSeq, Bool) [function, total]
  rule outerFold(I:Int, N:Int, _VS:ValSeq, F:Bool) => F requires I >=Int N [simplification]
  rule outerFold(I:Int, N:Int, VS:ValSeq, F:Bool)
    => outerFold(I +Int 1, N, VS, innerFold(I +Int 1, N, I, VS, F)) requires I <Int N [simplification]

  // result: does any i < j have l[i] + l[j] == 0?
  syntax Bool ::= pairsRes(ValSeq) [function]
  rule pairsRes(VS:ValSeq) => outerFold(0, vsLen(VS), VS, false) [simplification]
endmodule
