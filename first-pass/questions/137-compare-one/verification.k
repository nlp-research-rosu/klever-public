// verification.k — compare_one on the UNIFIED semantics, TRAP-FREE (P137).
// solution.py is canonical verbatim: real tuple-unpack, real isinstance +
// str.replace, real float() calls, real ==/> compares, real IfExp. The four
// keq/kgt Call traps are GONE. Trust boundary: fkeyF (the float() value) and
// fcmpI (the 3-way float comparator SIGN in {-1,0,1}) are opaque primitives; krun runs the real parse/compare.

requires "../../reference/src/lemmas.k"

module COMPARE-ONE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // float() runs the REAL shared rules (decStrToF on structural strs,
  // intToF on int vars, identity on floats); the compares reduce via
  // entailment-gated echoes onto the SHARED eqF/gtF atoms (P81 class)
  rule projectFloatTotal(F:Float) => F [simplification]
  syntax Bool ::= knownFK(Val) [function, total, no-evaluators]
  rule knownFK(F:Float)               => true  [simplification]
  rule knownFK(intToF(_:Int))         => true  [simplification]
  rule knownFK(decStrToF(_:IntSeq))   => true  [simplification]
  rule knownFK(str(_:IntSeq))         => false [simplification]
  // (Float compares reduce via the SHARED k-cell lemmas: lemmas/float.k)

  // the post-replace temp value and its float key, per input constructor
  syntax Val ::= tKey(Val) [function, total]
  rule tKey(I:Int)          => I
  rule tKey(F:Float)        => F
  rule tKey(str(CS:IntSeq)) => str(replaceC(CS, 44, 46))
  syntax Float ::= fk(Val) [function, total]
  rule fk(I:Int)          => intToF(I)
  rule fk(F:Float)        => F
  rule fk(str(CS:IntSeq)) => decStrToF(CS)

  // the result: 3-way select over the shared compare atoms
  syntax Val ::= compareRes(Val, Val) [function, total]
  rule compareRes(A:Val, B:Val) => noneV
    requires eqF(fk(tKey(A)), fk(tKey(B))) [simplification]
  rule compareRes(A:Val, B:Val) => A
    requires notBool eqF(fk(tKey(A)), fk(tKey(B)))
     andBool gtF(fk(tKey(A)), fk(tKey(B))) [simplification]
  rule compareRes(A:Val, B:Val) => B
    requires notBool eqF(fk(tKey(A)), fk(tKey(B)))
     andBool notBool gtF(fk(tKey(A)), fk(tKey(B))) [simplification]
endmodule
