requires "verification.k"

module UNICODE-ZERO-SPEC
  imports VOWELS-VERIFICATION

  claim [unicode-i-dot-k-result-zero]:
    <k>
      #loadAll(vowelsModule)
      ~> Call(
           Name("vowels_count"),
           str(iCons(304, .IntSeq))
         )
      =>
      0
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
        "vowels_count" |-> closureVal("s", vowelsBody, 0),
        parent(-1)
      )
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
