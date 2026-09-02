requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the submitted program returns [] on the satisfying
  // input [], not [1].
  claim
    <mpy>
      <k>
        #run(solutionProgram, ListV(.Values))
        => ListV((IntV(1), .Values))
      </k>
    </mpy>
    [label(false-empty-result)]
endmodule
