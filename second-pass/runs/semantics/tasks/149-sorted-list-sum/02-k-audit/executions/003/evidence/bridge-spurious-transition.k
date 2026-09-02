requires "verification-no-bridge.k"

module BRIDGE-SPURIOUS-TRANSITION
  imports HUMANEVAL-VERIFICATION

  // This is the candidate bridge specialized to an observable continuation.
  // It claims that the loop can reach Name("word") while the local scope still
  // has no "word" binding.
  claim
    <k>
      #loop(
        list(strVals(INPUT:StrList)),
        Name("word"),
        filterBody)
      ~> Name("word")
    =>
      Name("word")
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
      1 |-> scope(
             "lst" |-> list(strVals(WHOLE:StrList))
             "even_words" |-> ref(0),
             parent(0))
    </scopes>
    <heap>
      0 |-> list(ACC:ValSeq)
    =>
      0 |-> list(evenAppend(ACC, INPUT))
    </heap>
endmodule
