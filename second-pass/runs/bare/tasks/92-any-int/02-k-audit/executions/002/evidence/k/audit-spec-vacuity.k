requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports ANY-INT-VERIFICATION

  // Reviewer mutation of claim 1's result. This is false for X=5,Y=2,Z=7.
  claim <k> RunAnyInt(intVal(X), intVal(Y), intVal(Z))
             => boolVal(false) </k>
        <env> .Map </env>
    requires X +Int Y ==Int Z
endmodule
