requires "verification.k"

module ANY-INT-SPEC-VACUITY-AUDIT
  imports ANY-INT-VERIFICATION

  // Deliberately false: (1,2,3) satisfies the precondition, but the submitted
  // program and the semantics both return boolVal(true).
  claim [false-first-sum]:
        <k> RunAnyInt(intVal(X), intVal(Y), intVal(Z))
             => boolVal(false) </k>
        <env> .Map </env>
    requires X +Int Y ==Int Z
endmodule
