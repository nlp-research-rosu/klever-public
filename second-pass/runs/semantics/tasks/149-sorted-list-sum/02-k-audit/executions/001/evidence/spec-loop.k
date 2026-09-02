requires "verification.k"

module AUDIT-SPEC-LOOP
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
endmodule
