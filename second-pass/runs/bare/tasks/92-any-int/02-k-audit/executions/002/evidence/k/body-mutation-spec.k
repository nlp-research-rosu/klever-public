requires "verification-body-mutated.k"

module BODY-MUTATION-SPEC
  imports ANY-INT-VERIFICATION-BODY-MUTATED

  // False for the mutated body: (5,2,7) now returns False.
  claim <k> RunAnyIntBodyMutated(intVal(5), intVal(2), intVal(7))
             => boolVal(true) </k>
        <env> .Map </env>
endmodule
