requires "verification.k"

module SELECT-WORDS-SPEC
  imports SELECT-WORDS-VERIFICATION

  // Inductive loop invariant. ACC is the already-produced prefix; processing
  // WS appends exactly the contract filter selectedWords(WS, N).
  claim [select-loop]:
    <k>
      #loop(wordIter(N:Int, WS:WordSeq), Name("word"), selectLoopBody)
      =>
      .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |->
        scope(
          ("s" |-> S:Val
           "n" |-> N:Int
           "result" |-> ref(H:Int)
           "word" |-> OLDWORD:Val
           "lower" |-> OLDLOWER:Val
           "consonants" |-> OLDCOUNT:Int)
          =>
          ("s" |-> S
           "n" |-> N
           "result" |-> ref(H)
           "word" |-> ?FINALWORD:Val
           "lower" |-> ?FINALLOWER:Val
           "consonants" |-> ?FINALCOUNT:Int),
          parent(0))
      0 |-> scope("select_words" |-> SELECTFN:Val, parent(-1))
      -1 |-> builtinsScope
      ...
    </scopes>
    <heap>
      ...
      H |-> list(ACC:ValSeq => valSeqConcat(ACC, selectedWords(WS, N)))
      ...
    </heap>
    [circularity]

  // The function enters its first iteration before the loop-carried locals
  // exist. One symbolic step establishes the recurrent invariant above.
  claim [select-loop-entry]:
    <k>
      #loop(wordIter(N:Int, WS:WordSeq), Name("word"), selectLoopBody)
      =>
      .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |->
        scope(
          ("s" |-> S:Val
           "n" |-> N
           "result" |-> ref(H:Int))
          =>
          ("s" |-> S
           "n" |-> N
           "result" |-> ref(H)
           ?FINAL:Map),
          parent(0))
      0 |-> scope("select_words" |-> SELECTFN:Val, parent(-1))
      -1 |-> builtinsScope
      ...
    </scopes>
    <heap>
      ...
      H |-> list(ACC:ValSeq => valSeqConcat(ACC, selectedWords(WS, N)))
      ...
    </heap>
    [depends(select-loop)]

  // End-to-end functional correctness for every natural n and every symbolic
  // whitespace-split word sequence.
  claim [select-words-correct]:
    <k>
      #loadAll(selectWordsModule)
      ~> Call(Name("select_words"),
              str(inputWords(N:Int, WS:WordSeq)), N)
      ~> #expectList(selectedWords(WS, N))
      =>
      .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(
               "select_words" |->
                 closureVal(("s", "n", .ParamNames),
                            selectFunctionBody,
                            0),
               parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(selectedWords(WS, N))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
    [depends(select-loop-entry)]
endmodule
