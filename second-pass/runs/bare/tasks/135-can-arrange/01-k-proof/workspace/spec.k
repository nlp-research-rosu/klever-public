requires "verification.k"

module SPEC
  imports VERIFICATION

  // Inductive, all-length correctness claim. K is universally quantified,
  // so the theorem applies to calls in every expression continuation. ENV
  // and FRAMES are restored exactly across the call. The definition cell
  // fixes the interpreted function to the generated solution constructor.
  claim
    <k> invoke("can_arrange", arrayVal(A, O, N)) ~> K
      => value(intVal(answer(A, O, N))) ~> K </k>
    <env> ENV </env>
    <defs> "can_arrange" |-> canArrangeFunction </defs>
    <stack> FRAMES </stack>
    requires O >=Int 0
     andBool N >=Int 0
     andBool O +Int N <=Int arrSize(A)

endmodule
