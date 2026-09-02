requires "reference-semantics/semantics.k"

// Reviewer control definition: exact program macros plus only the structural
// input representation/iterator exposure. It deliberately omits decimalCodes,
// hasOnlyOddDigits, selectOddAcc, and the loop theorem/rule, so the submitted
// condition executes under the supplied fixed semantics.
module AUDIT-NO-CONDITION-BRIDGE
  imports MPY

  syntax Stmts ::= "uniqueDigitsLoopBody" [macro]
  rule uniqueDigitsLoopBody
    => Assign(Name("digits"), Call(Name("str"), Name("number")))
       If(BoolOp("and",
            Compare(Str("0"), CmpOp("not in", Name("digits"))),
            Compare(Str("2"), CmpOp("not in", Name("digits"))),
            Compare(Str("4"), CmpOp("not in", Name("digits"))),
            Compare(Str("6"), CmpOp("not in", Name("digits"))),
            Compare(Str("8"), CmpOp("not in", Name("digits")))),
          Expr(Call(Attribute(Name("result"), "append"), Name("number"))),
          .Stmts)

  syntax Stmts ::= "uniqueDigitsBody" [macro]
  syntax Stmts ::= "uniqueDigitsReturn" [macro]
  rule uniqueDigitsReturn
    => Return(Call(Name("sorted"), Name("result"))) .Stmts
  rule uniqueDigitsBody
    => Expr(Str("Return the sorted elements of x whose decimal digits are all odd."))
       Assign(Name("result"), ListExpr(.Exprs))
       For(Name("number"), Name("x"), uniqueDigitsLoopBody)
       uniqueDigitsReturn

  syntax Val ::= "uniqueDigitsClosure" [macro]
  rule uniqueDigitsClosure
    => closureVal(("x", .ParamNames), uniqueDigitsBody, 0)
  syntax Module ::= "uniqueDigitsModule" [macro]
  rule uniqueDigitsModule
    => Module(FuncDef("unique_digits", Params("x"), uniqueDigitsBody))

  syntax ValSeq ::= intsToVals(IntSeq)
  rule intsToVals(.IntSeq) => .ValSeq
  rule intsToVals(iCons(I:Int, R:IntSeq)) => vCons(I, intsToVals(R))
  rule <k> #iterNext(list(intsToVals(.IntSeq))) => #iterDone ... </k>
  rule <k> #iterNext(list(intsToVals(iCons(I:Int, R:IntSeq))))
        => #iterYield(I, list(intsToVals(R))) ... </k>
endmodule
