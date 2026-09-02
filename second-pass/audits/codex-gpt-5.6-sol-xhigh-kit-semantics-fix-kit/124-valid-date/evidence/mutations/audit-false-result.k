requires "verification.k"

module AUDIT-FALSE-RESULT
  imports VERIFICATION

  // Fresh audit mutation: 12-31-9999 satisfies the length-ten entry domain,
  // and the real function returns true. Requiring false must be rejected.
  claim [false-last-branch-result]:
    <k>
      #loadAll(validDateProgram)
      ~> Call(Name("valid_date"), (Str("12-31-9999"), .Exprs))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope((.Map => "valid_date" |-> validDateClosure), parent(-1))
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
