requires "verification.k"

module SPEC-HELPER-TARGET
  imports VERIFICATION

  claim
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

  claim
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
