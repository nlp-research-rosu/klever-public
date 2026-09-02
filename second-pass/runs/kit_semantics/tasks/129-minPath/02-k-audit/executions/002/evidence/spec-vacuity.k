requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: this satisfying input returns [1,2,1], not [1,3,1].
  claim [ground-n2-k3-false-result]:
    <k>
      Call(Name("minPath"),
           (list(gridRows(iCons(1, iCons(2, iCons(3, iCons(4, .IntSeq)))), 2)),
            3, .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        ("$perm" |-> str(iCons(1, iCons(2, iCons(3, iCons(4, .IntSeq))))))
        ("minPath" |-> closureVal(("grid", "k", .ParamNames),
                                   minPathBody, 0)),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map => 0 |-> list(vCons(1, vCons(3, vCons(1, .ValSeq))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

endmodule
