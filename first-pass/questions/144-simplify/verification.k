// verification.k — simplify on the UNIFIED semantics, TRAP-FREE (P144).
// solution.py is canonical verbatim: real split('/') unpacks, real int()
// parses, real products, and the real numerator/denom == int(numerator/denom)
// float wholeness test. The numer/denom helpers (and their Call traps) are
// GONE. Trust = pfI (int() of a field), mulI (product), fdivF (true
// division), truncI (int() of a float), eqWhole (the wholeness SIGN, compared
// ==Int so #branch splits). All PC atoms are PARTIAL-FREE.

requires "../../reference/src/lemmas.k"

module SIMPLIFY-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // ---- total split vocabulary, separator-parameterized (P124 kit) ----------
  syntax Int ::= splitCountC(IntSeq, Int) [function, total]
  rule splitCountC(.IntSeq, _:Int)                => 1
  rule splitCountC(iCons(C:Int, T:IntSeq), S:Int) => 1 +Int splitCountC(T, S) requires C ==Int S
  rule splitCountC(iCons(C:Int, T:IntSeq), S:Int) => splitCountC(T, S)        requires C =/=Int S
  syntax IntSeq ::= takeFieldC(IntSeq, Int) [function, total]
  rule takeFieldC(.IntSeq, _:Int)                => .IntSeq
  rule takeFieldC(iCons(C:Int, _), S:Int)        => .IntSeq requires C ==Int S
  rule takeFieldC(iCons(C:Int, T:IntSeq), S:Int) => iCons(C, takeFieldC(T, S)) requires C =/=Int S
  syntax IntSeq ::= fieldSeqC(Int, IntSeq, Int) [function, total]
  rule fieldSeqC(0, CS:IntSeq, S:Int)                  => takeFieldC(CS, S)
  rule fieldSeqC(I:Int, .IntSeq, _:Int)                => .IntSeq requires I >Int 0
  rule fieldSeqC(I:Int, iCons(C:Int, T:IntSeq), S:Int) => fieldSeqC(I -Int 1, T, S) requires I >Int 0 andBool C ==Int S
  rule fieldSeqC(I:Int, iCons(C:Int, T:IntSeq), S:Int) => fieldSeqC(I, T, S)        requires I >Int 0 andBool C =/=Int S

  // a 2-field '/'-split IS the cons of its two fields
  rule splitSep(CS:IntSeq, 47, .IntSeq)
    => vCons(str(fieldSeqC(0, CS, 47)), vCons(str(fieldSeqC(1, CS, 47)), .ValSeq))
    requires splitCountC(CS, 47) ==Int 2 [simplification]

  // ---- real vocabulary via entailment-gated echoes (P81/P124 class) ---------
  // int(field) is the REAL Horner fold under the entry's digit-domain atoms
  rule applyBuiltin("int", str(F:IntSeq), .Vals) => intDigAcc(F, 0)
    requires notBool (isLen(F) ==Int 0) andBool dgN(F) ==Int 1 [simplification]
  rule projectIntTotal(intDigAcc(F:IntSeq, A:Int)) => intDigAcc(F, A) [simplification]
  rule projectFloatTotal(F:Float) => F [simplification]

  // the products (the shared * rule cannot match opaque-term args)
  syntax Bool ::= knownPF(Val) [function, total, no-evaluators]
  rule knownPF(intDigAcc(_:IntSeq, _:Int)) => true  [simplification]
  rule knownPF(str(_:IntSeq))              => false [simplification]
  rule applyBin("*", V:Val, W:Val) => projectIntTotal(V) *Int projectIntTotal(W)
    requires knownPF(V) andBool knownPF(W) [simplification]

  // true division mirrors the shared applyBin("/",I1,I2)=>divII form
  syntax Bool ::= knownMul(Val) [function, total, no-evaluators]
  rule knownMul(A:Int *Int B:Int) => true  [simplification]
  rule knownMul(str(_:IntSeq))    => false [simplification]
  rule applyBin("/", V:Val, W:Val) => divII(projectIntTotal(V), projectIntTotal(W))
    requires knownMul(V) andBool knownMul(W) [simplification]
  rule projectIntTotal(A:Int *Int B:Int) => A *Int B [simplification]

  // int(float) mirrors the shared truncF rule
  syntax Bool ::= knownDiv(Val) [function, total, no-evaluators]
  rule knownDiv(divII(_:Int, _:Int)) => true  [simplification]
  rule knownDiv(str(_:IntSeq))       => false [simplification]
  rule applyBuiltin("int", V:Val, .Vals) => truncF(projectFloatTotal(V))
    requires knownDiv(V) [simplification]
  rule projectFloatTotal(divII(A:Int, B:Int)) => divII(A, B) [simplification]

  // the wholeness == mirrors the shared mixed Float==Int rule (eqF class)
  syntax Bool ::= knownTr(Val) [function, total, no-evaluators]
  rule knownTr(truncF(_:Float)) => true [simplification]
  rule applyCmp("==", V:Val, W:Val)
    => eqF(projectFloatTotal(V), intToF(projectIntTotal(W)))
    requires knownDiv(V) andBool knownTr(W) [simplification]
  rule projectIntTotal(truncF(F:Float)) => truncF(F) [simplification]

  // ---- the result model ------------------------------------------------------
  syntax Val ::= simpRes(IntSeq, IntSeq) [function, total]
  syntax Int ::= sNum(IntSeq, IntSeq) [function, total]
  rule sNum(XCS:IntSeq, NCS:IntSeq)
    => intDigAcc(fieldSeqC(0, XCS, 47), 0) *Int intDigAcc(fieldSeqC(0, NCS, 47), 0)
  syntax Int ::= sDen(IntSeq, IntSeq) [function, total]
  rule sDen(XCS:IntSeq, NCS:IntSeq)
    => intDigAcc(fieldSeqC(1, XCS, 47), 0) *Int intDigAcc(fieldSeqC(1, NCS, 47), 0)
  syntax Bool ::= simpAtom(IntSeq, IntSeq) [function, total]
  rule simpAtom(XCS:IntSeq, NCS:IntSeq)
    => eqF(divII(sNum(XCS, NCS), sDen(XCS, NCS)),
           intToF(truncF(divII(sNum(XCS, NCS), sDen(XCS, NCS)))))
  rule simpRes(XCS:IntSeq, NCS:IntSeq) => true
    requires simpAtom(XCS, NCS) [simplification]
  rule simpRes(XCS:IntSeq, NCS:IntSeq) => false
    requires notBool simpAtom(XCS, NCS) [simplification]
endmodule
