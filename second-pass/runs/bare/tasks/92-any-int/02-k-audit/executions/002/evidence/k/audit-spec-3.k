requires "verification.k"

module AUDIT-SPEC-3
  imports ANY-INT-VERIFICATION

  claim <k> RunAnyInt(intVal(X), intVal(Y), intVal(Z))
             => boolVal(true) </k>
        <env> .Map </env>
    requires notBool (X +Int Y ==Int Z)
     andBool notBool (X +Int Z ==Int Y)
     andBool Y +Int Z ==Int X
endmodule
