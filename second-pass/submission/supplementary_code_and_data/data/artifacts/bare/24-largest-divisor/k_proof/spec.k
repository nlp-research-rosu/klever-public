requires "verification.k"

module SPEC
  imports VERIFICATION

  // Direct loop contract.  The precondition records that candidates already
  // skipped above D are non-divisors; the existential result must satisfy the
  // declarative natural-language contract.
  claim [largest-divisor-loop-contract]:
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

  // End-to-end proof of the exact constructor tree in solution.mpy against
  // the declarative contract.
  claim [largest-divisor-natural-contract]:
    <k>
      Module(
        FuncDef("largest_divisor", Params("n"),
          Assign(Name("divisor"), BinOp("-", Name("n"), Int(1)))
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
