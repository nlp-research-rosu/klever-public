requires "candidate/reference-semantics/semantics.k"

module DIGITS-VERIFICATION-BASE
  imports MPY

  syntax Int ::= oddDigitProduct(Int, Int) [function, total]
               | oddDigitStep(Bool, Int, Int, Int) [function, total]

  rule oddDigitProduct(0, A:Int) => A

  rule oddDigitProduct(N:Int, A:Int)
    => oddDigitStep(
         pyMod(N, 2) ==Int 1,
         (N -Int pyMod(N, 10)) /Int 10,
         pyMod(N, 10),
         A)
    requires N >Int 0

  rule oddDigitStep(B:Bool, Q:Int, _:Int, A:Int)
    => oddDigitProduct(Q, A)
    requires notBool B

  rule oddDigitStep(B:Bool, Q:Int, D:Int, 0)
    => oddDigitProduct(Q, D)
    requires B

  rule oddDigitStep(B:Bool, Q:Int, D:Int, A:Int)
    => oddDigitProduct(Q, A *Int D)
    requires B andBool A =/=Int 0
endmodule
