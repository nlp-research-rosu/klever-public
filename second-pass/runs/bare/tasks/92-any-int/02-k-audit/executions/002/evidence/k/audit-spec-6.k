requires "verification.k"

module AUDIT-SPEC-6
  imports ANY-INT-VERIFICATION

  claim <k> RunAnyInt(_X:IntVal, _N:NonIntVal, _Z:Val)
             => boolVal(false) </k>
        <env> .Map </env>
endmodule
