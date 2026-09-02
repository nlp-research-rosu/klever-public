// spec.k — words_in_sentence, TRAP-FREE (P143). Inner sticky-flag invariant
// pair, THREE outer element-loop variants (binding sets are non-monotone:
// len<=2 words skip the inner loop entirely), tail posts (only new_lst is
// read after), entry over the real single FuncDef.
//
//   kompile verification.k --backend haskell --main-module WORDS-IN-SENTENCE-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module WORDS-IN-SENTENCE-SPEC

requires "verification.k"

module WORDS-IN-SENTENCE-SPEC
  imports WORDS-IN-SENTENCE-VERIFICATION

  claim
    <k>
      #loop(rangeObj(I:Int, IHI:Int, 1), Name("i"),
        If(Compare(BinOp("%", Call(Name("len"), Name("word")), Name("i")), CmpOp("==", Int(0))),
          Assign(Name("flg"), Int(1)),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "words_in_sentence" <- WSV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "sentence" <- SV:Val ] [ "new_lst" <- NLV:Val ] [ "word" <- WV:Val ]
                         [ "flg" <- F:Int ], parent(0))
           => scope(.Map [ "sentence" <- SV ] [ "new_lst" <- NLV ] [ "word" <- WV ]
                         [ "flg" <- divFlg(isLen(codesProj(WV)), I, IHI, F) ] [ "i" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 2 andBool IHI ==Int isLen(codesProj(WV)) andBool isStr(WV)
     andBool I <Int IHI
    [all-path]

  claim
    <k>
      #loop(rangeObj(I:Int, IHI:Int, 1), Name("i"),
        If(Compare(BinOp("%", Call(Name("len"), Name("word")), Name("i")), CmpOp("==", Int(0))),
          Assign(Name("flg"), Int(1)),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "words_in_sentence" <- WSV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "sentence" <- SV:Val ] [ "new_lst" <- NLV:Val ] [ "word" <- WV:Val ]
                         [ "flg" <- F:Int ] [ "i" <- _:Val ], parent(0))
           => scope(.Map [ "sentence" <- SV ] [ "new_lst" <- NLV ] [ "word" <- WV ]
                         [ "flg" <- divFlg(isLen(codesProj(WV)), I, IHI, F) ] [ "i" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 2 andBool IHI ==Int isLen(codesProj(WV)) andBool isStr(WV)
    [all-path]

  claim
    <k>
      #loop(list(VS:ValSeq), Name("word"),
        Assign(Name("flg"), Int(0))
        If(Compare(Call(Name("len"), Name("word")), CmpOp("==", Int(1))),
          Assign(Name("flg"), Int(1)),
          .Stmts)
        For(Name("i"), Call(Name("range"), Int(2), Call(Name("len"), Name("word"))),
          If(Compare(BinOp("%", Call(Name("len"), Name("word")), Name("i")), CmpOp("==", Int(0))),
            Assign(Name("flg"), Int(1)),
            .Stmts))
        If(BoolOp("or",
            Compare(Name("flg"), CmpOp("==", Int(0))),
            Compare(Call(Name("len"), Name("word")), CmpOp("==", Int(2)))),
          Expr(Call(Attribute(Name("new_lst"), "append"), Name("word"))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "words_in_sentence" <- WSV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "sentence" <- SV:Val ] [ "new_lst" <- ref(LR:Int) ], parent(0))
           => scope((.Map [ "sentence" <- SV ] [ "new_lst" <- ref(LR) ]) ?_:Map, parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (LR |-> list(ACC:ValSeq)) HREST:Map
        => (LR |-> list(wordFilt(VS, ACC))) HREST </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(VS)
    [all-path]

  claim
    <k>
      #loop(list(VS:ValSeq), Name("word"),
        Assign(Name("flg"), Int(0))
        If(Compare(Call(Name("len"), Name("word")), CmpOp("==", Int(1))),
          Assign(Name("flg"), Int(1)),
          .Stmts)
        For(Name("i"), Call(Name("range"), Int(2), Call(Name("len"), Name("word"))),
          If(Compare(BinOp("%", Call(Name("len"), Name("word")), Name("i")), CmpOp("==", Int(0))),
            Assign(Name("flg"), Int(1)),
            .Stmts))
        If(BoolOp("or",
            Compare(Name("flg"), CmpOp("==", Int(0))),
            Compare(Call(Name("len"), Name("word")), CmpOp("==", Int(2)))),
          Expr(Call(Attribute(Name("new_lst"), "append"), Name("word"))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "words_in_sentence" <- WSV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "sentence" <- SV:Val ] [ "new_lst" <- ref(LR:Int) ] [ "word" <- _:Val ] [ "flg" <- _:Val ], parent(0))
           => scope((.Map [ "sentence" <- SV ] [ "new_lst" <- ref(LR) ]) ?_:Map, parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (LR |-> list(ACC:ValSeq)) HREST:Map
        => (LR |-> list(wordFilt(VS, ACC))) HREST </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(VS)
    [all-path]

  claim
    <k>
      #loop(list(VS:ValSeq), Name("word"),
        Assign(Name("flg"), Int(0))
        If(Compare(Call(Name("len"), Name("word")), CmpOp("==", Int(1))),
          Assign(Name("flg"), Int(1)),
          .Stmts)
        For(Name("i"), Call(Name("range"), Int(2), Call(Name("len"), Name("word"))),
          If(Compare(BinOp("%", Call(Name("len"), Name("word")), Name("i")), CmpOp("==", Int(0))),
            Assign(Name("flg"), Int(1)),
            .Stmts))
        If(BoolOp("or",
            Compare(Name("flg"), CmpOp("==", Int(0))),
            Compare(Call(Name("len"), Name("word")), CmpOp("==", Int(2)))),
          Expr(Call(Attribute(Name("new_lst"), "append"), Name("word"))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "words_in_sentence" <- WSV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "sentence" <- SV:Val ] [ "new_lst" <- ref(LR:Int) ] [ "word" <- _:Val ] [ "flg" <- _:Val ] [ "i" <- _:Val ], parent(0))
           => scope((.Map [ "sentence" <- SV ] [ "new_lst" <- ref(LR) ]) ?_:Map, parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (LR |-> list(ACC:ValSeq)) HREST:Map
        => (LR |-> list(wordFilt(VS, ACC))) HREST </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(VS)
    [all-path]

  claim
    <k>
      FuncDef("words_in_sentence", Params("sentence"),
        Assign(Name("new_lst"), ListExpr(.Exprs))
        For(Name("word"), Call(Attribute(Name("sentence"), "split"), .Exprs),
          Assign(Name("flg"), Int(0))
        If(Compare(Call(Name("len"), Name("word")), CmpOp("==", Int(1))),
          Assign(Name("flg"), Int(1)),
          .Stmts)
        For(Name("i"), Call(Name("range"), Int(2), Call(Name("len"), Name("word"))),
          If(Compare(BinOp("%", Call(Name("len"), Name("word")), Name("i")), CmpOp("==", Int(0))),
            Assign(Name("flg"), Int(1)),
            .Stmts))
        If(BoolOp("or",
            Compare(Name("flg"), CmpOp("==", Int(0))),
            Compare(Call(Name("len"), Name("word")), CmpOp("==", Int(2)))),
          Expr(Call(Attribute(Name("new_lst"), "append"), Name("word"))),
          .Stmts))
        Return(Call(Attribute(Str(" "), "join"), Name("new_lst"))))
      Assign(Name("result"), Call(Name("words_in_sentence"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "words_in_sentence" <- ?_:Val ] [ "result" <- wisRes(CS) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
