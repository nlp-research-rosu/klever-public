requires "verification.k"

module AUDIT-LABELED-SPEC
  imports VERIFICATION

  claim [entry]:
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
      => answer(expected(OS, Num(FIRST, REST))) ...
    </k>
    <operators> ops(OS) </operators>
    <operands> ints(Num(FIRST, REST)) </operands>
    <expression>
      noText => builder(OS, Num(FIRST, REST), .Ops, .Ints)
    </expression>
    requires aligned(OS, REST)
     andBool validOps(OS)
     andBool nonNegative(Num(FIRST, REST))

  claim [example]:
    <k> check(expected(
           Op("+", Op("*", Op("-", .Ops))),
           Num(2, Num(3, Num(4, Num(5, .Ints))))))
         => checked(9) ... </k>

  claim [right-pow]:
    <k> check(expected(
           Op("**", Op("**", .Ops)),
           Num(2, Num(3, Num(2, .Ints)))))
         => checked(512) ... </k>

  claim [floor-precedence]:
    <k> check(expected(
           Op("//", Op("+", .Ops)),
           Num(7, Num(3, Num(2, .Ints)))))
         => checked(4) ... </k>

  claim [mul-precedence]:
    <k> check(expected(
           Op("+", Op("*", .Ops)),
           Num(2, Num(3, Num(4, .Ints)))))
         => checked(14) ... </k>

  claim [left-sub]:
    <k> check(expected(
           Op("-", Op("-", .Ops)),
           Num(10, Num(3, Num(2, .Ints)))))
         => checked(5) ... </k>
endmodule
