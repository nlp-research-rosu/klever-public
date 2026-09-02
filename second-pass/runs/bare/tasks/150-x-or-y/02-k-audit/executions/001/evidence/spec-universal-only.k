requires "verification.k"

module LOOP-SPEC-FOR-UNIVERSAL
  imports MPY-VERIFICATION

  claim [loop-invariant-for-universal]:
    <k>
      eval(
        Compare(
          BinOp("*", Name("divisor"), Name("divisor")),
          CmpOp("<=", Name("n"))))
      ~> whileBranch(
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
          BinOp("+", Name("divisor"), Int(1))),
        .Stmts)
      ~> exec(Return(Name("x")))
      => .K
    </k>
    <env>
      ("divisor" |-> intVal(D))
      ("n" |-> intVal(N))
      ("x" |-> intVal(X))
      ("y" |-> intVal(Y))
      => ?_FINALENV:Map
    </env>
    <n> N </n>
    <x> X </x>
    <y> Y </y>
    <result> .K => chooseVal(primeFrom(N, D), X, Y) </result>
    requires 2 <=Int D
endmodule

module SPEC-UNIVERSAL-ONLY
  imports LOOP-SPEC-FOR-UNIVERSAL

  claim [universal-entry-only]:
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
    <n> N </n>
    <x> X </x>
    <y> Y </y>
    <result> .K => chooseVal(isPrime(N), X, Y) </result>
endmodule
