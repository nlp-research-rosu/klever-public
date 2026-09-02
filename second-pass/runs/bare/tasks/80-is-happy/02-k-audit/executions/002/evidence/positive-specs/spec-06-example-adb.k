requires "verification.k"

module AUDIT-SPEC-06-EXAMPLE-ADB
  imports VERIFICATION

  claim <k> #call(#solution, "is_happy",
                  pyStr(ch(97, ch(100, ch(98, eps)))))
          => pyBool(true)
        </k>
endmodule
