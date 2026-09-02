requires "spec.k"

module BODY-MUTATION
  imports LOOP-SPEC

  // Body-sensitivity probe: change the program term actually executed by this
  // claim so the normal final return is y, while retaining the original
  // prime-selection postcondition.  N=7, X=34, Y=12 is a false witness.
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
          Return(Name("y"))))
      => .K
    </k>
    <env> .Map => ?_FINALENV:Map </env>
    <n> N </n>
    <x> X </x>
    <y> Y </y>
    <result> .K => chooseVal(isPrime(N), X, Y) </result>
endmodule
