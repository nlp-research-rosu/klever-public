requires "verification.k"

module SPEC
  imports VERIFICATION

  // Generalized loop invariant.  K uses this claim circularly after one
  // concrete loop iteration, which is induction on the shrinking quotient.
  claim
    <mpy>
      <k> loop(digitsCond, digitsLoopBody) ~> CONT
        => CONT </k>
      <n> N => 0 </n>
      <acc> A => oddProductFrom(N, A) </acc>
      <digit> D => finalScratchDigit(N, D) </digit>
      <answer> _ANSWER </answer>
    </mpy>
    requires N >=Int 0

  // End-to-end contract for every positive integer accepted by the prompt.
  claim
    <mpy>
      <k> Invoke(SolutionProgram, "digits", N) => .K </k>
      <n> 0 </n>
      <acc> 0 => oddProduct(N) </acc>
      <digit> 0 => finalScratchDigit(N, 0) </digit>
      <answer> .K => oddProduct(N) </answer>
    </mpy>
    requires N >Int 0
endmodule
