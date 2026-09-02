requires "verification.k"

module SPEC-INTENDED-AUDIT
  imports VERIFICATION

  // Diagnostic statement of the missing result theorem. The constructor
  // comparison in evidence/04-constructor-compare.log establishes that this
  // Module/FuncDef binding and body is the submitted solution.mpy term.
  claim [full-program-result]:
        <k>
          Module(FuncDef("smallest_change", Params("arr"),
                         #smallestChangeBody))
          => .K
        </k>
        <input> L </input>
        <result> .K => minimumPalindromeChanges(L) </result>
endmodule
