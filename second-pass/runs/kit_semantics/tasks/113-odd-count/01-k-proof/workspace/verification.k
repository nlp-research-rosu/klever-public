requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY

  syntax Stmts ::= "ODD-COUNT-BODY" [macro]
                 | "ODD-COUNT-LOOP-BODY" [macro]

  syntax Bool ::= isStringVal(Val) [function, total]
                | allDigitStrings(ValSeq) [function, total]

  syntax IntSeq ::= stringCodes(Val)
    [function, total, symbol(stringCodes), no-evaluators]
  syntax Int ::= oddDigitCount(IntSeq) [function, total]
  syntax Val ::= oddLine(IntSeq) [function, total]
  syntax ValSeq ::= oddLinesAcc(ValSeq, ValSeq) [function, total]
endmodule

module VERIFICATION
  imports VERIFICATION-SYNTAX
  imports MPY

  rule ODD-COUNT-BODY
    => Assign(Name("result"), ListExpr(.Exprs))
       Assign(Name("s"), Str(""))
       Assign(Name("count"), Int(0))
       Assign(Name("count_string"), Str(""))
       For(Name("s"), Name("lst"), ODD-COUNT-LOOP-BODY)
       Return(Name("result"))
       .Stmts

  rule ODD-COUNT-LOOP-BODY
    => Assign(
         Name("count"),
         BinOp(
           "+",
           BinOp(
             "+",
             BinOp(
               "+",
               BinOp(
                 "+",
                 Call(Attribute(Name("s"), "count"), Str("1")),
                 Call(Attribute(Name("s"), "count"), Str("3"))),
               Call(Attribute(Name("s"), "count"), Str("5"))),
             Call(Attribute(Name("s"), "count"), Str("7"))),
           Call(Attribute(Name("s"), "count"), Str("9"))))
       Assign(Name("count_string"), Call(Name("str"), Name("count")))
       Expr(
         Call(
           Attribute(Name("result"), "append"),
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
                           Name("count_string")),
                         Str("n the str")),
                       Name("count_string")),
                     Str("ng ")),
                   Name("count_string")),
                 Str(" of the ")),
               Name("count_string")),
             Str("nput."))))
       .Stmts

  rule isStringVal(str(_:IntSeq)) => true
  rule isStringVal(_:Val) => false [owise]

  rule stringCodes(str(CS:IntSeq)) => CS [simplification]

  rule allDigitStrings(.ValSeq) => true
  rule allDigitStrings(vCons(V:Val, REST:ValSeq))
    => isStringVal(V)
       andBool allDigit(stringCodes(V))
       andBool allDigitStrings(REST)

  rule applyMethod(V:Val, "count", str(PATTERN:IntSeq), .Vals)
    => cntSub(stringCodes(V), PATTERN)
    requires isStringVal(V)
    [simplification]

  rule oddDigitCount(CS:IntSeq)
    => cntSub(CS, iCons(49, .IntSeq))
       +Int cntSub(CS, iCons(51, .IntSeq))
       +Int cntSub(CS, iCons(53, .IntSeq))
       +Int cntSub(CS, iCons(55, .IntSeq))
       +Int cntSub(CS, iCons(57, .IntSeq))

  rule oddLine(CS:IntSeq)
    => applyBin(
         "+",
         applyBin(
           "+",
           applyBin(
             "+",
             applyBin(
               "+",
               applyBin(
                 "+",
                 applyBin(
                   "+",
                   applyBin(
                     "+",
                     applyBin(
                       "+",
                       str(strToCodes("the number of odd elements ")),
                       str(strToCodes(Int2String(oddDigitCount(CS))))),
                     str(strToCodes("n the str"))),
                   str(strToCodes(Int2String(oddDigitCount(CS))))),
                 str(strToCodes("ng "))),
               str(strToCodes(Int2String(oddDigitCount(CS))))),
             str(strToCodes(" of the "))),
           str(strToCodes(Int2String(oddDigitCount(CS))))),
         str(strToCodes("nput.")))

  rule oddLinesAcc(ACC:ValSeq, .ValSeq) => ACC
  rule oddLinesAcc(ACC:ValSeq, vCons(V:Val, REST:ValSeq))
    => oddLinesAcc(
         valSeqConcat(ACC, vCons(oddLine(stringCodes(V)), .ValSeq)),
         REST)
endmodule
