requires "verification-opposite.k"

module ODD-COUNT-OPPOSITE-SPEC
  imports ODD-COUNT-OPPOSITE-VERIFICATION

  // False for real Python and for the supplied fixed semantics: ["3"] has
  // one odd digit, so the interpolated digit must be 1, not 9.
  claim [opposite-result]:
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
                  "the number of odd elements 9n the str9ng 9 of the 9nput.")),
                .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
