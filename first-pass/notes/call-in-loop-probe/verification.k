// verification.k — Probe A: call-in-loop (de-escape rework Task 3). digsum (its own while-loop)
// called from total_digsum's range-loop, proven with NO interceptions: the real Call executes
// every iteration; frame deallocation (scopeLoc wind-back) keeps the outer invariant's
// configuration shape fixed across calls.

requires "../../src/lemmas.k"

module CALL-IN-LOOP-PROBE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // digit-sum summary (numeric-while rung; the reference's pyMod-based // and %). [total]:
  // lands in the scope map during the fold.
  syntax Int ::= digAcc(Int, Int) [function, total]
  rule digAcc(K:Int, S:Int) => S
    requires K <=Int 0
    [simplification]
  rule digAcc(K:Int, S:Int) => digAcc((K -Int pyMod(K, 10)) /Int 10, S +Int pyMod(K, 10))
    requires K >Int 0
    [simplification]

  // outer fold: t += digsum(i) for i in [I, N); the step adds digAcc(I, 0).
  syntax Int ::= tdFold(Int, Int, Int) [function, total]
  rule tdFold(I:Int, N:Int, T:Int) => T
    requires I >=Int N
    [simplification]
  rule tdFold(I:Int, N:Int, T:Int) => tdFold(I +Int 1, N, T +Int digAcc(I, 0))
    requires I <Int N
    [simplification]
endmodule
