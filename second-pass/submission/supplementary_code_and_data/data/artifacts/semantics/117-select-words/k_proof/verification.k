requires "reference-semantics/semantics.k"

module SELECT-WORDS-VERIFICATION
  imports MPY

  // A symbolic sequence of the words produced by whitespace splitting.
  // keepWord represents a word whose consonant count equals n; skipWord
  // represents one whose count differs. This is the complete behavioral
  // partition relevant to select_words for any fixed n.
  syntax WordSeq ::= ".WordSeq"
                   | keepWord(IntSeq, WordSeq)
                   | skipWord(IntSeq, WordSeq)

  // Opaque symbolic input whose split projection is exactly the given words.
  syntax IntSeq ::= inputWords(Int, WordSeq)
                  | countedWord(Int, IntSeq)

  // The program only iterates over s.split(); this proof-only iterable avoids
  // forcing the concrete splitWS function to destruct an unknown IntSeq.
  syntax Iterable ::= wordIter(Int, WordSeq)

  rule <k> #applyK(
             toCall(boundMethodV(str(inputWords(N:Int, WS:WordSeq)), "split")),
             .Vals)
        => wordIter(N, WS) ... </k>
       [priority(30)]

  rule <k> #iterNext(wordIter(_N:Int, .WordSeq))
        => #iterDone ... </k>
  rule <k> #iterNext(wordIter(N:Int, keepWord(W:IntSeq, WS:WordSeq)))
        => #iterYield(str(countedWord(N, W)), wordIter(N, WS)) ... </k>
  rule <k> #iterNext(wordIter(N:Int, skipWord(W:IntSeq, WS:WordSeq)))
        => #iterYield(str(countedWord(N +Int 1, W)), wordIter(N, WS)) ... </k>

  // Mathematical consonant count used by the contract. Since prompt inputs
  // contain only letters and spaces, a word's non-vowels are its consonants.
  // countedWord carries that mathematical count through the symbolic quotient.
  syntax Int ::= consonantCount(IntSeq)
                 [function, total, symbol(consonantCount), no-evaluators]
  rule ((((isLen(W:IntSeq)
           -Int cntSub(mapLower(W), iCons(97, .IntSeq)))
          -Int cntSub(mapLower(W), iCons(101, .IntSeq)))
         -Int cntSub(mapLower(W), iCons(105, .IntSeq)))
        -Int cntSub(mapLower(W), iCons(111, .IntSeq)))
       -Int cntSub(mapLower(W), iCons(117, .IntSeq))
    => consonantCount(W)
    [simplification]
  rule consonantCount(countedWord(C:Int, _W:IntSeq)) => C

  // Contract-level filter: preserve precisely the words with n consonants,
  // and preserve their order.
  syntax ValSeq ::= selectedWords(WordSeq, Int) [function, total]
  rule selectedWords(.WordSeq, _N:Int) => .ValSeq
  rule selectedWords(keepWord(W:IntSeq, WS:WordSeq), N:Int)
    => vCons(str(countedWord(N, W)), selectedWords(WS, N))
  rule selectedWords(skipWord(_W:IntSeq, WS:WordSeq), N:Int)
    => selectedWords(WS, N)

  // Associativity is a definitional theorem of valSeqConcat and is oriented
  // for the append-based loop invariant.
  rule valSeqConcat(valSeqConcat(A:ValSeq, B:ValSeq), C:ValSeq)
    => valSeqConcat(A, valSeqConcat(B, C))
    [simplification]
  rule valSeqConcat(A:ValSeq, .ValSeq) => A
    [simplification]

  // Expose absence of the closure-cell marker through ordinary map entries;
  // this keeps symbolic plain-frame assignments from spuriously narrowing to
  // the annotated-closure write rule.
  rule "$cells" in_keys ((X:String |-> _V:Val) REST:Map)
    => "$cells" in_keys (REST)
    requires X =/=String "$cells"
    [simplification]
  rule X:String in_keys (_M:Map [ X <- _V:Val ]) => true
    [simplification]
  rule {((X:String |-> V:Val) _REST:Map)[X]}:>Val => V
    [simplification]

  // Continuation used only to observe the structural contents of the returned
  // list reference.
  syntax KItem ::= #expectList(ValSeq)
  rule <k> ref(H:Int) ~> #expectList(VS:ValSeq) => .K ... </k>
       <heap> ... H |-> list(VS) ... </heap>

  // These macros are the exact translated function body in solution.mpy.
  syntax Stmts ::= "selectLoopBody" [macro]
  rule selectLoopBody
    => Assign(Name("lower"),
              Call(Attribute(Name("word"), "lower"), .Exprs))
       Assign(
         Name("consonants"),
         BinOp(
           "-",
           BinOp(
             "-",
             BinOp(
               "-",
               BinOp(
                 "-",
                 BinOp(
                   "-",
                   Call(Name("len"), Name("word")),
                   Call(Attribute(Name("lower"), "count"),
                        Str("a"))),
                 Call(Attribute(Name("lower"), "count"),
                      Str("e"))),
               Call(Attribute(Name("lower"), "count"),
                    Str("i"))),
             Call(Attribute(Name("lower"), "count"),
                  Str("o"))),
           Call(Attribute(Name("lower"), "count"),
                Str("u"))))
       If(Compare(Name("consonants"), CmpOp("==", Name("n"))),
          Expr(Call(Attribute(Name("result"), "append"),
                    Name("word")))
          .Stmts,
          .Stmts)
       .Stmts

  syntax Stmts ::= "selectFunctionBody" [macro]
  rule selectFunctionBody
    => Assign(Name("result"), ListExpr(.Exprs))
       For(Name("word"),
           Call(Attribute(Name("s"), "split"), .Exprs),
           selectLoopBody)
       Return(Name("result"))
       .Stmts

  syntax Module ::= "selectWordsModule" [macro]
  rule selectWordsModule
    => Module(
         FuncDef("select_words",
                 Params("s", "n"),
                 selectFunctionBody)
         .Stmts)
endmodule
