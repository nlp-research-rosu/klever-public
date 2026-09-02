requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX
  imports INT-SYNTAX

  syntax Int ::= lpfFrom(Int, Int) [function]
endmodule

module VERIFICATION
  imports MPY
  imports VERIFICATION-SYNTAX

  rule lpfFrom(N:Int, F:Int) => N
    requires F >=Int 2 andBool N <=Int F

  rule lpfFrom(N:Int, F:Int)
    => lpfFrom((N -Int pyMod(N, F)) /Int F, F)
    requires F >=Int 2 andBool N >Int F andBool pyMod(N, F) ==Int 0

  rule lpfFrom(N:Int, F:Int) => lpfFrom(N, F +Int 1)
    requires F >=Int 2 andBool N >Int F andBool pyMod(N, F) =/=Int 0
endmodule
