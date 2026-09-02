requires "verification.k"

module SPEC-GROUND-WITNESS
  imports VERIFICATION

  claim [aa-witness]:
    <k>
      #loadAll(#solutionModule)
      ~> Call(
           Name("words_in_sentence"),
           str(iCons(97, iCons(97, .IntSeq))))
      =>
      str(iCons(97, iCons(97, .IntSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
             "words_in_sentence"
               |-> closureVal("sentence", #wordsBody, 0),
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
