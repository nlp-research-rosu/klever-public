requires "verification.k"

module HUMANEVAL-SPEC-LABELED
  imports HUMANEVAL-VERIFICATION

  claim
    <k>
      #loop(
        list(strVals(INPUT:StrList)),
        Name("word"),
        filterBody)
      ~> CONT:K
    =>
      CONT
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
                     "lst" |-> list(strVals(_WHOLE:StrList))
                     "even_words" |-> ref(H:Int),
                     parent(0))
    </scopes>
    <heap>
      ... H |-> list(ACC:ValSeq)
    =>
          H |-> list(evenAppend(ACC, INPUT)) ...
    </heap>
    [label(loop-contract)]

  claim
    <k>
      FuncDef("sorted_list_sum", Params("lst"), solutionBody)
      ~> Call(Name("sorted_list_sum"), list(strVals(INPUT:StrList)))
    =>
      ref(2)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0  |-> scope(solutionGlobals, parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
    =>
      .Map
        [ 0 <- list(evenAppend(.ValSeq, INPUT)) ]
        [ 1 <- list(sortVS(evenAppend(.ValSeq, INPUT))) ]
        [ 2 <- list(
                 sortKeyVS(
                   sortVS(evenAppend(.ValSeq, INPUT)),
                   builtinV("len"))) ]
    </heap>
    <heapLoc> 0 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(entry-point)]
endmodule
