requires "verification.k"

module ODD-COUNT-GROUND-INTENDED
  imports ODD-COUNT-VERIFICATION

  // The intended result for the satisfying source-domain input ["3"].
  claim [ground-intended]:
    <k>
      #loadAll(ODD-COUNT-PROGRAM)
      ~> Call(
           Name("odd_count"),
           list(
             vCons(
               str(iCons(51, .IntSeq)),
               .ValSeq)))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(.Map, parent(-1))
      =>
      -1 |-> builtinsScope
      0  |-> scope(
              "odd_count" |-> closureVal("lst", ODD-COUNT-BODY, 0),
              parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
              vCons(
                str(strToCodes(
                  "the number of odd elements 1n the str1ng 1 of the 1nput.")),
                .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
