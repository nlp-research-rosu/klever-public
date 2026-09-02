requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately wrong program body: for A=25, B=15 it returns 15, not 5.
  claim [mutated-body-is-not-gcd]:
    <k>
      Module(
        FuncDef("greatest_common_divisor", Params("a", "b"),
          If(Compare(Name("a"), CmpOp("<", Int(0))),
            Assign(Name("a"), UnaryOp("-", Name("a"))),
            .Stmts)
          If(Compare(Name("b"), CmpOp("<", Int(0))),
            Assign(Name("b"), UnaryOp("-", Name("b"))),
            .Stmts)
          Assign(Name("r"), Int(0))
          While(Compare(Name("b"), CmpOp("!=", Int(0))),
            Assign(Name("r"), Int(0))
            Assign(Name("a"), Name("b"))
            Assign(Name("b"), Name("r"))
          )
          Return(Name("a"))
        )
      )
      => .K
    </k>
    <env>
      .Map
      => ("a" |-> gcdSpec(normInt(A), normInt(B)))
         ("b" |-> 0) ("r" |-> 0)
    </env>
    <inputA> A </inputA>
    <inputB> B </inputB>
    <result>
      noResult => result(gcdSpec(normInt(A), normInt(B)))
    </result>
endmodule
