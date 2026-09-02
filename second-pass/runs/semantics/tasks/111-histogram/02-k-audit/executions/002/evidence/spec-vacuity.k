requires "verification.k"

module HISTOGRAM-SPEC-VACUITY
  imports VERIFICATION

  // Fresh false result obligation: histogram("") is {}, never {"a": 1}.
  claim [false-empty-result]:
    <k>
      #loadAll(histogramCheck(
        Str(""),
        DictExpr(Entry(Str("a"), Int(1)))))
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
