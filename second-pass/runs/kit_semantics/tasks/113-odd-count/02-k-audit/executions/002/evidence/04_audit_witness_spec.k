requires "verification.k"

module AUDIT-WITNESS-SPEC
  imports VERIFICATION

  claim [digit-precondition-witness]:
    <k>
      allDigitStrings(
        vCons(str(iCons(49, .IntSeq)), .ValSeq))
      =>
      true
    </k>

  claim [ground-entry-one]:
    <k>
      Call(
        Name("odd_count"),
        list(vCons(str(iCons(49, .IntSeq)), .ValSeq)))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "odd_count" |-> closureVal("lst", ODD-COUNT-BODY, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
        vCons(
          oddLine(iCons(49, .IntSeq)),
          .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
