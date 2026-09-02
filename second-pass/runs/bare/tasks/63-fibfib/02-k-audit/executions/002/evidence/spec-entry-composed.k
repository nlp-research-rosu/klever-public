requires "/tmp/audit-work/63-fibfib/candidate/semantic.k"

module FIBFIB-SPEC-ENTRY-COMPOSED
  imports FIBFIB
  imports FIBFIB-VERIFICATION

  claim [program-correct]:
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
    <result> 0 => fibfibMath(N) </result>
    requires 0 <=Int N

  // This is byte-for-byte the candidate's separately proved loop obligation.
  // `trusted` is used only to perform a compositional entry-only proof run.
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
    [trusted]
endmodule
