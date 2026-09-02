requires "reference-semantics/semantics.k"

module HUMANEVAL-VERIFICATION
  imports MPY

  syntax StrList ::= ".StrList"
                   | sCons(IntSeq, StrList)

  syntax ValSeq ::= strVals(StrList)
  rule strVals(.StrList) => .ValSeq
  rule strVals(sCons(CS:IntSeq, REST:StrList))
    => vCons(str(CS), strVals(REST))

  syntax ValSeq ::= evenAppend(ValSeq, StrList) [function, total]
  rule evenAppend(ACC:ValSeq, .StrList) => ACC
  rule evenAppend(ACC:ValSeq, sCons(CS:IntSeq, REST:StrList))
    => evenAppend(
         valSeqConcat(ACC, vCons(str(CS), .ValSeq)),
         REST)
    requires pyMod(isLen(CS), 2) ==Int 0
  rule evenAppend(ACC:ValSeq, sCons(CS:IntSeq, REST:StrList))
    => evenAppend(ACC, REST)
    requires pyMod(isLen(CS), 2) =/=Int 0

  syntax Stmts ::= "filterBody" [macro]
  rule filterBody
    => If(
         Compare(
           BinOp("%", Call(Name("len"), Name("word")), Int(2)),
           CmpOp("==", Int(0))),
         Expr(
           Call(
             Attribute(Name("even_words"), "append"),
             Name("word"))),
         .Stmts)

  syntax Stmts ::= "solutionBody" [macro]
  rule solutionBody
    => Assign(Name("even_words"), ListExpr(.Exprs))
       For(Name("word"), Name("lst"), filterBody)
       Return(
         Call(
           Name("sorted"),
           Call(Name("sorted"), Name("even_words")),
           KwArg("key", Name("len"))))

  syntax Val ::= solutionClosure(Int) [function, total]
  rule solutionClosure(L:Int)
    => closureVal(("lst", .ParamNames), solutionBody, L)

  syntax Map ::= "solutionGlobals" [function, total]
  rule solutionGlobals
    => .Map [ "sorted_list_sum" <- solutionClosure(0) ]
endmodule
