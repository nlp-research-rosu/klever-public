requires "verification.k"

module AUDIT-VALUE-EVEN
  imports TRI-VERIFICATION
  claim [value-even]:
    <k> triValue(N) => 1 +Int (N /Int 2) ... </k>
    requires N >=Int 2 andBool N %Int 2 ==Int 0
endmodule
