// spec.k — select_words proof on the UNIFIED semantics (src/).
// Split on spaces + per-word consonant count filter, in ONE scan (four accumulators:
// result / current / cnt / has) over s + " ", keeping words with exactly n consonants.

requires "verification.k"

module SELECT-WORDS-SPEC
  imports SELECT-WORDS-VERIFICATION

  // ---- Loop invariant (circularity) — from (result=list(RESULT), current=str(CUR),
  // cnt=CNT, has=HAS) the loop leaves result := list(selRes(CS,RESULT,CUR,CNT,HAS,N)),
  // current := str(selCur(...)), cnt := selCnt(...), has := selHas(...). Induction on CS.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("ch"),
        If(Compare(Name("ch"), CmpOp("==", Str(" "))),
           If(Name("has"),
              If(Compare(Name("cnt"), CmpOp("==", Name("n"))),
                 Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Name("current")))),
                 .Stmts)
              Assign(Name("current"), Str(""))
              Assign(Name("cnt"), Int(0))
              Assign(Name("has"), Bool(false)),
              .Stmts),
           Assign(Name("current"), BinOp("+", Name("current"), Name("ch")))
           If(Compare(Name("ch"), CmpOp("not in", Str("aeiouAEIOU"))),
              Assign(Name("cnt"), BinOp("+", Name("cnt"), Int(1))),
              .Stmts)
           Assign(Name("has"), Bool(true))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "s" <- SV:Val ] [ "n" <- N:Int ] [ "result" <- ref(HN1_0:Int) ] [ "current" <- str(CUR:IntSeq) ] [ "cnt" <- CNT:Int ] [ "has" <- HAS:Bool ] [ "ch" <- _:Val ], P:Parent) =>
        scope(.Map [ "s" <- SV ] [ "n" <- N ] [ "result" <- ref(?HN1_0B:Int) ] [ "current" <- str(selCur(CS, CUR, CNT, HAS, N)) ] [ "cnt" <- selCnt(CS, CUR, CNT, HAS, N) ] [ "has" <- selHas(CS, CUR, CNT, HAS, N) ] [ "ch" <- ?_:Val ], P)
      ) ...
    </scopes>
    <heap> (HN1_0 |-> list(RESULT:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(selRes(CS, RESULT, CUR, CNT, HAS, N))) ?_:Map </heap>
    <heapLoc> HLC1:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
    [all-path]

  // ---- Entry claim — result = select_words(str(CS), N) == the words with N consonants.
  // The loop runs over s + " " = seqConcat(CS, iCons(32,.)), from result=[], current="",
  // cnt=0, has=false.
  claim
    <k>
      FuncDef("select_words", Params("s", "n"),
        Assign(Name("result"), ListExpr(.Exprs))
        Assign(Name("current"), Str(""))
        Assign(Name("cnt"), Int(0))
        Assign(Name("has"), Bool(false))
        Assign(Name("ch"), Str(""))
        For(Name("ch"), BinOp("+", Name("s"), Str(" ")),
          If(Compare(Name("ch"), CmpOp("==", Str(" "))),
             If(Name("has"),
                If(Compare(Name("cnt"), CmpOp("==", Name("n"))),
                   Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Name("current")))),
                   .Stmts)
                Assign(Name("current"), Str(""))
                Assign(Name("cnt"), Int(0))
                Assign(Name("has"), Bool(false)),
                .Stmts),
             Assign(Name("current"), BinOp("+", Name("current"), Name("ch")))
             If(Compare(Name("ch"), CmpOp("not in", Str("aeiouAEIOU"))),
                Assign(Name("cnt"), BinOp("+", Name("cnt"), Int(1))),
                .Stmts)
             Assign(Name("has"), Bool(true))))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("select_words"), (str(CS:IntSeq), Int(N:Int))))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "select_words" <- ?_:Val ]
                       [ "result" <- ref(?HN2_0:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?HN2_0 |-> list(selRes(seqConcat(CS, iCons(32, .IntSeq)), .ValSeq, .IntSeq, 0, false, N))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
