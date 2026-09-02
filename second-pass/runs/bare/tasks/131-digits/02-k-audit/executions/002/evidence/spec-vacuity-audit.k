requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  claim [loop-claim]:
    <mpy>
      <k> loop(digitsCond, digitsLoopBody) ~> CONT
        => CONT </k>
      <n> N => 0 </n>
      <acc> A => oddProductFrom(N, A) </acc>
      <digit> D => finalScratchDigit(N, D) </digit>
      <answer> _ANSWER </answer>
    </mpy>
    requires N >=Int 0

  // Deliberately false for the satisfying witness N = 1:
  // execution returns 1, while this destination demands 2 in <answer>.
  claim [false-entry-claim]:
    <mpy>
      <k> Invoke(SolutionProgram, "digits", N) => .K </k>
      <n> 0 </n>
      <acc> 0 => oddProduct(N) </acc>
      <digit> 0 => finalScratchDigit(N, 0) </digit>
      <answer> .K => oddProduct(N) +Int 1 </answer>
    </mpy>
    requires N >Int 0
endmodule
