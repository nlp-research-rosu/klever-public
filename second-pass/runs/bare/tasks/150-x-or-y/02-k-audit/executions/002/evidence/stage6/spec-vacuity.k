requires "spec.k"

module SPEC-VACUITY
  imports LOOP-SPEC

  // Fresh false-result mutation.  The satisfying input below is prime, so the
  // real program returns intVal(34), not the mutated intVal(35).
  claim
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
