requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately mutated target: it returns [] for the realizable input [1].
  claim [empty-body-is-not-by-length]:
    <k>
      Call(
        Name("by_length"),
        (list(vCons(1, .ValSeq)), .Exprs))
      => ref(?H:Int)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        ("collect_digit"
           |-> closureVal(
                 ("arr", "digit", "name", .ParamNames),
                 collectDigitBody,
                 0)
         "by_length"
           |-> closureVal(
                 ("arr", .ParamNames),
                 Return(ListExpr(.Exprs)) .Stmts,
                 0)),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      (?H |-> list(byLengthVS(vCons(1, .ValSeq)))) ?REST:Map
    </heap>
    <heapLoc> 0 => ?NEXT:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
