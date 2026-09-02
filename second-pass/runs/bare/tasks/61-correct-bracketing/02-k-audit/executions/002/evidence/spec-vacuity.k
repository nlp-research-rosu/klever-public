requires "/tmp/audit-work/61-correct-bracketing-audit/candidate/verification.k"

module SPEC-VACUITY
  imports MPY-VERIFICATION

  // Fresh false-result mutation.  The real submitted program is executed from
  // its ordinary initial state on the satisfying input "".  Both Python
  // implementations and fixed K execution return true; the mutated
  // destination deliberately requires false.
  claim [false-empty-result]:
    <mpy>
      <k> Run(solutionProgram, "correct_bracketing", "")
        => boolVal(false) </k>
      <functions> .Map => ?_FS:Map </functions>
      <env> .Map => ?_ENV:Map </env>
    </mpy>
endmodule
