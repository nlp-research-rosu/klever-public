requires "verification.k"

module STAGE4-NO-SUMMARY-EMPTY-ENV
  imports PRIME-FIB-PROGRAM

  // Deliberately asks fixed small-step execution to leave the environment
  // empty. The real semantics populates it, so this must be rejected.
  claim [actual-program-does-not-preserve-empty-env]:
    <k> primeFibProgram => .K </k>
    <env> .Map </env>
    <n> 1 </n>
    <result> noResult => 2 </result>
endmodule
