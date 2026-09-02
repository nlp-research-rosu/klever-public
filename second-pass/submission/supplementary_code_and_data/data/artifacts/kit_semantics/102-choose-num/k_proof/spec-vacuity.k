requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: choose_num(12, 15) is 14, not 15.
  claim [false-result]:
    <k>
      Call(Name("choose_num"), 12, 15)
      => ?R:Int
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "choose_num" |->
          closureVal(
            "x", "y", .ParamNames,
            If(
              Compare(Name("x"), CmpOp(">", Name("y"))),
              Return(UnaryOp("-", Int(1))) .Stmts,
              .Stmts)
            If(
              Compare(BinOp("%", Name("y"), Int(2)), CmpOp("==", Int(0))),
              Return(Name("y")) .Stmts,
              .Stmts)
            If(
              Compare(BinOp("-", Name("y"), Int(1)), CmpOp(">=", Name("x"))),
              Return(BinOp("-", Name("y"), Int(1))) .Stmts,
              .Stmts)
            Return(UnaryOp("-", Int(1))) .Stmts,
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
    ensures ?R ==Int 15
endmodule
