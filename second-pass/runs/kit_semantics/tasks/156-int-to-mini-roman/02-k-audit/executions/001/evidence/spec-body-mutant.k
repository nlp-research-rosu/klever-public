requires "verification-body-mutant.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION-BODY-MUTANT

  // The executed term returns "x" at 1000, so the original "m" result is false.
  claim [audit-body-sensitive-1000]:
    <k> #loadAll(solutionCallMutant(1000)) => .K </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "__result" |-> str(strToCodes("m"))
        "int_to_mini_roman" |->
          closureVal("number", .ParamNames, intToMiniRomanBodyMutant, 0),
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
