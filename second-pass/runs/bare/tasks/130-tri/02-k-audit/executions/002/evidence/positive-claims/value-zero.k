requires "verification.k"

module AUDIT-VALUE-ZERO
  imports TRI-VERIFICATION
  claim [value-zero]: <k> triValue(0) => 1 ... </k>
endmodule
