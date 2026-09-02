requires "semantic.k"

// Program text and a mathematical oracle used only by the proof.
// The three statement macros are a readable factorization of solution.mpy.

module ODD-COUNT-VERIFICATION
  imports MPY-SEMANTICS

  syntax Stmts ::= "innerBody" [macro]
                 | "outerBody" [macro]
                 | "functionBody" [macro]
  syntax Module ::= "solutionProgram" [macro]

  rule innerBody
    => If(Compare(Name("c"), CmpOp("in", Str("13579"))),
          Assign(Name("count"), BinOp("+", Name("count"), Int(1))),
          .Stmts)

  rule outerBody
    => Assign(Name("count"), Int(0))
       For(Name("c"), Name("s"), innerBody)
       Assign(
         Name("result"),
         BinOp(
           "+", Name("result"),
           ListExpr(
             BinOp(
               "+",
               BinOp(
                 "+",
                 BinOp(
                   "+",
                   BinOp(
                     "+",
                     BinOp(
                       "+",
                       BinOp(
                         "+",
                         BinOp(
                           "+",
                           BinOp(
                             "+",
                             Str("the number of odd elements "),
                             Call(Name("str"), Name("count"))),
                           Str("n the str")),
                         Call(Name("str"), Name("count"))),
                       Str("ng ")),
                     Call(Name("str"), Name("count"))),
                   Str(" of the ")),
                 Call(Name("str"), Name("count"))),
               Str("nput.")))))

  rule functionBody
    => Assign(Name("result"), ListExpr())
       For(Name("s"), Name("lst"), outerBody)
       Return(Name("result"))

  rule solutionProgram
    => Module(FuncDef("odd_count", Params("lst"), functionBody))

  syntax Int ::= oddCount ( Digits ) [function]
  rule oddCount(noDigits) => 0
  rule oddCount(digit(evenDigit, DS)) => oddCount(DS)
  rule oddCount(digit(oddDigit, DS)) => 1 +Int oddCount(DS)

  syntax Text ::= message ( Int ) [function]
  rule message(N)
    => concat(
         concat(
           concat(
             concat(
               concat(
                 concat(
                   concat(
                     concat(literal("the number of odd elements "), number(N)),
                     literal("n the str")),
                   number(N)),
                 literal("ng ")),
               number(N)),
             literal(" of the ")),
           number(N)),
         literal("nput."))

  syntax Values ::= expected ( Values ) [function]
  rule expected(noValues) => noValues
  rule expected(value(pyString(inputDigits(DS)), REST))
    => value(pyString(message(oddCount(DS))), expected(REST))

  syntax Value ::= runProgram ( Module , Value ) [function]
  rule runProgram(Module(FuncDef("odd_count", Params("lst"), BODY)), IN)
    => resultValue(execute(BODY, store("lst", IN, emptyEnv)))
endmodule
