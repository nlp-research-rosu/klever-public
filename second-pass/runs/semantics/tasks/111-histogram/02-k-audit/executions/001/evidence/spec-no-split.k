requires "verification-no-split.k"

module HISTOGRAM-NO-SPLIT-SPEC
  imports VERIFICATION-NO-SPLIT

  claim
    <k>
      #loadAll(histogramCheck(
        str(tokenText(vCons(str(A:IntSeq), .ValSeq))),
        DictExpr(Entry(str(A), Int(1)))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
