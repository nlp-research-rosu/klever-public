requires "verification.k"

module SPEC-BODY-SENSITIVITY
  imports VERIFICATION

  // The original theorem's n=2 instance. It must fail after the proof-side
  // body is deliberately changed from coefficient 18 to coefficient 19.
  claim
    <k> #invokeStartsOneEnds(2) => 18 </k>
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
