requires "verification.k"

module AUDIT-VACUITY
  imports DOUBLE-THE-DIFFERENCE-VERIFICATION

  // Exact candidate body and a satisfiable mixed input, but the result
  // obligation is deliberately false: the real result is 58, not 59.
  claim [false-result-must-fail]:
    <k>
      Call(
        Name("double_the_difference"),
        list(numVals(
          fNum(3.0,
          iNum(3,
          iNum(-5,
          fNum(2.5,
          iNum(7, .NumSeq))))))))
      => 59
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "double_the_difference" |->
          closureVal(
            "lst",
            Assign(Name("total"), Int(0))
            Assign(Name("number"), Int(0))
            For(
              Name("number"),
              Name("lst"),
              If(
                BoolOp(
                  "and",
                  Call(
                    Name("isinstance"),
                    Name("number"),
                    Name("int")),
                  Compare(
                    Name("number"),
                    CmpOp(">", Int(0))),
                  Compare(
                    BinOp("%", Name("number"), Int(2)),
                    CmpOp("==", Int(1)))),
                AugAssign(
                  Name("total"),
                  "+",
                  BinOp("**", Name("number"), Int(2))),
                .Stmts))
            Return(Name("total")),
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
