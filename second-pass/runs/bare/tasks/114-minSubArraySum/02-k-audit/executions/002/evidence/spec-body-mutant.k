requires "verification-body-mutant.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION

  claim
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
