requires "/tmp/audit-work/28-concatenate/verification.k"

module AUDIT-CONCATENATE-SPEC-ABC
  imports CONCATENATE-VERIFICATION

  claim [audit-abc]:
    <k>
      #loadAll(concatenateModule)
      ~> Call(
           Name("concatenate"),
           ListExpr(Str("a"), Str("b"), Str("c"))
         )
      =>
      str(iCons(97, iCons(98, iCons(99, .IntSeq))))
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
