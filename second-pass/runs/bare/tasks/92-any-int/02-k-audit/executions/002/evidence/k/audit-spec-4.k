requires "verification.k"

module AUDIT-SPEC-4
  imports ANY-INT-VERIFICATION

  claim <k> RunAnyInt(intVal(X), intVal(Y), intVal(Z))
             => boolVal(false) </k>
        <env> .Map </env>
    requires notBool (X +Int Y ==Int Z)
     andBool notBool (X +Int Z ==Int Y)
     andBool notBool (Y +Int Z ==Int X)
endmodule
