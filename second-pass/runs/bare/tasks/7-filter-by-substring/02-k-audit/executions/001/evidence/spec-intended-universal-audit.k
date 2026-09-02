requires "verification.k"

module SPEC-INTENDED-UNIVERSAL-AUDIT
  imports VERIFICATION

  // Auditor-written formulation of the universal entry result that the
  // submitted spec only describes informally as following by induction.
  claim <k> execute(solutionProgram,
                    "filter_by_substring",
                    INPUT:PyList,
                    SUBSTRING:String)
          => filterRef(INPUT, SUBSTRING)
        </k>
    [label(AUDIT-UNIVERSAL-ENTRY)]
endmodule
