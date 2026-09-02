requires "verification.k"

module SPEC-COMPOSED-ENTRY
  imports VERIFICATION

  // Reviewer-authored composition target: the submitted active-path prefix
  // followed by its submitted loop invariant, with the full result exposed.
  claim [active-path-full-result]:
    <k> solutionProgram => .K </k>
    <env>
      .Map => ("x" |-> X) ("n" |-> N)
              ("power" |-> powerCeiling(N, X, N))
    </env>
    <result> noResult => simplePowerSpec(X, N) </result>
    <x> X </x>
    <n> N </n>
    requires 1 <Int X andBool 2 <=Int N

  claim [loop-correct-review-copy]:
    <k>
      While(Compare(Name("power"), CmpOp("<", Name("x"))),
        Assign(Name("power"), BinOp("*", Name("power"), Name("n"))))
      ~> exec(Return(Compare(Name("power"), CmpOp("==", Name("x")))))
      => .K
    </k>
    <env>
      ("x" |-> X) ("n" |-> N) ("power" |-> P)
      => ("x" |-> X) ("n" |-> N)
         ("power" |-> powerCeiling(P, X, N))
    </env>
    <result> noResult => powerCeiling(P, X, N) ==Int X </result>
    <x> X </x>
    <n> N </n>
    requires 1 <Int X andBool 2 <=Int N andBool 0 <Int P

endmodule
