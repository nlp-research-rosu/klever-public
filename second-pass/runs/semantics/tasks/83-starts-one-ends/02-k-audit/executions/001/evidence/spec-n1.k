requires "verification.k"

module SPEC-N1
  imports VERIFICATION

  claim
    <k> #invokeStartsOneEnds(1) => 1 </k>
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
