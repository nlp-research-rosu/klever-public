requires "verification.k"

module SPEC-FALSE
  imports VERIFICATION

  // Fresh audit mutation: input 4 returns "iv", not "v".
  claim [audit-wrong-result-4]:
    <k> #loadAll(solutionCall(4)) => .K </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "__result" |-> str(strToCodes("v"))
        "int_to_mini_roman" |->
          closureVal("number", .ParamNames, intToMiniRomanBody, 0),
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
