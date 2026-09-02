requires "verification.k"

module AUDITOR-BODY-MUTATION
  imports VERIFICATION

  // The actually bound and executed closure body now always returns [].
  // The destination deliberately retains the original ["1"] result.
  claim [changed-executed-body]:
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
        "odd_count" |->
          closureVal(
            "lst",
            Assign(Name("result"), ListExpr(.Exprs))
            Return(Name("result"))
            .Stmts,
            0),
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
