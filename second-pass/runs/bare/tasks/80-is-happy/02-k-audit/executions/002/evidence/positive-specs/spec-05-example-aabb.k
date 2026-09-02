requires "verification.k"

module AUDIT-SPEC-05-EXAMPLE-AABB
  imports VERIFICATION

  claim <k> #call(#solution, "is_happy",
                  pyStr(ch(97, ch(97, ch(98, ch(98, eps))))))
          => pyBool(false)
        </k>
endmodule
