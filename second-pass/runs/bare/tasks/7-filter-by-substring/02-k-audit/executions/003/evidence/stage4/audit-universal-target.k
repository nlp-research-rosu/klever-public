requires "verification.k"

module AUDIT-UNIVERSAL-TARGET
  imports VERIFICATION

  claim <k> execute(solutionProgram,
                    "filter_by_substring",
                    INPUT:PyList,
                    SUBSTRING:String)
          => filterRef(INPUT, SUBSTRING)
        </k>
    [label(AUDIT-UNIVERSAL-TARGET)]
endmodule
