// verification.k — make_palindrome on the UNIFIED semantics, TRAP-FREE (P10).
// solution.py is canonical's TWO functions; make_palindrome performs a REAL
// is_palindrome call per while-search step (the call-in-loop rung, Probe A) on
// the REAL suffix slice. The three slice forms ride the REAL doSlice/buildIS
// route; the SHARED lemmas (lemmas/subscript.k) reduce them to take/drop/rev
// terms — the clamped suffix/prefix identities hold for every B >= 0, so no
// length bound enters the while claims (the co-inductive premise stays
// re-derivable at B+1).

requires "../../reference/src/lemmas.k"

module MAKE-PALINDROME-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // atI + the intSeqAt bounds bridge are SHARED now (lemmas/subscript.k)

  // ---- palAcc(CS, LO, HI): two-pointer mirror scan with GUARD-level compares
  syntax Bool ::= palAcc(IntSeq, Int, Int) [function, total]
  rule palAcc(_CS:IntSeq, LO:Int, HI:Int) => true requires LO >=Int HI [simplification]
  rule palAcc(CS:IntSeq, LO:Int, HI:Int) => palAcc(CS, LO +Int 1, HI -Int 1)
    requires 0 <=Int LO andBool LO <Int HI andBool HI <Int isLen(CS)
     andBool atI(CS, LO) ==Int atI(CS, HI)
    [simplification]
  rule palAcc(CS:IntSeq, LO:Int, HI:Int) => false
    requires 0 <=Int LO andBool LO <Int HI andBool HI <Int isLen(CS)
     andBool notBool (atI(CS, LO) ==Int atI(CS, HI))
    [simplification]

  // sticky-ok conjunction the callee loop leaves (claim A's postform)
  syntax Bool ::= palFold(IntSeq, Int, Int, Bool) [function, total]
  rule palFold(_CS:IntSeq, LO:Int, HI:Int, OK:Bool) => OK requires LO >=Int HI [simplification]
  rule palFold(CS:IntSeq, LO:Int, HI:Int, OK:Bool)
    => palFold(CS, LO +Int 1, HI -Int 1, OK)
    requires 0 <=Int LO andBool LO <Int HI andBool HI <Int isLen(CS)
     andBool atI(CS, LO) ==Int atI(CS, HI)
    [simplification]
  rule palFold(CS:IntSeq, LO:Int, HI:Int, OK:Bool) => false
    requires 0 <=Int LO andBool LO <Int HI andBool HI <Int isLen(CS)
     andBool notBool (atI(CS, LO) ==Int atI(CS, HI))
    [simplification]
  // false absorbs (sticky ok never recovers)
  rule palFold(_CS:IntSeq, _LO:Int, _HI:Int, false) => false [simplification]

  // starting from true over a suffix, the sticky fold IS the mirror scan
  rule palFold(CS:IntSeq, LO:Int, HI:Int, true) => palAcc(CS, LO, HI)
    requires 0 <=Int LO [simplification]

  // ---- the while-search: first b whose suffix is a palindrome (partial;
  // the co-inductive while-search rung — case-split per step, no measure)
  // guards over the RAW execution atom (len of the suffix stays opaque — no
  // length bound is needed anywhere, which keeps the circularity premise
  // re-derivable at B+1)
  syntax Int ::= firstPal(IntSeq, Int) [function]
  rule firstPal(CS:IntSeq, B:Int) => B
    requires palAcc(dropIS(CS, B), 0, isLen(dropIS(CS, B)) -Int 1) [simplification]
  rule firstPal(CS:IntSeq, B:Int) => firstPal(CS, B +Int 1)
    requires notBool palAcc(dropIS(CS, B), 0, isLen(dropIS(CS, B)) -Int 1) [simplification]

  // firstPal's result never precedes its start (on its defined domain);
  // both hooked spellings
  rule firstPal(_CS:IntSeq, B:Int) >=Int C:Int => true
    requires B >=Int C [simplification]
  rule C:Int <=Int firstPal(_CS:IntSeq, B:Int) => true
    requires B >=Int C [simplification]

  // ---- the whole result
  syntax Val ::= mpRes(IntSeq) [function]
  // guard form, not a constructor match: the shared equation shaping spells
  // the empty-branch path condition isLen(CS) ==Int 0, which never narrows
  // CS to the .IntSeq constructor
  rule mpRes(CS:IntSeq) => str(.IntSeq)
    requires isLen(CS) ==Int 0 [simplification]
  rule mpRes(CS:IntSeq) => str(seqConcat(CS, revIS(takeIS(CS, firstPal(CS, 0)))))
    requires notBool (isLen(CS) ==Int 0) [simplification]
endmodule
