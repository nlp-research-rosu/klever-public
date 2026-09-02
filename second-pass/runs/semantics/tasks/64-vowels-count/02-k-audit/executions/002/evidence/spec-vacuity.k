requires "verification.k"

module SPEC-VACUITY
  imports VOWELS-VERIFICATION

  claim [false-off-by-one-result]:
    <k>
      #loadAll(vowelsModule)
      ~> Call(Name("vowels_count"), str(S:IntSeq))
      =>
      specifiedVowels(S) +Int 1
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
