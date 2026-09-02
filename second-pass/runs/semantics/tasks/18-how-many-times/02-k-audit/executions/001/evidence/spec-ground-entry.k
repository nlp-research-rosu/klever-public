requires "/tmp/audit-work/fresh/verification.k"

module HOW-MANY-TIMES-GROUND-ENTRY-AUDIT
  imports HOW-MANY-TIMES-VERIFICATION

  // Fully ground satisfying entry state: string "aaaa", substring "aa".
  claim
    <k>
      #applyK(
        toCall(
          closureVal(
            ("string", "substring"),
            howManyTimesBody,
            0)),
        (str(iCons(97, iCons(97, iCons(97, iCons(97, .IntSeq))))),
         str(iCons(97, iCons(97, .IntSeq))),
         .Vals))
    =>
      3
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "how_many_times"
               |-> closureVal(
                     ("string", "substring"),
                     howManyTimesBody,
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
