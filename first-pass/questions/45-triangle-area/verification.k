// verification.k — triangle_area on the UNIFIED semantics (src/). First FLOAT problem on unified.
// Straight-line, no loop: the body `a * h / 2.0` builds intFloatDiv(a*h, 2.0) — the Python true
// division of the Int `a*h` by the float literal 2.0. Floats are TRUSTED opaque primitives for
// kprove (mpy-float.k: intFloatDiv is [no-evaluators], stays symbolic; the [concrete] rule
// evaluates it for krun), so the result is verified STRUCTURALLY. See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module TRIANGLE-AREA-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  // proof-only: let a Val sit in expression position (so symbolic Ints are Call args).
  syntax Expr ::= Val

  // result of `a * h / 2.0`: the exact opaque term the program builds.
  syntax Val ::= triangleRes(Int, Int) [function]
  rule triangleRes(A:Int, H:Int) => intFloatDiv(A *Int H, 2.0) [simplification]
endmodule
