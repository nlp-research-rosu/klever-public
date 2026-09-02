requires "spec.k"

module PIN-SPEC
  imports SPEC

  // Reviewer-authored bridge from the full submitted program term (represented
  // by the candidate's macro) through module loading to the independently
  // reconstructed and already-proved invocation claim.
  claim [full-program-pin]:
    <k> solutionProgram ~> invokeEntry(arrayVal(A, O, N))
      => value(intVal(answer(A, O, N))) </k>
    <env> .Map </env>
    <defs> .Map => "can_arrange" |-> canArrangeFunction </defs>
    <stack> .List </stack>
    requires O >=Int 0
     andBool N >=Int 0
     andBool O +Int N <=Int arrSize(A)

endmodule
