requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false off-by-one result mutation.
  claim [is-bored-off-by-one]:
    <k>
      Call(Name("is_bored"), (str(IS:IntSeq), .Exprs))
      => boredoms(IS) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "is_bored" |-> closureVal(
          ("S", .ParamNames),
          BORED-FUNCTION-BODY,
          0),
        parent(-1))
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
