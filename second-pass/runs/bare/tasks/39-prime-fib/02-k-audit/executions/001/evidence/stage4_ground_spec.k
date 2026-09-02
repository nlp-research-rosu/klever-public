requires "verification.k"

module STAGE4-GROUND-SPEC
  imports VERIFICATION

  claim [substitute-n1]:
    <k> primeFibProgram => .K </k>
    <env> .Map </env>
    <n> 1 </n>
    <result> noResult => 2 </result>

  claim [substitute-n4]:
    <k> primeFibProgram => .K </k>
    <env> .Map </env>
    <n> 4 </n>
    <result> noResult => 13 </result>

  claim [substitute-n6]:
    <k> primeFibProgram => .K </k>
    <env> .Map </env>
    <n> 6 </n>
    <result> noResult => 233 </result>
endmodule
