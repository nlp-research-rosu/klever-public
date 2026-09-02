requires "reference-semantics/semantics.k"

module VERIFICATION-REAL-LIST
  imports MPY

  syntax Stmt ::= "filterByPrefixDef" [macro]
  rule filterByPrefixDef
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
         Return(Name("result")))

  syntax StrList ::= ".StrList" [constructor]
                   | sCons(IntSeq, StrList) [constructor]

  // Transparent constructor-level embedding into the fixed list representation.
  syntax ValSeq ::= strValues(StrList) [function, total]
  rule strValues(.StrList) => .ValSeq [simplification]
  rule strValues(sCons(S:IntSeq, REST:StrList))
    => vCons(str(S), strValues(REST))
    [simplification]

  syntax ValSeq ::= prefixFilter(IntSeq, StrList) [function, total]
  rule prefixFilter(_:IntSeq, .StrList) => .ValSeq [simplification]
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
