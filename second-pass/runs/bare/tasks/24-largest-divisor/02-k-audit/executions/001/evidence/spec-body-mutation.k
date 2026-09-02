requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The original loop theorem is present, but its D < N guard prevents it
  // from legitimizing the mutated initialization below.
  claim [loop-support]:
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

  // Body-sensitivity mutation: initialize divisor to N rather than N - 1.
  // The changed program immediately returns N, which is not a proper divisor.
  claim [wrong-initialization]:
    <k>
      Module(
        FuncDef("largest_divisor", Params("n"),
          Assign(Name("divisor"), Name("n"))
          While(
            Compare(BinOp("%", Name("n"), Name("divisor")), CmpOp("!=", Int(0))),
            Assign(Name("divisor"), BinOp("-", Name("divisor"), Int(1))))
          Return(Name("divisor"))))
    => .K
    </k>
    <arg> N </arg>
    <env>
      .Map
    => ("n" |-> N) ("divisor" |-> ?RESULT)
    </env>
    <result> noResult => ?RESULT </result>
    requires N >Int 1
    ensures isLargestProperDivisor(N, ?RESULT)
endmodule
