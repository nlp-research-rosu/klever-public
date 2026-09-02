requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: on A=25, B=15 the program returns 5, not 6.
  claim [gcd-off-by-one]:
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
            Assign(Name("r"), BinOp("%", Name("a"), Name("b")))
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
      noResult => result(gcdSpec(normInt(A), normInt(B)) +Int 1)
    </result>
endmodule
