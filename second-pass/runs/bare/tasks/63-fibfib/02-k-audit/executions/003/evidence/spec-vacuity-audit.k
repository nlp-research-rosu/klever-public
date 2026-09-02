requires "semantic.k"

module FIBFIB-SPEC-VACUITY
  imports FIBFIB
  imports FIBFIB-VERIFICATION

  // AUDITOR FALSE MUTATION: the real result is fibfibMath(N), not +Int 1.
  claim [program-wrong-off-by-one]:
    <k> fibfibProgram ~> invoke(N) => .K </k>
    <env>
      .Map
      =>
      "a" |-> fibfibMath(N)
      "b" |-> fibfibMath(N +Int 1)
      "c" |-> fibfibMath(N +Int 2)
      "i" |-> N
      "n" |-> N
    </env>
    <result> 0 => fibfibMath(N) +Int 1 </result>
    requires 0 <=Int N

  // Preserve the genuine circularity so the mutation changes only the
  // result-constraining target obligation.
  claim [loop-invariant]:
    <k> While(loopCondition, loopBody)
         ~> (Return(Name("a")) .Stmts)
         ~> finish
      => .K
    </k>
    <env>
      "a" |-> fibfibMath(I)
      "b" |-> fibfibMath(I +Int 1)
      "c" |-> fibfibMath(I +Int 2)
      "i" |-> I
      "n" |-> N
      =>
      "a" |-> fibfibMath(N)
      "b" |-> fibfibMath(N +Int 1)
      "c" |-> fibfibMath(N +Int 2)
      "i" |-> N
      "n" |-> N
    </env>
    <result> _R => fibfibMath(N) </result>
    requires 0 <=Int I andBool I <=Int N
endmodule
