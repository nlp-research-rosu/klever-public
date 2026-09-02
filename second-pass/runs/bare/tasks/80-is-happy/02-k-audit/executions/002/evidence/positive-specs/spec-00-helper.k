requires "verification.k"

module AUDIT-SPEC-00-HELPER
  imports VERIFICATION

  claim <k> #call(#solution, "check_happy_triples", pyStr(S))
          => pyBool(#allTriples(S))
        </k>
endmodule
