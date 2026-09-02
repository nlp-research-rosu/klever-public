requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX
  imports MPY-CORE

  // The result of testing every candidate divisor I, I + 1, ..., N - 1.
  // The function is used only with I >= 2.
  syntax Val ::= trialChoice(Int, Int, Val, Val) [function]
               | xOrYSpec(Int, Val, Val)         [function, total]
endmodule

module VERIFICATION
  imports VERIFICATION-SYNTAX
  imports MPY

  rule trialChoice(N, I, R, _Y) => R
    requires I >=Int N andBool I >=Int 2

  rule trialChoice(N, I, _R, Y) => trialChoice(N, I +Int 1, Y, Y)
    requires I >=Int 2 andBool I <Int N
      andBool pyMod(N, I) ==Int 0

  rule trialChoice(N, I, R, Y) => trialChoice(N, I +Int 1, R, Y)
    requires I >=Int 2 andBool I <Int N
      andBool pyMod(N, I) =/=Int 0

  rule xOrYSpec(N, _X, Y) => Y
    requires N <Int 2

  rule xOrYSpec(N, X, Y) => trialChoice(N, 2, X, Y)
    requires N >=Int 2
endmodule
