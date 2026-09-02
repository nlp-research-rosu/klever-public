requires "verification.k"

module ADD-ELEMENTS-SPEC-VACUITY
  imports MPY-VERIFICATION

  // The genuine loop helper is retained so that the mutated entry obligation
  // reaches the return value instead of failing for an unrelated reason.
  claim [loop-invariant]:
    <k> solutionLoop ~> exec(Return(Name("total")) .Stmts) => .K </k>
    <env>
      "arr" |-> A:List
      "k" |-> K:Int
      "total" |-> T:Int
      "i" |-> I:Int
      "value" |-> _V:Int
      => ?_:Map
    </env>
    <arr> A </arr>
    <n> K </n>
    <result> noResult => result(T +Int sumRange(A, I, K)) </result>
    requires 0 <=Int I andBool I <=Int K andBool K <=Int size(A)

  // Fresh false mutation: require one more than the candidate's actual result.
  // Witness: A = ListItem(21), K = 1 satisfies the precondition; execution and
  // sumRange both yield 21, while this target demands 22.
  claim [add-elements-contract-plus-one]:
    <k> solutionProgram => .K </k>
    <env> .Map => ?_:Map </env>
    <arr> A:List </arr>
    <n> K:Int </n>
    <result>
      noResult => result(sumRange(A, 0, K) +Int 1)
    </result>
    requires 1 <=Int K
     andBool K <=Int size(A)
     andBool size(A) <=Int 100
endmodule
