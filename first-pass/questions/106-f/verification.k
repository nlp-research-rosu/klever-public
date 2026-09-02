// verification.k — f on the UNIFIED semantics (src/). First NESTED-loop proof on unified.
// The outer loop builds ret[i] = i! (i even) or 1+2+...+i (i odd); each element is computed
// by an INNER range loop. Everything is INDEX-based (factorial/triangular of the loop index),
// so there is no symbolic-element arithmetic. See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module F-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  // proof-only: let a Val sit in expression position (so a symbolic Int can be a Call arg).
  syntax Expr ::= Val

  // ---- summary functions = the spec (differential-tested vs CPython: 0 mismatches) -------
  //
  // INNER factorial fold (body `x *= j` over range(J, HI)):
  //   factFold(J, HI, X) = X * J * (J+1) * ... * (HI-1)  (the running product).
  // For range(1, i+1) from x=1 this is factFold(1, i+1, 1) = i!.  Python `*` is exact => *Int.
  syntax Int ::= factFold(Int, Int, Int) [function, total]
  rule factFold(J:Int, HI:Int, X:Int) => X                                requires J >=Int HI [simplification]
  rule factFold(J:Int, HI:Int, X:Int) => factFold(J +Int 1, HI, X *Int J) requires J  <Int HI [simplification]

  // INNER triangular-sum fold (body `x += j` over range(J, HI)):
  //   sumFold(J, HI, X) = X + J + (J+1) + ... + (HI-1).
  // For range(1, i+1) from x=0 this is sumFold(1, i+1, 0) = 1+2+...+i.
  syntax Int ::= sumFold(Int, Int, Int) [function, total]
  rule sumFold(J:Int, HI:Int, X:Int) => X                                requires J >=Int HI [simplification]
  rule sumFold(J:Int, HI:Int, X:Int) => sumFold(J +Int 1, HI, X +Int J)   requires J  <Int HI [simplification]

  // The element of `ret` produced at outer index I:  i! if i even else 1+2+...+i.
  // Branch on I % 2 (Python floored modInt) — the program's `if i % 2 == 0`.  Exhaustive
  // (modInt 2 is 0 or 1 for i >= 1), so [total].
  syntax Int ::= elemAt(Int) [function, total]
  rule elemAt(I:Int) => factFold(1, I +Int 1, 1) requires I modInt 2 ==Int 0  [simplification]
  rule elemAt(I:Int) => sumFold(1, I +Int 1, 0)  requires I modInt 2 =/=Int 0 [simplification]

  // OUTER list-build fold: the list emitted by the outer loop over [I, HI):
  //   [elemAt(I), elemAt(I+1), ..., elemAt(HI-1)].  elemAt(I):Int rides in a ValSeq (Int < Val).
  syntax ValSeq ::= retFrom(Int, Int) [function, total]
  rule retFrom(I:Int, HI:Int) => .ValSeq                                  requires I >=Int HI [simplification]
  rule retFrom(I:Int, HI:Int) => vCons(elemAt(I), retFrom(I +Int 1, HI))  requires I  <Int HI [simplification]

  // ---- left-append concat lemmas (from 30-get-positive) -------------------------------

  // whole-list result: ret starts [], so f(N) = valSeqConcat(.ValSeq, retFrom(1,N+1)) = retFrom(1,N+1).
  syntax Val ::= fRes(Int) [function]
  rule fRes(N:Int) => list(retFrom(1, N +Int 1)) [simplification]
endmodule
