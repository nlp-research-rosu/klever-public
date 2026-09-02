requires "verification.k"

module GET-ROW-SPEC-VACUITY
  imports GET-ROW-VERIFICATION

  // Fresh reviewer mutation: the empty input is falsely required to return
  // a result list containing coordinate (0, 0).
  claim
    <k>
      Call(Name("get_row"), list(.ValSeq), X:Int, .Exprs)
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("get_row" |-> getRowClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
             vCons(
               tuple(vCons(0, vCons(0, .ValSeq))),
               .ValSeq))
      1 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
