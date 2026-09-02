requires "verification.k"

module BRIDGE-SPURIOUS-TRANSITION-EXTENDED
  imports HUMANEVAL-VERIFICATION

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
