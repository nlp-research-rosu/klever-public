requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports VERIFICATION

  // Fresh false result mutation. N=1 satisfies the precondition, but the
  // submitted program, both Python implementations, and primeFibSpec return 2,
  // not 3.
  claim [false-off-by-one]:
    <k> primeFibProgram => .K </k>
    <env> .Map </env>
    <n> N </n>
    <result> noResult => primeFibSpec(N) +Int 1 </result>
    requires N >Int 0
endmodule
