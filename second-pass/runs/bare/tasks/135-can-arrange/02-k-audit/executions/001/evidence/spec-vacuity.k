requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation: the real result is shifted by +1.  The empty-array
  // witness satisfies the precondition, returns -1, and this postcondition
  // incorrectly requires 0.
  claim [false-off-by-one]:
    <k> invoke("can_arrange", arrayVal(A, O, N)) ~> K
      => value(intVal(answer(A, O, N) +Int 1)) ~> K </k>
    <env> ENV </env>
    <defs> "can_arrange" |-> canArrangeFunction </defs>
    <stack> FRAMES </stack>
    requires O >=Int 0
     andBool N >=Int 0
     andBool O +Int N <=Int arrSize(A)

endmodule
