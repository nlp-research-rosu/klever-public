requires "verification.k"

module AUDIT-SPEC-03-EXAMPLE-AA
  imports VERIFICATION

  claim <k> #call(#solution, "is_happy", pyStr(ch(97, ch(97, eps))))
          => pyBool(false)
        </k>
endmodule
