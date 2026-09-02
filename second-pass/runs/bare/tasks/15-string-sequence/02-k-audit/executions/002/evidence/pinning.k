requires "verification.k"

module PINNING
  imports VERIFICATION

  claim [program-constructor-equality]:
    <mpy>
      <k>
        targetProgram()
        =>
        Module(
          FuncDef("string_sequence", Params("n"),
            If(Compare(Name("n"), CmpOp("<", Int(0))),
              Return(Str("")),
              .Stmts)
            Assign(Name("result"), Str("0"))
            Assign(Name("i"), Int(1))
            While(Compare(Name("i"), CmpOp("<=", Name("n"))),
              Assign(
                Name("result"),
                BinOp(
                  "+",
                  BinOp("+", Name("result"), Str(" ")),
                  Call(Name("str"), Name("i"))))
              Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
            Return(Name("result"))))
      </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <stack> .List </stack>
    </mpy>
endmodule
