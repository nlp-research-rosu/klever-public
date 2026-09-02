requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: for x = 1, the real generated program returns true.
  // The precondition is satisfiable, for example by X=1, N=4.
  claim [false-return-on-one]:
    <k> solutionProgram => .K </k>
    <env> .Map => ("x" |-> 1) ("n" |-> N) </env>
    <result> noResult => false </result>
    <x> 1 </x>
    <n> N </n>

endmodule
