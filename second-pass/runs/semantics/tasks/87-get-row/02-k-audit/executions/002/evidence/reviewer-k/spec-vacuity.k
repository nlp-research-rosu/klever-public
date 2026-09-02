requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports GET-ROW-VERIFICATION

  // Fresh false mutation: on the satisfiable empty-list precondition, require
  // the returned result object to contain the fabricated coordinate (0, 0).
  // Python evaluation for the witness lst=[], x=7 returns [].
  claim [empty-fabricated-coordinate]:
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
