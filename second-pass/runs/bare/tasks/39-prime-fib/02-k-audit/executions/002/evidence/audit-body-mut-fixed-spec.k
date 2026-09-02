requires "audit-body-mut-verification.k"

module AUDIT-BODY-MUT-FIXED-SPEC
  imports AUDIT-BODY-MUT-PROGRAM

  // Under fixed small-step execution, returning a after N=1 yields 1.
  claim [mutated-fixed-result]:
    <k> primeFibProgram => .K </k>
    <env> .Map =>
      "a" |-> 1 "b" |-> 2 "c" |-> 2 "count" |-> 1
      "divisor" |-> 2 "n" |-> 1 "prime" |-> true
    </env>
    <n> 1 </n>
    <result> noResult => 1 </result>
endmodule
