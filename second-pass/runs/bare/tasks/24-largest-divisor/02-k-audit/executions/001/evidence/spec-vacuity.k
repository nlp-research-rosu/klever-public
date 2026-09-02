requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Correct loop invariant retained as a support claim so the end-to-end
  // mutation exercises the submitted proof path instead of merely unrolling.
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

  // Deliberately false but satisfiable mutation: some inputs (for example
  // N=4) do return 2, while the ground witness N=15 executes to 5.  Thus the
  // strengthened universal result obligation is false without making the
  // entire destination contradictory.
  claim [false-entry-result-equals-two]:
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
         andBool ?RESULT ==Int 2
endmodule
