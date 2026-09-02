requires "verification.k"

module AUDIT-VALUE-ODD-RECURRENCE
  imports TRI-VERIFICATION
  claim [value-odd-recurrence]:
    <k> triValue(N)
        => triValue(N -Int 1) +Int triValue(N -Int 2)
           +Int triValue(N +Int 1)
        ... </k>
    requires N >=Int 3 andBool N %Int 2 =/=Int 0
endmodule
