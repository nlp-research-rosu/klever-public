requires "loop-base.k"

module LOOP-SPEC
  imports LOOP-BASE

  claim [rolling-loop-connection]:
    <k>
      #loop(
        list(IS:ValSeq),
        Name("number"),
        If(
          Compare(Name("number"), CmpOp(">", Name("current"))),
          Assign(Name("current"), Name("number")) .Stmts,
          .Stmts)
        Expr(Call(
          Attribute(Name("result"), "append"),
          (Name("current"), .Exprs))) .Stmts)
      ~> .Stmts
      ~> Return(Name("result")) .Stmts
      ~> #endcall
      =>
      .Stmts
      ~> Return(Name("result")) .Stmts
      ~> #endcall
    </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(MODULE:Map, parent(-1))
      1 |-> scope(
        "current" |-> (M:Int => foldMax(M, IS))
        "number"  |-> (D:Int => lastOr(D, IS))
        "numbers" |-> list(ORIGINAL:ValSeq)
        "result"  |-> ref(0),
        parent(0))
      -1 |-> BUILTINS:Scope
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      0 |-> list(A:ValSeq => rollAcc(A, M, IS))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(IS)
endmodule
