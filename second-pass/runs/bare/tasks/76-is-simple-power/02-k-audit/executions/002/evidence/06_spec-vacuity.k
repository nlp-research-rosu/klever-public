requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh auditor mutation.  The unchanged executable program returns true
  // whenever x = 1, so this deliberately false result obligation must fail.
  claim [false-result-on-one]:
    <k> solutionProgram => .K </k>
    <env> .Map => ("x" |-> 1) ("n" |-> N) </env>
    <result> noResult => false </result>
    <x> 1 </x>
    <n> N </n>

endmodule
