requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: exchange([2], [1]) returns "YES", not "NO".
  claim [false-result]:
    <k>
      #loadAll(exchangeProgram)
      ~> Call(
           Name("exchange"),
           list(vCons(2, .ValSeq)),
           list(vCons(1, .ValSeq)))
      => str(strToCodes("NO"))
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
