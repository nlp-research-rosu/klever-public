requires "verification.k"

module AUDIT-SPEC-5
  imports ANY-INT-VERIFICATION

  claim <k> RunAnyInt(_N:NonIntVal, _Y:Val, _Z:Val)
             => boolVal(false) </k>
        <env> .Map </env>
endmodule
