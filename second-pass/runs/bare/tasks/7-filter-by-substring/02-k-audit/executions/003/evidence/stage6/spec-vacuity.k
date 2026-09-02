requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: "cde" does not contain "a", so the actual result
  // excludes it. The fixed input has no precondition and is realizable.
  claim <k> execute(solutionProgram,
                    "filter_by_substring",
                    Cons("abc", Cons("bacd", Cons("cde", Cons("array", Nil)))),
                    "a")
          => Cons("abc", Cons("bacd", Cons("cde", Cons("array", Nil))))
        </k>
    [label(FALSE-PROMPT-RESULT)]
endmodule
