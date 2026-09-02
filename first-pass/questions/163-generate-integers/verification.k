// verification.k — summary for the generate_integers proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module GENERATE-INTEGERS-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // evensV(I, HI) = the even integers in [I, HI) (range(I, HI)) in ascending order — the
  // filtered comprehension [i for i in range(I,HI) if i%2==0]. Branch-split like the loop:
  // I>=HI empty; else keep I (even) or skip. `%` is the reference's floored pyMod. [total].
  syntax ValSeq ::= evensV(Int, Int) [function, total]
  rule evensV(I:Int, HI:Int) => .ValSeq                       requires I >=Int HI [simplification]
  rule evensV(I:Int, HI:Int) => vCons(I, evensV(I +Int 1, HI)) requires I <Int HI andBool pyMod(I, 2) ==Int 0  [simplification]
  rule evensV(I:Int, HI:Int) => evensV(I +Int 1, HI)          requires I <Int HI andBool pyMod(I, 2) =/=Int 0 [simplification]

  // Left-built accumulator echoes ($acc = $acc + [i]).
endmodule
