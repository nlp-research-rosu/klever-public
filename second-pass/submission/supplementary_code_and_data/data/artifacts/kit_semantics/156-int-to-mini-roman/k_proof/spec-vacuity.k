requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the correct result for 19 is "xix", not "xviii".
  claim [wrong-result-19]:
    <k> #loadAll(solutionCall(19)) => .K </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "__result" |-> str(strToCodes("xviii"))
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
