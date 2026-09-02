requires "verification.k"

module AUDIT-SPEC-02-EXAMPLE-A
  imports VERIFICATION

  claim <k> #call(#solution, "is_happy", pyStr(ch(97, eps)))
          => pyBool(false)
        </k>
endmodule
