requires "verification.k"

module LOOP-SPEC
  imports MPY-VERIFICATION

  // Generalized loop invariant.  It deliberately starts at an arbitrary
  // D >= 2 so that one non-dividing iteration re-enters the same claim at
  // D + 1 and K's reachability prover can apply circularity.
  claim [loop-invariant]:
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

module SPEC
  imports LOOP-SPEC

  claim [universal-entry]:
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

  claim [example-seven]:
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
    <result> .K => intVal(34) </result>

  claim [example-fifteen]:
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
    <n> 15 </n>
    <x> 8 </x>
    <y> 5 </y>
    <result> .K => intVal(5) </result>
endmodule
