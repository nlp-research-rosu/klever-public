requires "verification.k"

module AUDIT-VALUE-ONE
  imports TRI-VERIFICATION
  claim [value-one]: <k> triValue(1) => 3 ... </k>
endmodule
