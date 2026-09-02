requires "verification.k"

module SPEC-CONTEXT
  imports VERIFICATION

  // Ground control-sensitivity check for the entry claim's arbitrary CONT.
  claim
    <k>
      call(
        Module(
          FuncDef("change_base", Params("x", "base"),
            If(Compare(Name("x"), CmpOp("<", Name("base"))),
              Return(Call(Name("str"), Name("x"))),
              .Stmts)
            Return(
              BinOp(
                "+",
                Call(
                  Name("change_base"),
                  BinOp("//", Name("x"), Name("base")),
                  Name("base")),
                Call(Name("str"),
                     BinOp("%", Name("x"), Name("base"))))))),
        "change_base", intVal(8), intVal(3))
      ~> binRight("+", strVal("P"))
    =>
      strVal("P22")
    </k>
endmodule
