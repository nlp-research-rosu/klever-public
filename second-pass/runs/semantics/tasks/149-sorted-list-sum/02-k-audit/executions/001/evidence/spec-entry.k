requires "verification.k"

module AUDIT-SPEC-ENTRY
  imports HUMANEVAL-VERIFICATION

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
