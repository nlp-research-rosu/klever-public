// verification.k — find_zero on the UNIFIED semantics (reference/src/).  PARTIAL-correctness summary.
//
// Two loops thread (begin, end): `bracket` doubles until poly(begin)*poly(end) <= 0; `bisect` halves,
// keeping the sign-changing half, and returns the final begin.  poly / the float ops / the guard gtF
// are TRUSTED opaque primitives (kprove has no float theory — float-proving-limitation), so the
// summaries are opaque on symbolic input and reduce in LOCKSTEP with the loop under the guard
// case-splits.  The theorem is PARTIAL (co-inductive): IF the loops halt, result = findZeroRes(xs).
// The loop-threading STRUCTURE is verified; the float math + root property are trusted (real in krun).
// Problem-local; no shared change (adds the additive Float cases applyBin("*")/applyCmp(">") the
// reference lacks).

requires "../../reference/src/lemmas.k"

module FINDZERO-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports FLOAT

  syntax Expr ::= Val

  // The program forms the literal -1.0 (begin's initial value); the missing
  // -Float hook is worked around by the SHARED literal rule (lemmas/float.k),
  // so the initial begin stays opaque-free while everything downstream (poly
  // on symbolic XS) stays opaque.

  // ---- trusted float ops the reference lacks (additive: it has -, +, / on Float, not * or >) --------
  // mulF / gtF are the SHARED float ops (semantics/float.k) since stage 3

  // ---- polynomial eval poly(xs, x): DEFINED symbolic twin below; concrete power-threading scan for krun --
  syntax KItem ::= #polyK1(Expr) | #polyK2(Val)
  rule <k> Call(Name("poly"), (A:Expr, B:Expr, .Exprs)) => A ~> #polyK1(B) ... </k>
  rule <k> AV:Val ~> #polyK1(B:Expr) => B ~> #polyK2(AV) ... </k>
  rule <k> XV:Float ~> #polyK2(list(XS:ValSeq)) => polyF(XS, XV) ... </k>
  // DE-ESCAPED: polyF keeps its [concrete] krun fold and gains a SYMBOLIC defining twin — the
  // same power-threading Horner scan over shared addF/mulF/projectFloatTotal (the #4 pattern).
  // Residue = the shared float leaves (+ the trivial -1.0 constant fold above, a missing-hook
  // workaround).
  syntax Float ::= polyF(ValSeq, Float) [function, total, symbol(polyF)]
  rule polyF(XS:ValSeq, X:Float) => pEval(XS, X, 1.0, 0.0) [concrete]
  rule polyF(XS:ValSeq, X:Float) => pEvalD(XS, X, 1.0, 0.0) [simplification]
  syntax Float ::= pEvalD(ValSeq, Float, Float, Float) [function, total]
  rule pEvalD(.ValSeq, _X:Float, _XP:Float, ACC:Float) => ACC [simplification]
  rule pEvalD(vCons(V:Val, R:ValSeq), X:Float, XP:Float, ACC:Float)
    => pEvalD(R, X, mulF(XP, X), addF(ACC, mulF(projectFloatTotal(V), XP))) [simplification]
  syntax Float ::= pEval(ValSeq, Float, Float, Float) [function]
  rule pEval(.ValSeq, _X:Float, _XP:Float, ACC:Float) => ACC [concrete]
  rule pEval(vCons(V:Val, R:ValSeq), X:Float, XP:Float, ACC:Float)
    => pEval(R, X, mulF(XP, X), addF(ACC, mulF(projF(V), XP))) [concrete]
  syntax Float ::= projF(Val) [function]
  rule projF(F:Float) => F [concrete]

  // ---- pair projections ---------------------------------------------------------------------------
  syntax Pair ::= pr(Float, Float)
  syntax Float ::= brB(Pair) [function, total]
  syntax Float ::= brE(Pair) [function, total]
  rule brB(pr(B:Float, _E:Float)) => B [simplification]
  rule brE(pr(_B:Float, E:Float)) => E [simplification]

  // ---- bracket-expansion loop: double (begin,end) while poly(begin)*poly(end) > 0 ------------------
  syntax Pair ::= bracket(ValSeq, Float, Float) [function]
  rule bracket(XS:ValSeq, B:Float, E:Float) => pr(B, E)
    requires notBool gtF(mulF(polyF(XS, B), polyF(XS, E)), 0.0) [simplification]
  rule bracket(XS:ValSeq, B:Float, E:Float) => bracket(XS, mulF(B, 2.0), mulF(E, 2.0))
    requires gtF(mulF(polyF(XS, B), polyF(XS, E)), 0.0) [simplification]

  // ---- bisection loop: halve, keep the sign-changing half; return final begin ---------------------
  syntax Float ::= bisect(ValSeq, Float, Float) [function]
  rule bisect(_XS:ValSeq, B:Float, E:Float) => B
    requires notBool gtF(subF(E, B), 1e-10) [simplification]
  rule bisect(XS:ValSeq, B:Float, E:Float) => bisect(XS, divF(addF(B, E), 2.0), E)
    requires gtF(subF(E, B), 1e-10)
     andBool gtF(mulF(polyF(XS, divF(addF(B, E), 2.0)), polyF(XS, B)), 0.0) [simplification]
  rule bisect(XS:ValSeq, B:Float, E:Float) => bisect(XS, B, divF(addF(B, E), 2.0))
    requires gtF(subF(E, B), 1e-10)
     andBool notBool gtF(mulF(polyF(XS, divF(addF(B, E), 2.0)), polyF(XS, B)), 0.0) [simplification]

  syntax Val ::= findZeroRes(ValSeq) [function]
  rule findZeroRes(XS:ValSeq)
    => bisect(XS, brB(bracket(XS, -1.0, 1.0)), brE(bracket(XS, -1.0, 1.0))) [simplification]
endmodule
