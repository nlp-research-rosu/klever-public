requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The function body is deliberately changed to `return False`, while the
  // postcondition still demands the original witness result True.
  claim [changed-body]:
    <k>
      Call(
        Name("will_it_fly"),
        (list(vCons(3, .ValSeq)), 5, .Exprs))
      => true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "will_it_fly" |->
          closureVal(
            ("q", "w", .ParamNames),
            Return(Bool(false)) .Stmts,
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
