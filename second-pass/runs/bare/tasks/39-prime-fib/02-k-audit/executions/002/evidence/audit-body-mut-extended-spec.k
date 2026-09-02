requires "audit-body-mut-verification.k"

module AUDIT-BODY-MUT-EXTENDED-SPEC
  imports AUDIT-BODY-MUT-VERIFICATION

  // The unchanged bridge still claims 2 and an empty environment.
  claim [mutated-bridge-result]:
    <k> primeFibProgram => .K </k>
    <env> .Map => .Map </env>
    <n> 1 </n>
    <result> noResult => 2 </result>
endmodule
