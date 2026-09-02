requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The exact translated function definition from solution.mpy.
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

  // A typed, list-isomorphic proof value.  Its iterator emits exactly the
  // same string values, in the same order, as a Python list of strings.
  syntax StrList ::= ".StrList" [constructor]
                   | sCons(IntSeq, StrList) [constructor]
  syntax Iterable ::= stringList(StrList)
  rule <k> #iterNext(stringList(.StrList)) => #iterDone ... </k>
  rule <k> #iterNext(stringList(sCons(S:IntSeq, REST:StrList)))
        => #iterYield(str(S), stringList(REST)) ... </k>

  // Mathematical result: retain exactly the strings satisfying startsWith.
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

  // Derived list lemma needed when ACC is symbolic (right identity).
  rule valSeqConcat(VS:ValSeq, .ValSeq) => VS [simplification]
  // Derived associativity lemma normalizes accumulator appends to the right.
  rule valSeqConcat(valSeqConcat(A:ValSeq, B:ValSeq), C:ValSeq)
    => valSeqConcat(A, valSeqConcat(B, C))
    [simplification]

  // Observe a returned heap list structurally, hiding its allocation address.
  syntax KItem ::= #checkFilter(ValSeq)
  rule <k> ref(H:Int) ~> #checkFilter(EXPECTED:ValSeq)
        => (ACTUAL ==K EXPECTED) ... </k>
       <heap> ... H |-> list(ACTUAL:ValSeq) ... </heap>
endmodule
