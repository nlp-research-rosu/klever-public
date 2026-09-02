requires "verification.k"

module GROUND-WITNESSES
  imports VERIFICATION

  // Satisfies the loop claim's N >= 0 precondition with
  // N=235, A=0, D=0, CONT=.K, ANSWER=.K.
  claim [loop-235]:
    <mpy>
      <k> loop(digitsCond, digitsLoopBody) => .K </k>
      <n> 235 => 0 </n>
      <acc> 0 => 15 </acc>
      <digit> 0 => 2 </digit>
      <answer> .K </answer>
    </mpy>

  // Satisfies the entry claim's N > 0 precondition with N=235.
  claim [entry-235]:
    <mpy>
      <k> Invoke(SolutionProgram, "digits", 235) => .K </k>
      <n> 0 </n>
      <acc> 0 => 15 </acc>
      <digit> 0 => 2 </digit>
      <answer> .K => 15 </answer>
    </mpy>
endmodule
