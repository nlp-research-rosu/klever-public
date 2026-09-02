requires "verification.k"

module SPEC-UNICODE-WITNESS
  imports VERIFICATION

  // The supplied ASCII-only swapC leaves U+00E9 (é) unchanged.
  claim
    <k> #runFlipCase(iCons(233, .IntSeq))
      => str(iCons(233, .IntSeq)) </k>
    <env> 0 </env>
    <scopes>
        0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope
      =>
        0  |-> scope(
                 "flip_case" |->
                   closureVal(
                     ("string", .ParamNames),
                     flipCaseBody,
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
