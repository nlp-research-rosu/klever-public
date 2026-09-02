requires "/tmp/audit-work/63-fibfib/candidate/semantic.k"

module FIBFIB-SPEC-VACUITY
  imports FIBFIB
  imports FIBFIB-VERIFICATION

  // Fresh false mutation: the exact program is required to return F(N)+1.
  // N=0 satisfies the precondition and returns 0, not 1.
  claim [program-correct-off-by-one]:
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

  // Preserve the candidate's real helper exactly, so the entry can reach the
  // result obligation rather than failing for a missing circularity.
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
