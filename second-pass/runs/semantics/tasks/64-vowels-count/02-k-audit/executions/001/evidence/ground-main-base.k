requires "verification.k"

module GROUND-MAIN-BASE
  imports VOWELS-BASE

  // Satisfying entry state with S = "a".  This deliberately excludes the
  // candidate loop bridge and executes the one-iteration body concretely.
  claim [ground-a-without-bridge]:
    <k>
      #loadAll(vowelsModule)
      ~> Call(
        Name("vowels_count"),
        str(iCons(97, .IntSeq))
      )
      =>
      1
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
