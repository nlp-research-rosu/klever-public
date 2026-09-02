requires "verification.k"

module AUDIT-FRESH-VACUITY
  imports VERIFICATION

  // Fresh false result mutation: choose_num(4,5) is 4, not 5.
  claim [false-result-4-5]:
    <k>
      Call(Name("choose_num"), 4, 5)
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
    ensures ?R ==Int 5
endmodule
