requires "verification.k"

module AUDIT-FALSE-MUTATION
  imports VERIFICATION

  // Fresh false result obligation. The satisfying input is exactly two spaces.
  // Real execution returns "__"; this mutation demands only "_".
  claim [wrong-two-space-result]:
    <k>
      Call(
        Name("fix_spaces"),
        str(iCons(32, iCons(32, .IntSeq))))
      =>
      str(iCons(95, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "fix_spaces" |->
          closureVal(("text", .ParamNames), #fixSpacesBody, 0),
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
