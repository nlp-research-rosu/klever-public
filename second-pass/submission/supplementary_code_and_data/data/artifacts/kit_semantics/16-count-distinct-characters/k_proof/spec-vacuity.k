requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim [false-off-by-one-postcondition]:
    <k>
      Call(Name("count_distinct_characters"), str(CS:IntSeq))
      =>
      isLen(dedupCodes(mapLower(CS))) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "count_distinct_characters" |->
          closureVal(
            ("string", .ParamNames),
            Return(
              Call(
                Name("len"),
                Call(
                  Name("set"),
                  Call(Attribute(Name("string"), "lower"), .Exprs)
                )
              )
            ) .Stmts,
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
