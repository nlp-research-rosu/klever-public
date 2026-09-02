requires "reference-semantics/semantics.k"

module ODD-COUNT-VERIFICATION
  imports MPY

  // The mathematical number of odd decimal digits in a code sequence.
  syntax Int ::= oddDigits(IntSeq) [function, total]
               | oddDigitsFrom(Int, IntSeq) [function, total]
  rule oddDigits(CS:IntSeq) => oddDigitsFrom(0, CS)
  rule oddDigitsFrom(N:Int, .IntSeq) => N
  rule oddDigitsFrom(N:Int, iCons(C:Int, CS:IntSeq))
    => oddDigitsFrom(N +Int pyMod(C -Int 48, 2), CS)

  // The value left in the loop target after iterating over a string.
  syntax Val ::= lastDigit(IntSeq, Val) [function, total]
  rule lastDigit(.IntSeq, OLD:Val) => OLD
  rule lastDigit(iCons(C:Int, CS:IntSeq), _:Val)
    => lastDigit(CS, str(iCons(C, .IntSeq)))

  // The required output sentence, expressed using exactly the string
  // operations available to the program.
  // Decimal rendering is total for every integer. The reference's
  // strToCodes(Int2String(_)) implementation computes it concretely but is
  // intentionally partial-looking to the symbolic backend, so name that
  // mathematically total result explicitly.
  syntax IntSeq ::= decimalCodes(Int)
    [function, total, symbol(decimalCodes), no-evaluators]
  rule strToCodes(Int2String(N:Int)) => decimalCodes(N) [simplification]

  syntax Val ::= oddText(Int) [function, total]
  rule oddText(N:Int)
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
                       str(decimalCodes(N))),
                     str(strToCodes("n the str"))),
                   str(decimalCodes(N))),
                 str(strToCodes("ng "))),
               str(decimalCodes(N))),
             str(strToCodes(" of the "))),
           str(decimalCodes(N))),
         str(strToCodes("nput.")))

  syntax ValSeq ::= oddCountSpec(ValSeq) [function, total]
                    | oddCountFrom(ValSeq, ValSeq) [function, total]
  rule oddCountSpec(INPUT:ValSeq) => oddCountFrom(.ValSeq, INPUT)
  rule oddCountFrom(ACC:ValSeq, .ValSeq) => ACC
  rule oddCountFrom(
         ACC:ValSeq,
         vCons(V:Val, REST:ValSeq))
    => oddCountFrom(
         valSeqConcat(
           ACC,
           vCons(oddText(oddDigits(codesProj(V))), .ValSeq)),
         REST)

  // Values of the ordinary Python locals after the outer loop. These are
  // useful only for stating a strong loop invariant; the returned result does
  // not depend on them.
  syntax Val ::= outerDigits(ValSeq, Val) [function, total]
               | outerDigit(ValSeq, Val) [function, total]
               | outerText(ValSeq, Val) [function, total]
  syntax Int ::= outerCount(ValSeq, Int) [function, total]
  rule outerDigits(.ValSeq, OLD:Val) => OLD
  rule outerDigits(vCons(str(CS:IntSeq), REST:ValSeq), _:Val)
    => outerDigits(REST, str(CS))
  rule outerCount(.ValSeq, OLD:Int) => OLD
  rule outerCount(vCons(str(CS:IntSeq), REST:ValSeq), _:Int)
    => outerCount(REST, oddDigits(CS))
  rule outerDigit(.ValSeq, OLD:Val) => OLD
  rule outerDigit(vCons(str(CS:IntSeq), REST:ValSeq), _:Val)
    => outerDigit(REST, lastDigit(CS, str(.IntSeq)))
  rule outerText(.ValSeq, OLD:Val) => OLD
  rule outerText(vCons(str(CS:IntSeq), REST:ValSeq), _:Val)
    => outerText(REST, oddText(oddDigits(CS)))

  syntax Bool ::= validDigitStrings(ValSeq) [function, total]
                  | validDigitString(Val) [function, total]
  syntax IntSeq ::= codesProj(Val) [function, total]
  rule codesProj(str(CS:IntSeq)) => CS
  rule validDigitStrings(.ValSeq) => true
  rule validDigitStrings(vCons(V:Val, REST:ValSeq))
    => validDigitString(V) andBool validDigitStrings(REST)
  rule validDigitString(V:Val)
    => V ==K str(codesProj(V)) andBool allDigit(codesProj(V))

  // A proof-only representation of lists of strings. Every concrete
  // list-of-strings value has exactly this shape; exposing the constructor
  // lets symbolic execution induct on the outer list without narrowing an
  // otherwise arbitrary Val head.
  syntax DigitStrings ::= "noStrings"
                        | moreStrings(IntSeq, DigitStrings)
  syntax ValSeq ::= asValues(DigitStrings) [function]
  rule asValues(noStrings) => .ValSeq
  rule asValues(moreStrings(CS:IntSeq, REST:DigitStrings))
    => vCons(str(CS), asValues(REST))

  syntax Bool ::= validDigitInput(DigitStrings) [function]
  rule validDigitInput(noStrings) => true
  rule validDigitInput(moreStrings(CS:IntSeq, REST:DigitStrings))
    => allDigit(CS) andBool validDigitInput(REST)

  // Program fragments below are a direct K rendering of solution.mpy. Keeping
  // them named makes the loop invariants in spec.k readable.
  syntax Stmts ::= "ODD-INNER-BODY" [macro]
  rule ODD-INNER-BODY
    => AugAssign(
         Name("count"),
         "+",
         BinOp("%", Call(Name("int"), Name("digit")), Int(2)))
       .Stmts

  // A modular use of the digit-loop theorem proved in spec.k. The abstract
  // outer-list head is related to its string projection by validDigitString;
  // this rule applies that already-proved loop transformer at the For site.
  // The standalone digit-loop claim starts at #loop and therefore proves the
  // transformer from the reference iterator rules, without using this rule.
  rule <k>
         For(
           Name("digit"),
           V:Val,
           AugAssign(
             Name("count"),
             "+",
             BinOp("%", Call(Name("int"), Name("digit")), Int(2)))
           .Stmts)
         => .K
         ...
       </k>
       <env> 1 </env>
       <scopes>
         ...
         1  |-> scope(
                 ("lst" |-> list(INPUT:ValSeq))
                 ("result" |-> ref(OUT:Int))
                 ("digits" |-> CURRENT:Val)
                 ("count" |-> N:Int)
                 ("digit" |-> D:Val)
                 ("text" |-> TXT:Val),
                 parent(0))
         =>
         1  |-> scope(
                 ("lst" |-> list(INPUT))
                 ("result" |-> ref(OUT))
                 ("digits" |-> CURRENT)
                 ("count" |-> oddDigitsFrom(N, codesProj(V)))
                 ("digit" |-> lastDigit(codesProj(V), D))
                 ("text" |-> TXT),
                 parent(0))
         ...
       </scopes>
       requires validDigitString(V)
       [priority(40)]

  syntax Stmts ::= "ODD-OUTER-BODY" [macro]
  rule ODD-OUTER-BODY
    => Assign(Name("count"), Int(0))
       Assign(Name("digit"), Str(""))
       For(Name("digit"), Name("digits"), ODD-INNER-BODY)
       Assign(
         Name("text"),
         BinOp(
           "+",
           Str("the number of odd elements "),
           Call(Name("str"), Name("count"))))
       Assign(
         Name("text"),
         BinOp(
           "+",
           BinOp(
             "+",
             BinOp(
               "+",
               BinOp("+", Name("text"), Str("n the str")),
               Call(Name("str"), Name("count"))),
             Str("ng ")),
           Call(Name("str"), Name("count"))))
       Assign(
         Name("text"),
         BinOp(
           "+",
           BinOp(
             "+",
             BinOp("+", Name("text"), Str(" of the ")),
             Call(Name("str"), Name("count"))),
           Str("nput.")))
       Expr(Call(Attribute(Name("result"), "append"), Name("text")))
       Assign(Name("digits"), Str(""))
       Assign(Name("count"), Int(0))
       Assign(Name("digit"), Str(""))
       Assign(Name("text"), Str(""))
       .Stmts

  syntax Stmts ::= "ODD-COUNT-BODY" [macro]
  rule ODD-COUNT-BODY
    => Assign(Name("result"), ListExpr(.Exprs))
       Assign(Name("digits"), Str(""))
       Assign(Name("count"), Int(0))
       Assign(Name("digit"), Str(""))
       Assign(Name("text"), Str(""))
       For(Name("digits"), Name("lst"), ODD-OUTER-BODY)
       Return(Name("result"))
       .Stmts

  syntax Module ::= "ODD-COUNT-PROGRAM" [macro]
  rule ODD-COUNT-PROGRAM
    => Module(
         FuncDef(
           "odd_count",
           Params("lst"),
           ODD-COUNT-BODY))
endmodule
