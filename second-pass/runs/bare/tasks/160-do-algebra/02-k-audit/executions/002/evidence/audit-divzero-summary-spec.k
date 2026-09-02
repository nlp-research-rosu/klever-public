requires "verification.k"

module AUDIT-DIVZERO-SUMMARY-SPEC
  imports VERIFICATION

  // This source execution raises ZeroDivisionError. The candidate theory can
  // nevertheless reach an answer-shaped term containing the undefined summary.
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
      => answer(expected(Op("//", .Ops), Num(1, Num(0, .Ints)))) ...
    </k>
    <operators> ops(Op("//", .Ops)) </operators>
    <operands> ints(Num(1, Num(0, .Ints))) </operands>
    <expression>
      noText
      => builder(
           Op("//", .Ops),
           Num(1, Num(0, .Ints)),
           .Ops,
           .Ints)
    </expression>
endmodule
