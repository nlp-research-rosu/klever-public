requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false for the satisfiable concrete input "a":
  // both trusted canonical Python and submitted Python return {"a": 1}.
  claim [false-single-count]:
    <k>
      execute(histogramProgram(), "a")
      => pyDict(pyString("a") |-> pyInt(2),
                ListItem(pyString("a")))
    </k>
endmodule
