requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports MPY-SEMANTIC
  imports SORTED-LIST-VERIFICATION

  // Deliberately false: the satisfying input ["aa"] must return ["aa"], not [].
  claim <k>
          Run(solutionProgram,
            Call(Name("sorted_list_sum"), ListExpr(Str("aa"))))
        => Result(VList(.Words))
        </k>
    [label(false-ground-result)]
endmodule
