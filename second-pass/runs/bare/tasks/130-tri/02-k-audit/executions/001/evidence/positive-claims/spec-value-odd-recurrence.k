requires "/tmp/audit-work/130-tri/candidate/verification.k"

module AUDIT-SPEC-VALUE-ODD-RECURRENCE
  imports TRI-VERIFICATION
  claim <k> triValue(N)
          => triValue(N -Int 1) +Int triValue(N -Int 2) +Int triValue(N +Int 1)
        ... </k>
    requires N >=Int 3 andBool N %Int 2 =/=Int 0
endmodule
