requires "verification-body-mutation.k"

module SPEC-GROUND-BODY-MUTATION
  imports VERIFICATION-BODY-MUTATION

  claim [ground-n2-k3]:
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
      .Map => 0 |-> list(vCons(1, vCons(2, vCons(1, .ValSeq))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

endmodule
