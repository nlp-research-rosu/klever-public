requires "verification.k"

module GROUND-SPEC
  imports VERIFICATION

  // [1], [2] satisfies the entry precondition and is exactly on the YES boundary.
  claim [ground-threshold]:
    <k>
      #loadAll(exchangeProgram)
      ~> Call(
           Name("exchange"),
           list(vCons(1, .ValSeq)),
           list(vCons(2, .ValSeq)))
      => str(strToCodes("YES"))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
