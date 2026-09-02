requires "verification.k"

module AUDIT-WITNESS-SPEC
  imports VERIFICATION

  claim <k>
          aligned(
            Op("+", Op("*", Op("-", .Ops))),
            Num(3, Num(4, Num(5, .Ints))))
          andBool validOps(Op("+", Op("*", Op("-", .Ops))))
          andBool nonNegative(Num(2, Num(3, Num(4, Num(5, .Ints)))))
          => true
        ... </k>

  claim <k>
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
          => answer(9)
        ... </k>
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
