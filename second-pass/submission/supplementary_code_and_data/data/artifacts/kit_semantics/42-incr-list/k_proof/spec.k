requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-inv]:
    <k>
      #loop(
        list(REM:ValSeq),
        Name("x"),
        Expr(
          Call(
            Attribute(Name("result"), "append"),
            (BinOp("+", Name("x"), Int(1)), .Exprs)))
        .Stmts)
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "l"      |-> LVALUE:Val
        "result" |-> ref(H:Int)
        "x"      |-> (X:Val => ?X:Val),
        P:Parent)
      ...
    </scopes>
    <heap>
      ...
      H |-> (list(ACC:ValSeq) => list(incrAcc(ACC, REM)))
      ...
    </heap>
    <heapLoc> NEXT:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allNumeric(REM)

  claim [incr-list]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "incr_list",
            Params("l"),
            Assign(Name("result"), ListExpr(.Exprs))
            Assign(Name("x"), Int(0))
            For(
              Name("x"),
              Name("l"),
              Expr(
                Call(
                  Attribute(Name("result"), "append"),
                  (BinOp("+", Name("x"), Int(1)), .Exprs)))
              .Stmts)
            Return(Name("result"))
            .Stmts)
          .Stmts))
      ~> Call(Name("incr_list"), (ref(0), .Exprs))
      => ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(
         "incr_list" |->
           closureVal(
             "l",
             Assign(Name("result"), ListExpr(.Exprs))
             Assign(Name("x"), Int(0))
             For(
               Name("x"),
               Name("l"),
               Expr(
                 Call(
                   Attribute(Name("result"), "append"),
                   (BinOp("+", Name("x"), Int(1)), .Exprs)))
               .Stmts)
             Return(Name("result"))
             .Stmts,
             0),
         parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      0 |-> list(INPUT:ValSeq)
      =>
      0 |-> list(INPUT)
      1 |-> list(incrAcc(.ValSeq, INPUT))
    </heap>
    <heapLoc> 1 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allNumeric(INPUT)
endmodule
