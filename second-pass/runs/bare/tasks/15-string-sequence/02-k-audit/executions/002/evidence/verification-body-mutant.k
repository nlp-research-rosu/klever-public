requires "semantic.k"

module VERIFICATION
  imports MPY

  syntax String ::= sequenceFrom(Int, Int, String) [function]
                  | sequence(Int) [function]
  syntax Int ::= indexAfter(Int, Int) [function]
  syntax Expr ::= loopCondition() [function]
  syntax Stmts ::= loopBody() [function]
                   | targetBody() [function]
  syntax Function ::= targetFunction() [function]
  syntax Module ::= targetProgram() [function]

  rule sequenceFrom(I, N, S)
       => sequenceFrom(I +Int 1, N, S +String " " +String Int2String(I))
       requires I <=Int N
  rule sequenceFrom(I, N, S) => S
       requires I >Int N

  rule sequence(N) => "" requires N <Int 0
  rule sequence(N) => sequenceFrom(1, N, "0") requires N >=Int 0

  rule indexAfter(I, N) => indexAfter(I +Int 1, N)
       requires I <=Int N
  rule indexAfter(I, N) => I
       requires I >Int N

  rule loopCondition()
       => Compare(Name("i"), CmpOp("<=", Name("n")))

  rule loopBody()
       => Assign(
            Name("result"),
            BinOp(
              "+",
              BinOp("+", Name("result"), Str(" ")),
              Call(Name("str"), Name("i"))))
          Assign(Name("i"), BinOp("+", Name("i"), Int(1)))

  rule targetBody()
       => If(
            Compare(Name("n"), CmpOp("<", Int(0))),
            Return(Str("")),
            .Stmts)
          Assign(Name("result"), Str("X"))
          Assign(Name("i"), Int(1))
          While(loopCondition(), loopBody())
          Return(Name("result"))

  rule targetFunction() => function("n", targetBody())
  rule targetProgram()
       => Module(FuncDef("string_sequence", Params("n"), targetBody()))
endmodule
