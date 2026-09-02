requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Operational-sensitivity probe: replacing the real body by "return False"
  // must invalidate the true result for [0, 0, 0].
  claim [mutated-body]:
    <k>
      Call(
        Name("triples_sum_to_zero"),
        (ref(0), .Exprs))
      => true
    </k>
    <env> 0 </env>
    <scopes>
        0 |-> scope(
          "triples_sum_to_zero"
            |-> closureVal(
                  ("l", .ParamNames),
                  Return(Bool(false)) .Stmts,
                  0),
          parent(-1))
       -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      -1 |-> intSeqGhost(iCons(0, iCons(0, iCons(0, .IntSeq))))
       0 |-> list(intVals(iCons(0, iCons(0, iCons(0, .IntSeq)))))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
