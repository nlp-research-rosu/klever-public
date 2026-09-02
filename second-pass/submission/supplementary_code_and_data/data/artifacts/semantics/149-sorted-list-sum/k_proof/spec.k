requires "verification.k"

module HUMANEVAL-SPEC
  imports HUMANEVAL-VERIFICATION

  // Universal loop-contract claim over arbitrary-length list[str] inputs.
  // This checks that the proof-only summary is wired to the exact translated
  // loop state and exposes precisely the contract-level accumulator result.
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

  // End-to-end entry-point theorem.  INPUT ranges over lists of arbitrary
  // length whose strings have arbitrary code sequences.  sortVS and sortKeyVS
  // are the supplied semantics' trusted lexical and stable keyed-sort symbols.
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
endmodule
