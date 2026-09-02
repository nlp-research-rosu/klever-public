requires "verification.k"

module CONCATENATE-SPEC-LABELED
  imports CONCATENATE-VERIFICATION

  claim [loop]:
    <k>
      #loop(
        list(VS:ValSeq),
        Name("string"),
        concatenateLoopBody
      )
      ~> CONT:K
      =>
      CONT
    </k>
    <env> L:Int </env>
    <scopes>
      SC:Map
      L |-> scope(
        ("result" |-> str(A:IntSeq)
         "string" |-> OLD_STRING:Val
         "strings" |-> ARGUMENT:Val)
        =>
        ("result" |-> str(concatenateValues(A, VS))
         "string" |-> finalLoopValue(OLD_STRING, VS)
         "strings" |-> ARGUMENT),
        parent(0)
      )
    </scopes>
    requires allStringValues(VS)

  claim [empty]:
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

  claim [abc]:
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
