requires "verification-body-mutated.k"

module AUDIT-SHAPE-BODY-MUTATED-SPEC
  imports GET-ROW-VERIFICATION-MUTATED

  claim [shape-ascending-body-wrong-post]:
    <k>
      Call(
        Name("get_row"),
        list(vCons(ref(0), vCons(ref(1), vCons(ref(2), .ValSeq)))),
        X:Int,
        .Exprs)
      =>
      ref(3)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("get_row" |-> getRowClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      0 |-> list(.ValSeq)
      1 |-> list(vCons(A:Int, .ValSeq))
      2 |-> list(vCons(B:Int, vCons(C:Int, vCons(D:Int, .ValSeq))))
      =>
      0 |-> list(.ValSeq)
      1 |-> list(vCons(A, .ValSeq))
      2 |-> list(vCons(B, vCons(C, vCons(D, .ValSeq))))
      3 |-> list(
             addMatch(
               A, X, 1, 0,
               addMatch(
                 D, X, 2, 2,
                 addMatch(
                   C, X, 2, 1,
                   addMatch(B, X, 2, 0, .ValSeq)))))
      4 |-> list(
             vCons(
               tuple(vCons(0, vCons(ref(0), .ValSeq))),
               vCons(
                 tuple(vCons(1, vCons(ref(1), .ValSeq))),
                 vCons(
                   tuple(vCons(2, vCons(ref(2), .ValSeq))),
                   .ValSeq))))
    </heap>
    <heapLoc> 3 => 5 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
