requires "verification.k"

module AUDIT-BRIDGE-STATE-EXTENDED
  imports VERIFICATION

  // The operational bridge makes this false fixed-semantics state close.
  claim [bridge-state-witness]:
    <k> primeFibProgram => .K </k>
    <env> .Map => .Map </env>
    <n> 1 </n>
    <result> noResult => 2 </result>
endmodule
