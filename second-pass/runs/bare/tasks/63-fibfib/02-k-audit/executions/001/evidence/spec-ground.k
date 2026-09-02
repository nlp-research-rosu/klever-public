requires "semantic.k"

module FIBFIB-SPEC-GROUND
  imports FIBFIB
  imports FIBFIB-VERIFICATION

  // N = 5 satisfies the entry precondition 0 <= N.
  claim [program-ground-n5]:
    <k> fibfibProgram ~> invoke(5) => .K </k>
    <env>
      .Map
      =>
      "a" |-> 4
      "b" |-> 7
      "c" |-> 13
      "i" |-> 5
      "n" |-> 5
    </env>
    <result> 0 => 4 </result>

  // I = 2, N = 5 satisfies the loop precondition 0 <= I <= N.
  claim [loop-ground-i2-n5]:
    <k> While(loopCondition, loopBody)
         ~> (Return(Name("a")) .Stmts)
         ~> finish
      => .K
    </k>
    <env>
      "a" |-> 1
      "b" |-> 1
      "c" |-> 2
      "i" |-> 2
      "n" |-> 5
      =>
      "a" |-> 4
      "b" |-> 7
      "c" |-> 13
      "i" |-> 5
      "n" |-> 5
    </env>
    <result> 123 => 4 </result>
endmodule
