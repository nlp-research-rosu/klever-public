requires "verification.k"

module ADD-ELEMENTS-SPEC
  imports MPY-VERIFICATION

  // Loop invariant: from any legal index I, the current total plus the
  // mathematical sum over the remaining range is the eventual return value.
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

  // Full contract for every integer array and every k satisfying the prompt.
  claim [add-elements-contract]:
    <k> solutionProgram => .K </k>
    <env> .Map => ?_:Map </env>
    <arr> A:List </arr>
    <n> K:Int </n>
    <result> noResult => result(sumRange(A, 0, K)) </result>
    requires 1 <=Int K
     andBool K <=Int size(A)
     andBool size(A) <=Int 100
endmodule
