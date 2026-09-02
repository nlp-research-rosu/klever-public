requires "/tmp/audit-work/142-sum-squares-audit/verification.k"

module SUM-SQUARES-VERIFICATION-BRIDGE-MUTANT
  imports SUM-SQUARES-VERIFICATION

  // Operational-sensitivity mutation.  Priority 30 preempts the candidate's
  // priority-40 nonempty Ints bridge and binds each loop element to X + 1.
  rule <k> #iterNext(list(intVals(intCons(X:Int, XS:Ints))))
        => #iterYield(X +Int 1, list(intVals(XS))) ... </k>
    [priority(30)]
endmodule
