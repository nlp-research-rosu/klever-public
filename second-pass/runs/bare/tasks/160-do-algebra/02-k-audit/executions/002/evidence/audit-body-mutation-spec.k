requires "verification.k"

module AUDIT-BODY-MUTATION-SPEC
  imports VERIFICATION

  // The loop body now appends only the operand text and omits every operator.
  // This changes the constructor term executed by the claim itself.
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
              Call(Name("str"), Name("oprn"))))
          Return(Call(Name("eval"), Name("expression")))))
      ~> invoke
      => answer(9) ...
    </k>
    <operators> ops(Op("+", Op("*", Op("-", .Ops)))) </operators>
    <operands> ints(Num(2, Num(3, Num(4, Num(5, .Ints))))) </operands>
    <expression>
      noText
      => builder(
           Op("+", Op("*", Op("-", .Ops))),
           Num(2, Num(3, Num(4, Num(5, .Ints)))),
           .Ops,
           .Ints)
    </expression>
endmodule
