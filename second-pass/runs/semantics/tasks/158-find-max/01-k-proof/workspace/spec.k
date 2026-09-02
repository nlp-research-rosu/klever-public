requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [find-max-loop-invariant]:
    <k> #loop(list(wordVals(WORDS:WordSeq)),
              Name("word"),
              findMaxLoopBody)
         ~> KONT:K
      => KONT
    </k>
    <env> 1 </env>
    <scopes>
          1 |-> scope(
            ("words" |-> list(wordVals(ALL_WORDS:WordSeq)))
            ("best" |-> str(BEST:IntSeq))
            ("max_unique" |-> SCORE:Int)
            ("word" |-> str(PREVIOUS_WORD:IntSeq))
            ("unique" |-> PREVIOUS_SCORE:Int),
            parent(0))
          0 |-> scope(
            "find_max" |->
              closureVal(
                ("words", .ParamNames),
                findMaxFunctionBody,
                0),
            parent(-1))
         -1 |-> builtinsScope
      =>
          1 |-> scope(
            ("words" |-> list(wordVals(ALL_WORDS)))
            ("best" |-> str(bestWord(
              findMaxWords(WORDS, BEST, SCORE))))
            ("max_unique" |-> bestScore(
              findMaxWords(WORDS, BEST, SCORE)))
            ("word" |-> str(?FINAL_WORD:IntSeq))
            ("unique" |-> ?FINAL_SCORE:Int),
            parent(0))
          0 |-> scope(
            "find_max" |->
              closureVal(
                ("words", .ParamNames),
                findMaxFunctionBody,
                0),
            parent(-1))
         -1 |-> builtinsScope
    </scopes>

  claim [find-max-contract]:
    <k> #loadAll(Module(
         FuncDef("find_max", Params("words"), findMaxFunctionBody)))
         ~> Call(Name("find_max"), list(wordVals(WORDS:WordSeq)))
      => str(bestWord(findMaxWords(
           WORDS, .IntSeq, 0)))
    </k>
    <env> 0 </env>
    <scopes>
         0 |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope
      =>
         0 |-> scope(
                "find_max" |->
                  closureVal(
                    ("words", .ParamNames),
                    findMaxFunctionBody,
                    0),
                parent(-1))
        -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
