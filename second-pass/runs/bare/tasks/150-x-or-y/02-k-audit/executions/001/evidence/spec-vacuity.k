requires "verification.k"

module AUDIT-VACUITY
  imports MPY-VERIFICATION

  // Fresh auditor mutation: the real program returns 34 for this satisfying
  // prime input, so requiring 35 must be rejected if the result is constrained.
  claim [false-seven-result]:
    <k>
      Module(
        FuncDef("x_or_y", Params("n", "x", "y"),
          If(
            Compare(Name("n"), CmpOp("<", Int(2))),
            Return(Name("y")),
            .Stmts)
          Assign(Name("divisor"), Int(2))
          While(
            Compare(
              BinOp("*", Name("divisor"), Name("divisor")),
              CmpOp("<=", Name("n"))),
            If(
              Compare(
                BinOp("%", Name("n"), Name("divisor")),
                CmpOp("==", Int(0))),
              Return(Name("y")),
              .Stmts)
            Assign(
              Name("divisor"),
              BinOp("+", Name("divisor"), Int(1))))
          Return(Name("x"))))
      => .K
    </k>
    <env> .Map => ?_FINALENV:Map </env>
    <n> 7 </n>
    <x> 34 </x>
    <y> 12 </y>
    <result> .K => intVal(35) </result>
endmodule
