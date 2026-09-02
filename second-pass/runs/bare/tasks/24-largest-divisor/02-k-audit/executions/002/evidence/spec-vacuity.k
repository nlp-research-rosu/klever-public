requires "/tmp/audit-work/src/verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation: the result must be unequal to itself.
  claim [false-loop-result]:
    <k>
      While(
        Compare(BinOp("%", Name("n"), Name("divisor")), CmpOp("!=", Int(0))),
        Assign(Name("divisor"), BinOp("-", Name("divisor"), Int(1))))
      ~> (Return(Name("divisor")) .Stmts)
      ~> .K
    => .K
    </k>
    <arg> N </arg>
    <env>
      ("n" |-> N) ("divisor" |-> D)
    => ("n" |-> N) ("divisor" |-> ?RESULT)
    </env>
    <result> noResult => ?RESULT </result>
    requires N >Int 1
         andBool D >Int 0
         andBool D <Int N
         andBool noDivisorFrom(N, D +Int 1, N -Int 1)
    ensures isLargestProperDivisor(N, ?RESULT)
         andBool ?RESULT =/=Int ?RESULT
endmodule
