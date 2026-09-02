requires "verification.k"

module AUDIT-BODY-SENSITIVITY
  imports MPY-VERIFICATION

  // Auditor probe: changing the divisor branch to return x changes the result
  // at n=9. The original result obligation (29) must therefore fail.
  claim [changed-body-original-result]:
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
              Return(Name("x")),
              .Stmts)
            Assign(
              Name("divisor"),
              BinOp("+", Name("divisor"), Int(1))))
          Return(Name("x"))))
      => .K
    </k>
    <env> .Map => ?_FINALENV:Map </env>
    <n> 9 </n>
    <x> 13 </x>
    <y> 29 </y>
    <result> .K => intVal(29) </result>
endmodule
