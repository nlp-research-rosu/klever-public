requires "verification.k"

module BRIDGE-STATE-WITNESS-SPEC
  imports VERIFICATION-WITH-LOOP-LEMMA

  // This is the same false post-state as FIXED-STATE-WITNESS-SPEC.
  // The operational bridge preserves divisor=2 and therefore proves it.
  claim <k>
          While(Compare(
            BinOp("*", Name("divisor"), Name("divisor")),
            CmpOp("<=", Name("length"))),
            If(Compare(
              BinOp("%", Name("length"), Name("divisor")),
              CmpOp("==", Int(0))),
              Return(Str("NO")),
              .Stmts)
            Assign(Name("divisor"), BinOp("+", Name("divisor"), Int(1))))
          ~> (Return(Str("YES")) .Stmts)
          => strVal("YES")
        </k>
        <env>
          "length" |-> intVal(5)
          "divisor" |-> intVal(2)
        </env>
endmodule
