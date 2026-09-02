requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the real submitted program returns {"a": 1} here.
  claim
    <k>
      #loadAll(histogramCheck(
        Str("a"),
        DictExpr(Entry(Str("a"), Int(2)))))
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
