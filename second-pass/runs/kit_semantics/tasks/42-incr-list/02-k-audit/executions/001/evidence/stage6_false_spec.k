requires "verification.k"

module AUDIT-FALSE-SPEC
  imports VERIFICATION

  // The genuine general loop circularity is retained so the ground entry probe
  // fails only at its deliberately false result obligation.
  claim [audit-loop-inv]:
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

  // False witness: on input [0], the exact original body returns [1], not [2].
  claim [audit-false-result]:
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
      0 |-> list(vCons(0, .ValSeq))
      =>
      0 |-> list(vCons(0, .ValSeq))
      1 |-> list(vCons(2, .ValSeq))
    </heap>
    <heapLoc> 1 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
