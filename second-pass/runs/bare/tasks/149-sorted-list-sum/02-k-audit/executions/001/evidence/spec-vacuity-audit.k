requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports MPY-SEMANTIC
  imports SORTED-LIST-VERIFICATION

  // False for the satisfiable witness INPUT = .Words: the real result is empty.
  claim <k>
          Run(solutionProgram,
            Call(Name("sorted_list_sum"), ValueExpr(VList(INPUT:Words))))
        => Result(VList("AUDIT_SENTINEL", sortedListSumSpec(INPUT)))
        </k>
    [label(audit-false-result)]
endmodule
