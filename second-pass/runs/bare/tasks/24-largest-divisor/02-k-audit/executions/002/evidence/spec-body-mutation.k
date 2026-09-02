requires "/tmp/audit-work/src/verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The executed loop decrements by two, so n=15 reaches divisor zero
  // rather than the expected largest proper divisor 5.
  claim [mutated-body-n15]:
    <k>
      Module(
        FuncDef("largest_divisor", Params("n"),
          Assign(Name("divisor"), BinOp("-", Name("n"), Int(1)))
          While(
            Compare(BinOp("%", Name("n"), Name("divisor")), CmpOp("!=", Int(0))),
            Assign(Name("divisor"), BinOp("-", Name("divisor"), Int(2))))
          Return(Name("divisor"))))
    => .K
    </k>
    <arg> 15 </arg>
    <env>
      .Map
    => ("n" |-> 15) ("divisor" |-> 5)
    </env>
    <result> noResult => 5 </result>
endmodule
