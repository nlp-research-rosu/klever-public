requires "/tmp/audit-work/28-concatenate/verification.k"

module AUDIT-CONCATENATE-SPEC-VACUITY-FRESH
  imports CONCATENATE-VERIFICATION

  // Deliberately false: the satisfying input ["a", "b", "c"] returns "abc",
  // whose last code point is 99, not the mutated 100 ("abd").
  claim [false-abc-to-abd]:
    <k>
      #loadAll(concatenateModule)
      ~> Call(
           Name("concatenate"),
           ListExpr(Str("a"), Str("b"), Str("c"))
         )
      =>
      str(iCons(97, iCons(98, iCons(100, .IntSeq))))
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
