// spec.k — words_string proof on the UNIFIED semantics (src/).
// THREE-accumulator delimiter-split scan (result / current / has) over s + " " (the
// trailing space flushes the last word). Emits a list of word strings.

requires "verification.k"

module WORDS-STRING-SPEC
  imports WORDS-STRING-VERIFICATION

  // ---- Loop invariant (circularity) — from (result=list(RESULT), current=str(CUR),
  // has=HAS) the loop leaves result := list(wordsRes(CS,RESULT,CUR,HAS)),
  // current := str(wordsCur(CS,CUR,HAS)), has := wordsHas(CS,HAS). Induction on CS.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("ch"),
        If(Compare(Name("ch"), CmpOp("in", Str(", "))),
           If(Name("has"),
              Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Name("current"))))
              Assign(Name("current"), Str(""))
              Assign(Name("has"), Bool(false)),
              .Stmts),
           Assign(Name("current"), BinOp("+", Name("current"), Name("ch")))
           Assign(Name("has"), Bool(true))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "s" <- SV:Val ] [ "result" <- ref(HN1_0:Int) ] [ "current" <- str(CUR:IntSeq) ] [ "has" <- HAS:Bool ] [ "ch" <- _:Val ], P:Parent) =>
        scope(.Map [ "s" <- SV ] [ "result" <- ref(?HN1_0B:Int) ] [ "current" <- str(wordsCur(CS, CUR, HAS)) ] [ "has" <- wordsHas(CS, HAS) ] [ "ch" <- ?_:Val ], P)
      ) ...
    </scopes>
    <heap> (HN1_0 |-> list(RESULT:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(wordsRes(CS, RESULT, CUR, HAS))) ?_:Map </heap>
    <heapLoc> HLC1:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
    [all-path]

  // ---- Entry claim — result = words_string(str(CS)) == the list of words. The loop runs
  // over s + " " = seqConcat(CS, iCons(32,.)), from result=[], current="", has=false.
  claim
    <k>
      FuncDef("words_string", Params("s"),
        Assign(Name("result"), ListExpr(.Exprs))
        Assign(Name("current"), Str(""))
        Assign(Name("has"), Bool(false))
        Assign(Name("ch"), Str(""))
        For(Name("ch"), BinOp("+", Name("s"), Str(" ")),
          If(Compare(Name("ch"), CmpOp("in", Str(", "))),
             If(Name("has"),
                Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Name("current"))))
                Assign(Name("current"), Str(""))
                Assign(Name("has"), Bool(false)),
                .Stmts),
             Assign(Name("current"), BinOp("+", Name("current"), Name("ch")))
             Assign(Name("has"), Bool(true))))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("words_string"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "words_string" <- ?_:Val ]
                       [ "result" <- ref(?HN2_0:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?HN2_0 |-> list(wordsRes(seqConcat(CS, iCons(32, .IntSeq)), .ValSeq, .IntSeq, false))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
