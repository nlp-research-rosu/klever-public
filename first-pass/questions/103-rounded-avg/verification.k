// verification.k — rounded_avg on the UNIFIED semantics, TRAP-FREE (P103).
// solution.py is canonical verbatim: the real summation loop and
// bin(round(summation/(m-n+1))). The float atoms (divII/roundF) stay opaque
// per the float rung; trusted non-negativity properties let bin's domain
// guard discharge; binCodes stays opaque on the symbolic atom.

requires "../../reference/src/lemmas.k"

module ROUNDED-AVG-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // range-sum fold
  syntax Int ::= sumRange(Int, Int) [function, total]
  rule sumRange(I:Int, HI:Int) => 0 requires I >=Int HI [simplification]
  rule sumRange(I:Int, HI:Int) => I +Int sumRange(I +Int 1, HI)
    requires I <Int HI [simplification]
  // trusted non-negativity of the opaque float route (float-rung policy):
  // a round of a non-negative division is a non-negative int; the sum-fold
  // shapes cover the once-unfolded PC normal form
  rule sumRange(I:Int, HI:Int) >=Int 0 => true
    requires I >=Int 0 [simplification]
  rule N:Int +Int sumRange(I:Int, HI:Int) >=Int 0 => true
    requires N >=Int 0 andBool I >=Int 0 [simplification]
  rule roundF(divII(A:Int, B:Int)) >=Int 0 => true
    requires A >=Int 0 andBool B >Int 0 [simplification]

  // the shared bin rule's guard (arg >= 0) is not Z3-decidable on the opaque
  // float route (the roundF atom abstracts whole); this echo of the shared
  // rule keys on the structural roundF(divII(..)) head, and its guard
  // discharges through the trusted lemmas above
  rule applyBuiltin("bin", roundF(divII(S:Int, B:Int)), .Vals)
    => str(iCons(48, iCons(98, binCodes(roundF(divII(S, B))))))
    requires S >=Int 0 andBool B >Int 0
    [simplification]

  // the whole result
  syntax Val ::= raRes(Int, Int) [function]
  rule raRes(N:Int, M:Int) => -1 requires M <Int N [simplification]
  rule raRes(N:Int, M:Int)
    => str(iCons(48, iCons(98, binCodes(roundF(divII(sumRange(N, M +Int 1), (M -Int N) +Int 1))))))
    requires M >=Int N [simplification]
endmodule
