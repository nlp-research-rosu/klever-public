requires "verification.k"

module AUDIT-FALSE-SPEC
  imports VERIFICATION

  // Fresh auditor mutation: [0, 2] has even endpoint sum and therefore
  // returns [2, 0]. This deliberately false destination demands [0, 2].
  claim [audit-false-even-branch]:
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
      (0 |-> list(vCons(0, vCons(2, .ValSeq))))
      =>
      (0 |-> list(vCons(0, vCons(2, .ValSeq)))
       1 |-> list(vCons(0, vCons(2, .ValSeq))))
    </heap>
    <heapLoc> 1 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
