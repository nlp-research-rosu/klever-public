requires "verification.k"

module SPEC
  imports VERIFICATION

  // Universal source-level theorem.  Under the prompt's shape and value
  // preconditions, executing the exact translated function reaches the
  // precedence-defined mathematical result.
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

  // Prompt example: multiplication binds tighter than addition/subtraction.
  claim <k> check(expected(
                 Op("+", Op("*", Op("-", .Ops))),
                 Num(2, Num(3, Num(4, Num(5, .Ints))))))
             => checked(9) ... </k>

  // Exponentiation is right associative: 2 ** (3 ** 2), not (2 ** 3) ** 2.
  claim <k> check(expected(
                 Op("**", Op("**", .Ops)),
                 Num(2, Num(3, Num(2, .Ints)))))
             => checked(512) ... </k>

  // Floor division is in the multiplicative precedence group.
  claim <k> check(expected(
                 Op("//", Op("+", .Ops)),
                 Num(7, Num(3, Num(2, .Ints)))))
             => checked(4) ... </k>

  // Addition is performed after the following multiplication: 2 + 3 * 4.
  claim <k> check(expected(
                 Op("+", Op("*", .Ops)),
                 Num(2, Num(3, Num(4, .Ints)))))
             => checked(14) ... </k>

  // Subtraction is left associative: (10 - 3) - 2.
  claim <k> check(expected(
                 Op("-", Op("-", .Ops)),
                 Num(10, Num(3, Num(2, .Ints)))))
             => checked(5) ... </k>
endmodule
