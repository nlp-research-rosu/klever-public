requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Inner-loop invariant: B records whether any already-visited divisor was
  // found; noFactor(C,D) describes exactly the unvisited suffix.
  claim [trial-correct]:
    <k> trial(C, D, B, N) ~> K
      => scan(C +Int 1, N)
         ~> prependIf(C, B andBool noFactor(C, D)) ~> K
    </k>
    requires C >=Int 2 andBool D >=Int 2

  // Outer-loop invariant: scan(C,N) returns every and only prime in [C,N),
  // in increasing order.
  claim [scan-correct]:
    <k> scan(C, N) ~> K
      => primesFrom(C, N) ~> K
    </k>
    requires C >=Int 2

  // End-to-end claim over every non-negative input.  The complete source AST
  // below is identical to solution.mpy; semantic.k only lowers this tree.
  claim [count-up-to-body-mutated]:
    <k>
      Module(
        FuncDef("count_up_to", Params("n"),
          Assign(Name("primes"), ListExpr(.Exprs))
          Assign(Name("candidate"), Int(3))
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
    <result> .K => primesBelow(N) </result>
    requires N >=Int 0
endmodule
