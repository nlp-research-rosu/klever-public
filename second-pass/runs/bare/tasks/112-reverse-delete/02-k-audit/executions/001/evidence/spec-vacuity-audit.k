requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: the satisfying input ("abcde", "ae") returns "bcd",
  // not "bcdx".  The boolean component remains unchanged to isolate the
  // result-string obligation.
  claim [false-result]:
        <k>
          execute(solutionPgm, "abcde", "ae")
          => returned(tupleVal(strVal("bcdx"), boolVal(false)))
        </k>
endmodule
