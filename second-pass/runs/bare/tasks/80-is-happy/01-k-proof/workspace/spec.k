requires "verification.k"

module SPEC
  imports VERIFICATION

  // Recursive helper correctness.  #short3 in the semantics supplies the
  // exhaustive constructor split; the recursive branch uses this claim as a
  // circularity only after consuming one character.
  claim <k> #call(#solution, "check_happy_triples", pyStr(S))
          => pyBool(#allTriples(S))
        </k>

  // Required entry point for every finite input string.
  claim <k> #call(#solution, "is_happy", pyStr(S))
          => pyBool(#happy(S))
        </k>

  // The six examples from prompt.py are also executable proof claims.
  claim <k> #call(#solution, "is_happy", pyStr(ch(97, eps)))
          => pyBool(false)
        </k>
  claim <k> #call(#solution, "is_happy", pyStr(ch(97, ch(97, eps))))
          => pyBool(false)
        </k>
  claim <k> #call(#solution, "is_happy",
                  pyStr(ch(97, ch(98, ch(99, ch(100, eps))))))
          => pyBool(true)
        </k>
  claim <k> #call(#solution, "is_happy",
                  pyStr(ch(97, ch(97, ch(98, ch(98, eps))))))
          => pyBool(false)
        </k>
  claim <k> #call(#solution, "is_happy",
                  pyStr(ch(97, ch(100, ch(98, eps)))))
          => pyBool(true)
        </k>
  claim <k> #call(#solution, "is_happy",
                  pyStr(ch(120, ch(121, ch(121, eps)))))
          => pyBool(false)
        </k>
endmodule
