// verification.k — how_many_times on the UNIFIED semantics, TRAP-FREE (P18).
// solution.py is canonical's ONE function; the slice-compare is the sanctioned
// inline window scan (diff-tested). NO interceptions: the inner scan's atoms
// are atI compares; ok folds via winEq, the count via countFold — both guarded
// case-splits over exactly the atoms the INLINE code produces.

requires "../../reference/src/lemmas.k"

module HOW-MANY-TIMES-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // (atI + the intSeqAt bounds bridge are SHARED: lemmas/subscript.k)

  // ---- winEq(SC, SUBC, I, J): the remaining window conjunction from offset J
  syntax Bool ::= winEq(IntSeq, IntSeq, Int, Int) [function, total]
  rule winEq(_SC:IntSeq, SUBC:IntSeq, _I:Int, J:Int) => true
    requires J >=Int isLen(SUBC) [simplification]
  rule winEq(SC:IntSeq, SUBC:IntSeq, I:Int, J:Int) => winEq(SC, SUBC, I, J +Int 1)
    requires 0 <=Int J andBool J <Int isLen(SUBC)
     andBool 0 <=Int I andBool I +Int isLen(SUBC) <=Int isLen(SC)
     andBool atI(SC, I +Int J) ==Int atI(SUBC, J)
    [simplification]
  rule winEq(SC:IntSeq, SUBC:IntSeq, I:Int, J:Int) => false
    requires 0 <=Int J andBool J <Int isLen(SUBC)
     andBool 0 <=Int I andBool I +Int isLen(SUBC) <=Int isLen(SC)
     andBool notBool (atI(SC, I +Int J) ==Int atI(SUBC, J))
    [simplification]

  // ---- count fold over i in [I, N): times += 1 when the window matches
  syntax Int ::= countFold(Int, Int, IntSeq, IntSeq, Int) [function, total]
  rule countFold(I:Int, N:Int, _SC:IntSeq, _SUBC:IntSeq, C:Int) => C
    requires I >=Int N [simplification]
  rule countFold(I:Int, N:Int, SC:IntSeq, SUBC:IntSeq, C:Int)
    => countFold(I +Int 1, N, SC, SUBC, C +Int 1)
    requires I <Int N andBool winEq(SC, SUBC, I, 0) [simplification]
  rule countFold(I:Int, N:Int, SC:IntSeq, SUBC:IntSeq, C:Int)
    => countFold(I +Int 1, N, SC, SUBC, C)
    requires I <Int N andBool notBool winEq(SC, SUBC, I, 0) [simplification]
endmodule
