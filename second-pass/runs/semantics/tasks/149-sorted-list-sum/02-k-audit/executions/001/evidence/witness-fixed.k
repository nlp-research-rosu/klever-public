requires "reference-semantics/semantics.k"

module AUDIT-WITNESS-FIXED
  imports MPY

  syntax StrList ::= ".StrList"
                   | sCons(IntSeq, StrList)

  syntax ValSeq ::= strVals(StrList)
  rule strVals(.StrList) => .ValSeq
  rule strVals(sCons(CS:IntSeq, REST:StrList))
    => vCons(str(CS), strVals(REST))

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
endmodule
