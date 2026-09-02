requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Keep the genuine loop theorem available so failure of the entry mutation
  // is attributable to the changed result obligation.
  claim [loop-invariant]:
    <mpy>
      <k> loop(digitsCond, digitsLoopBody) ~> CONT
        => CONT </k>
      <n> N => 0 </n>
      <acc> A => oddProductFrom(N, A) </acc>
      <digit> D => finalScratchDigit(N, D) </digit>
      <answer> _ANSWER </answer>
    </mpy>
    requires N >=Int 0

  // Fresh false mutation: the real claim returns oddProduct(N).  This demands
  // one more in the observable answer cell while leaving all other obligations
  // unchanged.  N=235 satisfies the precondition and has real result 15, so
  // the mutated obligation demands the false result 16.
  claim [false-entry-result]:
    <mpy>
      <k> Invoke(SolutionProgram, "digits", N) => .K </k>
      <n> 0 </n>
      <acc> 0 => oddProduct(N) </acc>
      <digit> 0 => finalScratchDigit(N, 0) </digit>
      <answer> .K => (oddProduct(N) +Int 1) </answer>
    </mpy>
    requires N >Int 0
endmodule
