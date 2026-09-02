// verification.k — triples_sum_to_zero on the UNIFIED semantics. TRIPLE nested loop; extends
// 43 pairs_sum_to_zero. The inner test l[i]+l[j]+l[k]==0 is arithmetic on THREE symbolic list
// elements. Two allInt-guarded applyBin echoes reduce it: (a) both-elements l[i]+l[j], and
// (b) Int+element (the partial sum) + l[k]. solution.py rewrites the early `return True` as a
// sticky `found` accumulator (index-based triple loop). See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module TRIPLES-SUM-TO-ZERO-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // ---- isInt-bridge echoes under allInt (SOUND: all elements are ints). applyBin is a function
  // symbol → legal [simplification] LHS. (a) both operands are elements; (b) one operand is
  // already an Int (a partial sum) and the other is an element — needed for the LEFT-assoc triple
  // sum (l[i]+l[j])+l[k].

  // ---- innermost k-fold over k in [K, N): found becomes true if l[i]+l[j]+l[k] == 0 (i,j fixed).
  // Guarded case-split (the primeAcc/#31 + #43 pattern); guard = the program's If condition inlined
  // after the echoes reduce the left-assoc triple sum.
  syntax Bool ::= kFold(Int, Int, Int, Int, ValSeq, Bool) [function, total]
  rule kFold(K:Int, N:Int, _I:Int, _J:Int, _VS:ValSeq, F:Bool) => F requires K >=Int N [simplification]
  rule kFold(K:Int, N:Int, I:Int, J:Int, VS:ValSeq, _F:Bool) => kFold(K +Int 1, N, I, J, VS, true)
    requires K <Int N
     andBool (projectIntTotal(valSeqAt(VS, I)) +Int projectIntTotal(valSeqAt(VS, J)) +Int projectIntTotal(valSeqAt(VS, K))) ==Int 0
    [simplification]
  rule kFold(K:Int, N:Int, I:Int, J:Int, VS:ValSeq, F:Bool) => kFold(K +Int 1, N, I, J, VS, F)
    requires K <Int N
     andBool (projectIntTotal(valSeqAt(VS, I)) +Int projectIntTotal(valSeqAt(VS, J)) +Int projectIntTotal(valSeqAt(VS, K))) =/=Int 0
    [simplification]

  // ---- middle j-fold over j in [J, N): each runs the k-fold from k = j+1 (i fixed). ----------
  syntax Bool ::= jFold(Int, Int, Int, ValSeq, Bool) [function, total]
  rule jFold(J:Int, N:Int, _I:Int, _VS:ValSeq, F:Bool) => F requires J >=Int N [simplification]
  rule jFold(J:Int, N:Int, I:Int, VS:ValSeq, F:Bool)
    => jFold(J +Int 1, N, I, VS, kFold(J +Int 1, N, I, J, VS, F)) requires J <Int N [simplification]

  // ---- outer i-fold over i in [I, N): each runs the j-fold from j = i+1. ----------------------
  syntax Bool ::= iFold(Int, Int, ValSeq, Bool) [function, total]
  rule iFold(I:Int, N:Int, _VS:ValSeq, F:Bool) => F requires I >=Int N [simplification]
  rule iFold(I:Int, N:Int, VS:ValSeq, F:Bool)
    => iFold(I +Int 1, N, VS, jFold(I +Int 1, N, I, VS, F)) requires I <Int N [simplification]

  // result: does any i < j < k have l[i] + l[j] + l[k] == 0?
  syntax Bool ::= triplesRes(ValSeq) [function]
  rule triplesRes(VS:ValSeq) => iFold(0, vsLen(VS), VS, false) [simplification]
endmodule
