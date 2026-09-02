requires "/tmp/audit-work/28-concatenate/verification.k"

module AUDIT-CONCATENATE-SPEC-EMPTY
  imports CONCATENATE-VERIFICATION

  claim [audit-empty]:
    <k>
      #loadAll(concatenateModule)
      ~> Call(Name("concatenate"), ListExpr(.Exprs))
      =>
      str(.IntSeq)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 => ?FINAL_SCOPE_LOC:Int </scopeLoc>
    <heap> .Map => ?FINAL_HEAP:Map </heap>
    <heapLoc> 0 => ?FINAL_HEAP_LOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
