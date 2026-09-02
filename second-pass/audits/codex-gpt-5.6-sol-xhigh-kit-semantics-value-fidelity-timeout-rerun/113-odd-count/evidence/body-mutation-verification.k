requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY

  // Compile-time abbreviations for the exact Stmts subtrees in solution.mpy.
  syntax Stmts ::= "oddBody" [macro]
                 | "oddLoopBody" [macro]

  rule oddBody =>
    Assign(Name("result"), ListExpr(.Exprs))
    Return(Name("result"))
    .Stmts

  rule oddLoopBody =>
    Assign(
      Name("count"),
      BinOp(
        "+",
        BinOp(
          "+",
          BinOp(
            "+",
            BinOp(
              "+",
              Call(Attribute(Name("s"), "count"), (Str("1"), .Exprs)),
              Call(Attribute(Name("s"), "count"), (Str("3"), .Exprs))),
            Call(Attribute(Name("s"), "count"), (Str("5"), .Exprs))),
          Call(Attribute(Name("s"), "count"), (Str("7"), .Exprs))),
        Call(Attribute(Name("s"), "count"), (Str("9"), .Exprs))))
    Expr(
      Call(
        Attribute(Name("result"), "append"),
        (BinOp(
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
                        Call(Name("str"), (Name("count"), .Exprs))),
                      Str("n the str")),
                    Call(Name("str"), (Name("count"), .Exprs))),
                  Str("ng ")),
                Call(Name("str"), (Name("count"), .Exprs))),
              Str(" of the ")),
            Call(Name("str"), (Name("count"), .Exprs))),
          Str("nput.")), .Exprs)))
    .Stmts
endmodule

module VERIFICATION-BASE
  imports VERIFICATION-SYNTAX
  imports MPY
  imports INT
  imports BOOL

  // Definitional postcondition summaries. None of these rules rewrites a
  // program computation or intercepts a call.
  syntax Bool ::= allStringValues(ValSeq) [function, total]
  rule allStringValues(.ValSeq) => true
  rule allStringValues(vCons(V:Val, REST:ValSeq))
    => isStrV(V) andBool allStringValues(REST)

  syntax IntSeq ::= codesProj(Val)
                    [function, total, symbol(codesProj), no-evaluators]
  rule codesProj(str(CS:IntSeq)) => CS

  // Trusted value for the fixed, pure str.count(one-character) primitive.
  // The theorem is conditional on digitOccurrences(CS,D) denoting the number
  // of occurrences of code D in CS.
  syntax Int ::= digitOccurrences(IntSeq, Int)
                 [function, total, symbol(digitOccurrences), no-evaluators]
  rule digitOccurrences(CS:IntSeq, D:Int)
    => cntSub(CS, iCons(D, .IntSeq))
    [concrete]

  // Trusted-primitive bridge for fixed pure str.count. Callee and argument
  // evaluation have already completed at applyMethod; no state or control
  // cell is changed.
  rule applyMethod(
         V:Val,
         "count",
         str(iCons(D:Int, .IntSeq)),
         .Vals)
    => digitOccurrences(codesProj(V), D)
    requires isStrV(V)
    [priority(40)]

  syntax Int ::= oddDigits(IntSeq) [function, total]
  rule oddDigits(CS:IntSeq)
    => digitOccurrences(CS, 49)
       +Int digitOccurrences(CS, 51)
       +Int digitOccurrences(CS, 53)
       +Int digitOccurrences(CS, 55)
       +Int digitOccurrences(CS, 57)

  // Trusted value for fixed pure str(int). The theorem is conditional on
  // intStringCodes(N) denoting Python's decimal rendering of N.
  syntax IntSeq ::= intStringCodes(Int)
                    [function, total, symbol(intStringCodes), no-evaluators]
  rule intStringCodes(N:Int) => strToCodes(Int2String(N)) [concrete]
  rule applyBuiltin("str", N:Int, .Vals) => str(intStringCodes(N))
    [priority(40)]

  syntax IntSeq ::= oddSentenceCodes(Int) [function, total]
  rule oddSentenceCodes(N:Int)
    => seqConcat(
         seqConcat(
           seqConcat(
             seqConcat(
               seqConcat(
                 seqConcat(
                   seqConcat(
                     seqConcat(
                       strToCodes("the number of odd elements "),
                       intStringCodes(N)),
                     strToCodes("n the str")),
                   intStringCodes(N)),
                 strToCodes("ng ")),
               intStringCodes(N)),
             strToCodes(" of the ")),
           intStringCodes(N)),
         strToCodes("nput."))

  syntax Val ::= oddSentence(Int) [function, total]
  rule oddSentence(N:Int) => str(oddSentenceCodes(N))

  // Tail-recursive description of appending one rendered result per input.
  // Its step is deliberately aligned with list.append's fixed semantics.
  syntax ValSeq ::= oddRun(ValSeq, ValSeq) [function]
  rule oddRun(ACC:ValSeq, .ValSeq) => ACC
  rule oddRun(ACC:ValSeq, vCons(V:Val, REST:ValSeq))
    => oddRun(
         valSeqConcat(
           ACC,
           vCons(oddSentence(oddDigits(codesProj(V))), .ValSeq)),
         REST)
    requires isStrV(V)

  syntax ValSeq ::= "emptyOutput" [function, total]
  rule emptyOutput => .ValSeq
endmodule

module VERIFICATION
  imports VERIFICATION-BASE
endmodule

module VERIFICATION-KRUN
  imports VERIFICATION
  imports MPY-CONCRETE
endmodule
