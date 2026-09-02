requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX
  imports INT

  syntax Int ::= digitResult(Int, Int) [function]
               | fizzResult(Int, Int) [function]
endmodule

module VERIFICATION
  imports MPY
  imports VERIFICATION-SYNTAX
  imports INT
  imports BOOL

  // Tail-recursive mathematical result of the inner loop.
  rule digitResult(C, N) => C
    requires N <=Int 0
    [simplification]
  rule digitResult(C, N) =>
      C +Int (#if pyMod(N, 10) ==Int 7 #then 1 #else 0 #fi)
    requires N >Int 0
     andBool (N -Int pyMod(N, 10)) /Int 10 <=Int 0
    [simplification]
  rule digitResult(
         C +Int
           (#if ((N %Int 10) +Int 10) %Int 10 ==Int 7
            #then 1 #else 0 #fi),
         (N -Int (((N %Int 10) +Int 10) %Int 10)) /Int 10)
       => digitResult(C, N)
    requires N >Int 0
    [simplification]

  // Tail-recursive mathematical result of the outer loop.
  rule fizzResult(C, N) => C
    requires N <=Int 0
    [simplification]
  rule fizzResult(digitResult(C, N +Int -1), N +Int -1)
       => fizzResult(C, N)
    requires N >Int 0
     andBool (
       ((((N +Int -1) %Int 11) +Int 11) %Int 11 ==Int 0)
       orBool
       ((((N +Int -1) %Int 13) +Int 13) %Int 13 ==Int 0))
    [simplification]
  rule fizzResult(C, N +Int -1)
       => fizzResult(C, N)
    requires N >Int 0
     andBool notBool (
       ((((N +Int -1) %Int 11) +Int 11) %Int 11 ==Int 0)
       orBool
       ((((N +Int -1) %Int 13) +Int 13) %Int 13 ==Int 0))
    [simplification]
endmodule
