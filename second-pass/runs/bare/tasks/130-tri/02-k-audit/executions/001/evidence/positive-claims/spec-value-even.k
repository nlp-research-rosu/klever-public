requires "/tmp/audit-work/130-tri/candidate/verification.k"

module AUDIT-SPEC-VALUE-EVEN
  imports TRI-VERIFICATION
  claim <k> triValue(N) => 1 +Int (N /Int 2) ... </k>
    requires N >=Int 2 andBool N %Int 2 ==Int 0
endmodule
