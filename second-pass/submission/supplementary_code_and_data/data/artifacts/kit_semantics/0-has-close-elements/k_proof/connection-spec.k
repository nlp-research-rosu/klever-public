requires "connection-verification.k"

module CONNECTION-SPEC
  imports CONNECTION-VERIFICATION

  // Bridge-free universal connection for the fixed Float subtraction rule.
  claim [float-subtraction]:
    <k> applyBin("-", A:Float, B:Float) => subF(A, B) ... </k>
endmodule
