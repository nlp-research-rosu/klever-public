requires "verification.k"

module MISSING-UNIVERSAL-ENTRY
  imports CONCATENATE-VERIFICATION

  // Exact copy of the candidate's auxiliary loop claim, included so the
  // added entry claim can use it as a circularity.
  claim [loop]:
    <k>
      #loop(list(VS:ValSeq), Name("string"), concatenateLoopBody)
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

  // This full-domain entry theorem is deliberately absent from candidate
  // spec.k. It is an audit experiment, not part of the immutable candidate.
  claim [universal-entry]:
    <k>
      #loadAll(concatenateModule)
      ~> Call(Name("concatenate"), (list(VS:ValSeq), .Exprs))
      =>
      str(concatenateValues(.IntSeq, VS))
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
    requires allStringValues(VS)
endmodule
