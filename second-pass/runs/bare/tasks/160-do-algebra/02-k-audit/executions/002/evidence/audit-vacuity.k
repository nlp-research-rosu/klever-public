requires "verification.k"

module AUDIT-VACUITY
  imports VERIFICATION

  // Fresh false result obligation: 0 - 1 is -1, not 0.
  claim
    <k>
      Module(
        FuncDef("do_algebra", Params("operator", "operand"),
          Assign(
            Name("expression"),
            Call(Name("str"), Subscript(Name("operand"), Int(0))))
          For(TupleExpr(Name("oprt"), Name("oprn")), Call(
            Name("zip"),
            Name("operator"),
            Subscript(Name("operand"), Slice(Int(1), NoBound, NoBound))),
            AugAssign(
              Name("expression"),
              "+",
              BinOp("+", Name("oprt"),
                    Call(Name("str"), Name("oprn")))))
          Return(Call(Name("eval"), Name("expression")))))
      ~> invoke
      => answer(0) ...
    </k>
    <operators> ops(Op("-", .Ops)) </operators>
    <operands> ints(Num(0, Num(1, .Ints))) </operands>
    <expression>
      noText
      => builder(
           Op("-", .Ops),
           Num(0, Num(1, .Ints)),
           .Ops,
           .Ints)
    </expression>
endmodule
