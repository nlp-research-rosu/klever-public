requires "verification.k"

module MAIN-NO-BRIDGE-SPEC
  imports VERIFICATION

  claim [all-space-separated-strings]:
    <k>
      execute(histogramProgram(), INPUT:String)
      => histogramSpecString(INPUT)
    </k>
endmodule
