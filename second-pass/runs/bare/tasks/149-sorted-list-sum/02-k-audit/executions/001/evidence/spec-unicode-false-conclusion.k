requires "verification.k"

module SPEC-UNICODE-FALSE-CONCLUSION
  imports MPY-SEMANTIC
  imports SORTED-LIST-VERIFICATION

  // The runtime parser maps raw 😀 to these four K String bytes.  This closes
  // in the candidate theory, but CPython returns [] for the raw input ["😀"].
  claim <k>
          Run(solutionProgram,
            Call(Name("sorted_list_sum"),
              ValueExpr(VList("\xf0\x9f\x98\x80"))))
        => Result(VList("\xf0\x9f\x98\x80"))
        </k>
    [label(emoji-retained)]
endmodule
