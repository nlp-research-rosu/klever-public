requires "verification.k"

module BODY-SENSITIVITY-SPEC
  imports VERIFICATION

  // Fresh auditor mutation: the executed closure body is replaced by
  // `return True`, but the short-list witness is required to return false.
  claim [mutated-body-short-list]:
    <k>
      Call(Name("triples_sum_to_zero"), (ref(0), .Exprs))
      => false
    </k>
    <env> 0 </env>
    <scopes>
        0 |-> scope(
          "triples_sum_to_zero"
            |-> closureVal(
                  ("l", .ParamNames),
                  Return(Bool(true)) .Stmts,
                  0),
          parent(-1))
       -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      -1 |-> intSeqGhost(iCons(1, iCons(2, .IntSeq)))
       0 |-> list(intVals(iCons(1, iCons(2, .IntSeq))))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
