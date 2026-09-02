requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation: "abc" satisfies the unrestricted entry domain and
  // has one pairwise-distinct triple, so the real result is true, not false.
  claim <k> #call(#solution, "is_happy",
                  pyStr(ch(97, ch(98, ch(99, eps)))))
          => pyBool(false)
        </k>
endmodule
