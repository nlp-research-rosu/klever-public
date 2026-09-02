requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [load-choose-num]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "choose_num", Params("x", "y"),
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
            Return(UnaryOp("-", Int(1))) .Stmts)))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
      =>
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
        parent(-1)))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [choose-num]:
    <k>
      Call(Name("choose_num"), X:Int, Y:Int)
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
    requires X >Int 0 andBool Y >Int 0
    ensures ?R ==Int chooseNumSpec(X, Y)
endmodule
