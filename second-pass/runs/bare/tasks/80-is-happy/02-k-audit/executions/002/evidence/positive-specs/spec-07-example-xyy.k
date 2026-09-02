requires "verification.k"

module AUDIT-SPEC-07-EXAMPLE-XYY
  imports VERIFICATION

  claim <k> #call(#solution, "is_happy",
                  pyStr(ch(120, ch(121, ch(121, eps)))))
          => pyBool(false)
        </k>
endmodule
