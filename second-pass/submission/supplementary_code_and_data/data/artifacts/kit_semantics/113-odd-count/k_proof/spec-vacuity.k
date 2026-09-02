requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim [false-result]:
    <k>
      Call(Name("odd_count"), list(.ValSeq))
      =>
      ref(1)
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
      0 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
