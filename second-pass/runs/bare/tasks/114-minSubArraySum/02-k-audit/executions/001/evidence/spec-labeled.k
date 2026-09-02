requires "verification.k"

module SPEC-LABELED
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

  claim [entry]:
    <py>
      <k> solutionProgram => pyInt(minSubarray(cons(H, T))) ~> .K </k>
      <entry> "minSubArraySum" </entry>
      <args> pyList(cons(H, T)) </args>
      <functions> .Map => solutionFunctions </functions>
      <env> .Map </env>
      <callStack> .List </callStack>
      <callDepth> z </callDepth>
    </py>
endmodule
