requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // False witness: the precondition is realized by the concrete state below,
  // but starts_one_ends(1) returns 1, not 2.
  claim [false-result-at-one]:
    <k> #invokeStartsOneEnds(1) => 2 </k>
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
