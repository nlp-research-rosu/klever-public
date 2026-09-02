requires "verification.k"

module ADEQUACY-PROBE
  imports VERIFICATION

  // The unrestricted theorem the candidate would need to connect its
  // executable sorter to the declarative stable-sort equations.
  claim [label(all-lists-sort)]:
        <py>
          <k>
            sortWith(VS:Vals, PointKey, solutionDefs)
            => specSort(VS)
          </k>
          <program> solutionProgram </program>
          <input> ListExpr(.Exprs) </input>
          <output> NoValue </output>
        </py>
endmodule
