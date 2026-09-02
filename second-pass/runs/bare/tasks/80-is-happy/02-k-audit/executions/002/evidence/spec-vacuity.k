requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports VERIFICATION

  // "abc" satisfies the original claim and returns true; false is deliberate.
  claim <k> #call(#solution, "is_happy",
                  pyStr(ch(97, ch(98, ch(99, eps)))))
          => pyBool(false)
        </k>
endmodule
