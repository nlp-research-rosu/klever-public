requires "verification.k"

module SPEC
  imports VERIFICATION

  // General functional-correctness claim for the contract's positive index.
  claim [prime-fib-correct]:
    <k> primeFibProgram => .K </k>
    <env> .Map </env>
    <n> N </n>
    <result> noResult => primeFibSpec(N) </result>
    requires N >Int 0

  claim [example-1]:
    <k> primeFibProgram => .K </k>
    <env> .Map </env>
    <n> 1 </n>
    <result> noResult => 2 </result>

  claim [example-2]:
    <k> primeFibProgram => .K </k>
    <env> .Map </env>
    <n> 2 </n>
    <result> noResult => 3 </result>

  claim [example-3]:
    <k> primeFibProgram => .K </k>
    <env> .Map </env>
    <n> 3 </n>
    <result> noResult => 5 </result>

  claim [example-4]:
    <k> primeFibProgram => .K </k>
    <env> .Map </env>
    <n> 4 </n>
    <result> noResult => 13 </result>

  claim [example-5]:
    <k> primeFibProgram => .K </k>
    <env> .Map </env>
    <n> 5 </n>
    <result> noResult => 89 </result>
endmodule
