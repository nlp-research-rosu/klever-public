requires "verification.k"

module AUDIT-SPEC-1
  imports ANY-INT-VERIFICATION

  claim <k> RunAnyInt(intVal(X), intVal(Y), intVal(Z))
             => boolVal(true) </k>
        <env> .Map </env>
    requires X +Int Y ==Int Z
endmodule
