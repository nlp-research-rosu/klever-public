requires "verification.k"

module SPEC-PREFIX-ONLY
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
endmodule
