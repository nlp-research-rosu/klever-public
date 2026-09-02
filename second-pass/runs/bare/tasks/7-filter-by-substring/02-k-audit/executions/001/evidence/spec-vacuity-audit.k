requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh false result mutation. The input is the prompt's satisfiable ground
  // example, but the postcondition wrongly drops the matching final "array".
  claim <k> execute(solutionProgram,
                    "filter_by_substring",
                    Cons("abc", Cons("bacd", Cons("cde", Cons("array", Nil)))),
                    "a")
          => Cons("abc", Cons("bacd", Nil))
        </k>
    [label(AUDIT-FALSE-PROMPT-RESULT)]
endmodule
