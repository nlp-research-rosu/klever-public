requires "verification.k"

module ANY-INT-SPEC-INDIVIDUAL
  imports ANY-INT-VERIFICATION

  claim [int-first]:
        <k> RunAnyInt(intVal(X), intVal(Y), intVal(Z))
             => boolVal(true) </k>
        <env> .Map </env>
    requires X +Int Y ==Int Z

  claim [int-second]:
        <k> RunAnyInt(intVal(X), intVal(Y), intVal(Z))
             => boolVal(true) </k>
        <env> .Map </env>
    requires notBool (X +Int Y ==Int Z)
     andBool X +Int Z ==Int Y

  claim [int-third]:
        <k> RunAnyInt(intVal(X), intVal(Y), intVal(Z))
             => boolVal(true) </k>
        <env> .Map </env>
    requires notBool (X +Int Y ==Int Z)
     andBool notBool (X +Int Z ==Int Y)
     andBool Y +Int Z ==Int X

  claim [int-none]:
        <k> RunAnyInt(intVal(X), intVal(Y), intVal(Z))
             => boolVal(false) </k>
        <env> .Map </env>
    requires notBool (X +Int Y ==Int Z)
     andBool notBool (X +Int Z ==Int Y)
     andBool notBool (Y +Int Z ==Int X)

  claim [nonint-first]:
        <k> RunAnyInt(_N:NonIntVal, _Y:Val, _Z:Val)
             => boolVal(false) </k>
        <env> .Map </env>

  claim [nonint-second]:
        <k> RunAnyInt(_X:IntVal, _N:NonIntVal, _Z:Val)
             => boolVal(false) </k>
        <env> .Map </env>

  claim [nonint-third]:
        <k> RunAnyInt(_X:IntVal, _Y:IntVal, _N:NonIntVal)
             => boolVal(false) </k>
        <env> .Map </env>
endmodule
