requires "verification.k"

module SPEC
  imports VERIFICATION

  // For every string in the supplied code-sequence model, flip_case returns
  // exactly the semantics' pointwise case swap.
  claim
    <k> #runFlipCase(S:IntSeq) => str(mapSwap(S)) </k>
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
