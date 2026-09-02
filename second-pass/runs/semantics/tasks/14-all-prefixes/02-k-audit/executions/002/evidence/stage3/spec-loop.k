requires "verification.k"

module SPEC-LOOP
  imports VERIFICATION

  claim
    <k>
      #loop(
        rangeObj(END:Int, STOP:Int, 1),
        Name("end"),
        allPrefixesLoopBody()) ~> CONT:K
      => CONT
    </k>
    <env> L:Int </env>
    <scopes>
      SC:Map
      L |-> scope(
        "end" |-> _PREV:Int
        "prefixes" |-> ref(H:Int)
        "string" |-> str(S:IntSeq),
        P:Parent)
      => SC
         L |-> scope(
           "end" |-> ?FINAL:Int
           "prefixes" |-> ref(H)
           "string" |-> str(S),
           P)
    </scopes>
    <heap>
      HP:Map H |-> list(ACC:ValSeq)
      => HP H |-> list(prefixesAcc(S, END, STOP, ACC))
    </heap>
    requires END <=Int STOP
endmodule
