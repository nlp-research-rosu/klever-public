requires "verification.k"

module SPEC-AUDIT-VACUITY
  imports VERIFICATION

  // Deliberately false at the satisfiable witness n = 2:
  // the program returns 18, while this destination requires 19.
  claim
    <k>
      #invokeStartsOneEnds(2)
      => 19
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "starts_one_ends" |->
          closureVal(("n", .ParamNames), startsOneEndsBody, 0),
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
