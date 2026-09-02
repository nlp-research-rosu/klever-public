requires "body-mutated-verification.k"

module BODY-MUTATED-SPEC
  imports BODY-MUTATED-VERIFICATION

  claim
    <k> invoke("can_arrange", arrayVal(A, O, N)) ~> K
      => value(intVal(answer(A, O, N))) ~> K </k>
    <env> ENV </env>
    <defs> "can_arrange" |-> mutatedCanArrangeFunction </defs>
    <stack> FRAMES </stack>
    requires O >=Int 0
     andBool N >=Int 0
     andBool O +Int N <=Int arrSize(A)

endmodule
