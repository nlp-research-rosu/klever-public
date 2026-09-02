requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-MUTATION
  imports MPY

  // Deliberate body mutation: return a newly allocated empty list instead of
  // the computed result reference.
  syntax Stmt ::= "filterByPrefixDefMutated" [macro]
  rule filterByPrefixDefMutated
    => FuncDef(
         "filter_by_prefix",
         Params("strings", "prefix"),
         Assign(Name("result"), ListExpr(.Exprs))
         Assign(Name("string"), Str(""))
         For(
           Name("string"),
           Name("strings"),
           If(
             Call(Attribute(Name("string"), "startswith"), Name("prefix")),
             Expr(Call(Attribute(Name("result"), "append"), Name("string"))),
             .Stmts))
         Return(ListExpr(.Exprs)))

  syntax StrList ::= ".StrList" [constructor]
                   | sCons(IntSeq, StrList) [constructor]
  syntax Iterable ::= stringList(StrList)
  rule <k> #iterNext(stringList(.StrList)) => #iterDone ... </k>
  rule <k> #iterNext(stringList(sCons(S:IntSeq, REST:StrList)))
        => #iterYield(str(S), stringList(REST)) ... </k>

  syntax ValSeq ::= prefixFilter(IntSeq, StrList) [function, total]
  rule prefixFilter(_:IntSeq, .StrList) => .ValSeq
    [simplification]
  rule prefixFilter(P:IntSeq, sCons(S:IntSeq, REST:StrList))
    => vCons(str(S), prefixFilter(P, REST))
    requires startsWith(P, S) ==Bool true
    [simplification]
  rule prefixFilter(P:IntSeq, sCons(S:IntSeq, REST:StrList))
    => prefixFilter(P, REST)
    requires startsWith(P, S) ==Bool false
    [simplification]

  rule valSeqConcat(VS:ValSeq, .ValSeq) => VS [simplification]
  rule valSeqConcat(valSeqConcat(A:ValSeq, B:ValSeq), C:ValSeq)
    => valSeqConcat(A, valSeqConcat(B, C))
    [simplification]

  syntax KItem ::= #checkFilter(ValSeq)
  rule <k> ref(H:Int) ~> #checkFilter(EXPECTED:ValSeq)
        => (ACTUAL ==K EXPECTED) ... </k>
       <heap> ... H |-> list(ACTUAL:ValSeq) ... </heap>
endmodule
