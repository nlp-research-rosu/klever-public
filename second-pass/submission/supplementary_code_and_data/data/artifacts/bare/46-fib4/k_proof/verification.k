module VERIFICATION
  imports INT

  // Mathematical result of rolling the window from loop index I through N.
  // This is separate from the Python AST semantics: it is the functional
  // specification used by the loop invariant.
  syntax Int ::= "advanceTo" "(" Int "," Int "," Int "," Int "," Int "," Int ")"
                 [function, total]
  rule advanceTo(_A, _B, _C, D, I, N) => D
    requires I >Int N
  rule advanceTo(A, B, C, D, I, N)
    => advanceTo(B, C, D, A +Int B +Int C +Int D, I +Int 1, N)
    requires I <=Int N

  // The HumanEval recurrence, expressed by the rolling mathematical model.
  // Index 4 is the first update from the base window at indices 0..3.
  syntax Int ::= "fib4Spec" "(" Int ")" [function, total]
  rule fib4Spec(0) => 0
  rule fib4Spec(1) => 0
  rule fib4Spec(2) => 2
  rule fib4Spec(3) => 0
  rule fib4Spec(N) => advanceTo(0, 0, 2, 0, 4, N)
    requires N >=Int 4
endmodule
