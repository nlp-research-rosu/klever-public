requires "verification.k"

module AUDIT-BRIDGE-STATE-FIXED
  imports PRIME-FIB-PROGRAM

  // Deliberately asserts the verification bridge's empty final environment.
  // This should fail under the unextended small-step semantics at N = 1.
  claim [bridge-state-witness]:
    <k> primeFibProgram => .K </k>
    <env> .Map => .Map </env>
    <n> 1 </n>
    <result> noResult => 2 </result>
endmodule
