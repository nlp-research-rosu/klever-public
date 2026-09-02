// verification.k — truncate_number on the UNIFIED semantics. The fractional part `number % 1.0`
// is a float remainder — a TRUSTED opaque primitive for kprove (mpy-float.k: floatMod is
// [no-evaluators], stays symbolic; [concrete] for krun). Result verified STRUCTURALLY. See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module TRUNCATE-NUMBER-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  // proof-only: let a Val (symbolic Float) sit in expression position (Call arg).
  syntax Expr ::= Val

  // result of `number % 1.0`: the exact opaque term the program builds.
  syntax Val ::= truncRes(Float) [function]
  rule truncRes(F:Float) => floatMod(F, 1.0) [simplification]
endmodule
