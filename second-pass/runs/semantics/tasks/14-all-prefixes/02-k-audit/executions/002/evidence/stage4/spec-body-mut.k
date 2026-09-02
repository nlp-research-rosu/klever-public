requires "verification-body-mut.k"

module SPEC-BODY-MUT
  imports VERIFICATION-BODY-MUT

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

  claim
    <k>
      #loadAll(solutionModule())
      ~> Call(Name("all_prefixes"), (str(S:IntSeq), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      => 0 |-> scope(
           "all_prefixes" |-> closureVal(
             "string", .ParamNames, allPrefixesBody(), 0),
           parent(-1))
         -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map => 0 |-> list(allPrefixes(S))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
