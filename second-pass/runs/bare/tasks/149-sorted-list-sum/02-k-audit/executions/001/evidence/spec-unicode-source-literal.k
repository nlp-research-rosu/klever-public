requires "verification.k"

module SPEC-UNICODE-SOURCE-LITERAL
  imports MPY-SEMANTIC
  imports SORTED-LIST-VERIFICATION

  // K-definition-source parsing treats this literal as one character.
  claim <k>
          Run(solutionProgram,
            Call(Name("sorted_list_sum"), ValueExpr(VList("😀"))))
        => Result(VList(.Words))
        </k>
    [label(source-emoji-filtered)]
endmodule
