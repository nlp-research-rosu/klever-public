requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The body is materially changed to reverse every nonempty input. The
  // original postcondition for the witness [0, 1] must therefore be rejected.
  claim [mutated-body]:
    <k> Call(Name("sort_array"), ref(0)) => ref(1) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "sort_array" |->
          closureVal(
            "array",
            If(
              UnaryOp("not", Name("array")),
              Return(Call(Name("sorted"), Name("array"))) .Stmts,
              .Stmts)
            Return(
              Call(
                Name("sorted"),
                Name("array"),
                KwArg("reverse", Bool(true)))) .Stmts,
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      (0 |-> list(vCons(0, vCons(1, .ValSeq))))
      =>
      (0 |-> list(vCons(0, vCons(1, .ValSeq)))
       1 |-> list(vCons(0, vCons(1, .ValSeq))))
    </heap>
    <heapLoc> 1 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
