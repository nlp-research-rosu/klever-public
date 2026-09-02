requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Mathematical tail-recursive summary of the loop's result sequence.
  // It does not rewrite or replace any program computation.
  syntax ValSeq ::= factorAcc(ValSeq, Int, Int) [function]

  rule factorAcc(A:ValSeq, N:Int, D:Int) => A
    requires N <Int D

  rule factorAcc(A:ValSeq, N:Int, D:Int)
    => factorAcc(
         valSeqConcat(A, vCons(D, .ValSeq)),
         (N -Int pyMod(N, D)) /Int D,
         D)
    requires D <=Int N andBool pyMod(N, D) ==Int 0

  rule factorAcc(A:ValSeq, N:Int, D:Int)
    => factorAcc(A, N, D +Int 1)
    requires D <=Int N andBool pyMod(N, D) =/=Int 0
endmodule
