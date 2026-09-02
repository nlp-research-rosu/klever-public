requires "semantic.k"
requires "solution-program.k"

module VERIFICATION
  imports MPY
  imports SOLUTION-PROGRAM

  syntax KItem ::= "verifyBF" "(" String "," String ")"

  rule <k> verifyBF(P1, P2)
          => solutionProgram ~> invokeBF(P1, P2)
       ... </k>
endmodule
