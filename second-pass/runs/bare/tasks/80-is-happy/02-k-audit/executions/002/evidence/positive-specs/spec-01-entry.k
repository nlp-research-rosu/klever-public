requires "verification.k"

module AUDIT-SPEC-01-ENTRY
  imports VERIFICATION

  claim <k> #call(#solution, "check_happy_triples", pyStr(S))
          => pyBool(#allTriples(S))
        </k>

  claim <k> #call(#solution, "is_happy", pyStr(S))
          => pyBool(#happy(S))
        </k>
endmodule
