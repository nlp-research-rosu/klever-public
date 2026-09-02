requires "verification.k"

module STAGE6-SPEC-VACUITY
  imports VERIFICATION

  // Fresh false result obligation. n=1 satisfies the entry domain, but both
  // Python implementations and primeFibSpec(1) return 2, not 3.
  claim [false-result-n1]:
    <k> primeFibProgram => .K </k>
    <env> .Map </env>
    <n> 1 </n>
    <result> noResult => 3 </result>
endmodule
