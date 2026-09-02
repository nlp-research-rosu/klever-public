requires "verification.k"

module ADD-ELEMENTS-SPEC-VACUITY
  imports MPY-VERIFICATION

  claim [loop-invariant-for-mutation]:
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

  // Deliberately false: for A = [21], K = 1, execution returns 21, not 22.
  claim [false-add-elements-contract]:
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
