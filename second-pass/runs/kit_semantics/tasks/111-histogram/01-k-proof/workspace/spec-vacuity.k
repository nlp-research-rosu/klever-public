requires "spec.k"

module SPEC-VACUITY
  imports SPEC

  // Deliberately false for the satisfiable input "a": the proven summary
  // contains {"a": 1}, not {"a": 2}.
  claim [false-result]:
    <k>
      histogramResult(iCons(97, .IntSeq))
      =>
      dictV(
        vCons(str(iCons(97, .IntSeq)), .ValSeq),
        vCons(2, .ValSeq))
    </k>
endmodule
