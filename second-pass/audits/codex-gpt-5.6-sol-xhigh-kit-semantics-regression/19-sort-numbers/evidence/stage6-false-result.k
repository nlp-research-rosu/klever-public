requires "/tmp/audit-work/19-sort-numbers/source/verification.k"

module AUDIT-FALSE-RESULT
  imports VERIFICATION

  // Fresh auditor mutation: the real function always returns a string on the
  // formal domain, so replacing the entry claim's exact string result by noneV
  // is false. VS=.ValSeq is a concrete satisfying witness; Python returns "".
  claim [returns-none]:
    <k> Call(Name("sort_numbers"),
             (str(joinCodes(iCons(32, .IntSeq), VS:ValSeq)), .Exprs))
      => noneV </k>
    <env> 0 </env>
    <scopes> 0  |-> scope("sort_numbers" |-> sortNumbersFunction, parent(-1))
             -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(VS)
                    1 |-> list(sortKeyVS(VS, numberKeyFunction)) </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires validNumberWords(VS)
endmodule
