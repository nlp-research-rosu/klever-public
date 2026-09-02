requires "verification.k"

module AUDIT-SPEC-7
  imports ANY-INT-VERIFICATION

  claim <k> RunAnyInt(_X:IntVal, _Y:IntVal, _N:NonIntVal)
             => boolVal(false) </k>
        <env> .Map </env>
endmodule
