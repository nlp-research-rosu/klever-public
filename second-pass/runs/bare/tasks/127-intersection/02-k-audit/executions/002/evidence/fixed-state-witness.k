requires "verification.k"

module FIXED-STATE-WITNESS-SPEC
  imports VERIFICATION

  // For N=5,D=2, fixed execution increments divisor to 3 before returning YES.
  // Requiring the final divisor still to be 2 is therefore deliberately false.
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
