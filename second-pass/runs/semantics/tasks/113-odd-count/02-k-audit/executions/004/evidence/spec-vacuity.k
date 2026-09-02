requires "verification.k"

module ODD-COUNT-SPEC-VACUITY
  imports ODD-COUNT-VERIFICATION

  // Fresh false mutation: the satisfying input ["3"] must produce a
  // one-element result, so requiring the returned list to be empty is false.
  claim [false-empty-result]:
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
      0 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
