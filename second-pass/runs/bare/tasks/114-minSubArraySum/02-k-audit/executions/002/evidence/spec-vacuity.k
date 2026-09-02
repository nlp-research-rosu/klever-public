requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Recursive helper correctness, for every finite non-empty integer list and
  // in every caller environment/continuation.
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

  // Target-function correctness against the contract equations.
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

  // End-to-end: parse/load the exact translated module, invoke the required
  // entry point, and obtain the contract value for every non-empty input.
  claim
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
