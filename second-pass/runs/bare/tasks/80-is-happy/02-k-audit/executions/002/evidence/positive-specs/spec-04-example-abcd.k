requires "verification.k"

module AUDIT-SPEC-04-EXAMPLE-ABCD
  imports VERIFICATION

  claim <k> #call(#solution, "is_happy",
                  pyStr(ch(97, ch(98, ch(99, ch(100, eps))))))
          => pyBool(true)
        </k>
endmodule
