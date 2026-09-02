requires "verification.k"

module SPEC-VACUITY-AUDIT
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

  // Deliberately false: every non-empty input is required to return one more
  // than the result already established by the unchanged call-level claims.
  claim [false-entry-plus-one]:
    <py>
      <k> solutionProgram
        => pyInt(minSubarray(cons(H, T)) +Int 1) ~> .K </k>
      <entry> "minSubArraySum" </entry>
      <args> pyList(cons(H, T)) </args>
      <functions> .Map => solutionFunctions </functions>
      <env> .Map </env>
      <callStack> .List </callStack>
      <callDepth> z </callDepth>
    </py>
endmodule
