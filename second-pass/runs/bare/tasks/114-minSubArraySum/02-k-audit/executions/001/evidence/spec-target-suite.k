requires "verification.k"

module SPEC-TARGET-SUITE
  imports VERIFICATION

  claim [prefix-helper]:
    <py>
      <k> apply(funref("min_prefix_sum"), pyList(cons(H, T))) ~> K
        => returned(D, pyInt(minPrefix(cons(H, T)))) ~> K </k>
      <entry> ENTRY </entry>
      <args> ARGS </args>
      <functions> solutionFunctions </functions>
      <env> RHO </env>
      <callStack> STACK </callStack>
      <callDepth> D </callDepth>
    </py>

  claim [target-call]:
    <py>
      <k> apply(funref("minSubArraySum"), pyList(cons(H, T))) ~> K
        => returned(D, pyInt(minSubarray(cons(H, T)))) ~> K </k>
      <entry> ENTRY </entry>
      <args> ARGS </args>
      <functions> solutionFunctions </functions>
      <env> RHO </env>
      <callStack> STACK </callStack>
      <callDepth> D </callDepth>
    </py>
endmodule
