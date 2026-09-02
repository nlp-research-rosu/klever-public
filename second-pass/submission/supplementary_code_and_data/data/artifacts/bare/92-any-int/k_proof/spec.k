requires "verification.k"

module ANY-INT-SPEC
  imports ANY-INT-VERIFICATION

  // Together these four claims partition all integer triples according to
  // the first true sum equality.  Thus they prove the complete positive and
  // negative behavior on Python integers, not just concrete examples.
  claim <k> RunAnyInt(intVal(X), intVal(Y), intVal(Z))
             => boolVal(true) </k>
        <env> .Map </env>
    requires X +Int Y ==Int Z

  claim <k> RunAnyInt(intVal(X), intVal(Y), intVal(Z))
             => boolVal(true) </k>
        <env> .Map </env>
    requires notBool (X +Int Y ==Int Z)
     andBool X +Int Z ==Int Y

  claim <k> RunAnyInt(intVal(X), intVal(Y), intVal(Z))
             => boolVal(true) </k>
        <env> .Map </env>
    requires notBool (X +Int Y ==Int Z)
     andBool notBool (X +Int Z ==Int Y)
     andBool Y +Int Z ==Int X

  claim <k> RunAnyInt(intVal(X), intVal(Y), intVal(Z))
             => boolVal(false) </k>
        <env> .Map </env>
    requires notBool (X +Int Y ==Int Z)
     andBool notBool (X +Int Z ==Int Y)
     andBool notBool (Y +Int Z ==Int X)

  // These claims partition every call containing a non-integer according to
  // the position of its first non-integer argument.  Later arguments remain
  // fully symbolic because short-circuiting prevents their arithmetic use.
  claim <k> RunAnyInt(_N:NonIntVal, _Y:Val, _Z:Val)
             => boolVal(false) </k>
        <env> .Map </env>

  claim <k> RunAnyInt(_X:IntVal, _N:NonIntVal, _Z:Val)
             => boolVal(false) </k>
        <env> .Map </env>

  claim <k> RunAnyInt(_X:IntVal, _Y:IntVal, _N:NonIntVal)
             => boolVal(false) </k>
        <env> .Map </env>
endmodule
