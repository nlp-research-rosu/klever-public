requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: [0, 1] has odd endpoint sum and must remain ascending,
  // while this destination demands [1, 0].
  claim [false-result]:
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
                KwArg(
                  "reverse",
                  Compare(
                    BinOp(
                      "%",
                      BinOp(
                        "+",
                        Subscript(Name("array"), Int(0)),
                        Subscript(Name("array"), UnaryOp("-", Int(1)))),
                      Int(2)),
                    CmpOp("==", Int(0)))))) .Stmts,
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      (0 |-> list(vCons(0, vCons(1, .ValSeq))))
      =>
      (0 |-> list(vCons(0, vCons(1, .ValSeq)))
       1 |-> list(vCons(1, vCons(0, .ValSeq))))
    </heap>
    <heapLoc> 1 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
