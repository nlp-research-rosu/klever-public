requires "verification.k"

module AUDIT-BODY-MUTATION
  imports VERIFICATION

  claim [mutated-return-zero-must-not-prove]:
    <k>
      Call(Name("count_distinct_characters"), str(CS:IntSeq))
      =>
      isLen(dedupCodes(mapLower(CS)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "count_distinct_characters" |->
          closureVal(
            ("string", .ParamNames),
            Return(Int(0)) .Stmts,
            0
          ),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
