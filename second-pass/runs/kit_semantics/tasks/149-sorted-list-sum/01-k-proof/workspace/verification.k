requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY

  syntax Bool ::= stringsOnly(ValSeq) [function, total]
  syntax ValSeq ::= scanEven(ValSeq, ValSeq) [function, total]

  // Exact constructor-level abbreviations for solution.mpy.
  syntax Stmts ::= "sortedListSumBody" [macro]
  syntax Module ::= "sortedListSumModule" [macro]
endmodule

module VERIFICATION
  imports VERIFICATION-SYNTAX
  imports MPY

  rule stringsOnly(.ValSeq) => true
  rule stringsOnly(vCons(V:Val, REST:ValSeq))
    => isStrV(V) andBool stringsOnly(REST)

  // scanEven(ACC, INPUT) is the stable odd-length filter appended to ACC.
  rule scanEven(ACC:ValSeq, .ValSeq) => ACC
  rule scanEven(ACC:ValSeq, vCons(V:Val, REST:ValSeq))
    => scanEven(
         valSeqConcat(ACC, vCons(V, .ValSeq)),
         REST)
    requires isStrV(V)
     andBool pyMod(seqLen(V), 2) ==Int 0
    [simplification]
  rule scanEven(ACC:ValSeq, vCons(V:Val, REST:ValSeq))
    => scanEven(ACC, REST)
    requires isStrV(V)
     andBool pyMod(seqLen(V), 2) =/=Int 0
    [simplification]
  rule scanEven(ACC:ValSeq, vCons(V:Val, REST:ValSeq))
    => scanEven(ACC, REST)
    requires notBool isStrV(V)

  // Definedness consequences of the string-list precondition.
  rule #Ceil(seqLen(V:Val)) => #Top
    requires isStrV(V)
    [simplification]

  rule sortedListSumBody
    => Assign(Name("result"), ListExpr(.Exprs))
       Assign(Name("word"), Str(""))
       For(
         Name("word"),
         Name("lst"),
         If(
           Compare(
             BinOp("%", Call(Name("len"), Name("word")), Int(2)),
             CmpOp("==", Int(0))),
           Expr(
             Call(
               Attribute(Name("result"), "append"),
               Name("word"))),
           .Stmts))
       Return(
         Call(
           Name("sorted"),
           Call(Name("sorted"), Name("result")),
           KwArg("key", Name("len"))))

  rule sortedListSumModule
    => Module(
         FuncDef(
           "sorted_list_sum",
           Params("lst"),
           sortedListSumBody))
endmodule
