requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim [trial-correct]:
    <k> trial(C, D, B, N) ~> K
      => scan(C +Int 1, N)
         ~> prependIf(C, B andBool noFactor(C, D)) ~> K
    </k>
    requires C >=Int 2 andBool D >=Int 2

  claim [scan-correct]:
    <k> scan(C, N) ~> K
      => primesFrom(C, N) ~> K
    </k>
    requires C >=Int 2

  // Deliberately false at the satisfiable input N = 5:
  // the real result is cons(2, cons(3, nil)), not nil.
  claim [false-count-up-to]:
    <k>
      Module(
        FuncDef("count_up_to", Params("n"),
          Assign(Name("primes"), ListExpr(.Exprs))
          Assign(Name("candidate"), Int(2))
          While(Compare(Name("candidate"), CmpOp("<", Name("n"))),
            Assign(Name("is_prime"), Bool(true))
            Assign(Name("divisor"), Int(2))
            While(Compare(
              BinOp("*", Name("divisor"), Name("divisor")),
              CmpOp("<=", Name("candidate"))),
              If(Compare(
                BinOp("%", Name("candidate"), Name("divisor")),
                CmpOp("==", Int(0))),
                Assign(Name("is_prime"), Bool(false)) .Stmts,
                .Stmts)
              Assign(Name("divisor"),
                BinOp("+", Name("divisor"), Int(1))))
            If(Name("is_prime"),
              Assign(Name("primes"),
                BinOp("+", Name("primes"),
                  ListExpr(Name("candidate"), .Exprs))) .Stmts,
              .Stmts)
            Assign(Name("candidate"),
              BinOp("+", Name("candidate"), Int(1))))
          Return(Name("primes"))))
      => .K
    </k>
    <n> N </n>
    <result> .K => nil </result>
    requires N ==Int 5
endmodule
