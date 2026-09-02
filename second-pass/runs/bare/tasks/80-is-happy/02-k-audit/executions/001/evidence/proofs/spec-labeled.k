requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [helper]:
    <k> #call(#solution, "check_happy_triples", pyStr(S))
        => pyBool(#allTriples(S))
    </k>

  claim [entry]:
    <k> #call(#solution, "is_happy", pyStr(S))
        => pyBool(#happy(S))
    </k>

  claim [example-a]:
    <k> #call(#solution, "is_happy", pyStr(ch(97, eps)))
        => pyBool(false)
    </k>

  claim [example-aa]:
    <k> #call(#solution, "is_happy", pyStr(ch(97, ch(97, eps))))
        => pyBool(false)
    </k>

  claim [example-abcd]:
    <k> #call(#solution, "is_happy",
              pyStr(ch(97, ch(98, ch(99, ch(100, eps))))))
        => pyBool(true)
    </k>

  claim [example-aabb]:
    <k> #call(#solution, "is_happy",
              pyStr(ch(97, ch(97, ch(98, ch(98, eps))))))
        => pyBool(false)
    </k>

  claim [example-adb]:
    <k> #call(#solution, "is_happy",
              pyStr(ch(97, ch(100, ch(98, eps)))))
        => pyBool(true)
    </k>

  claim [example-xyy]:
    <k> #call(#solution, "is_happy",
              pyStr(ch(120, ch(121, ch(121, eps)))))
        => pyBool(false)
    </k>
endmodule
