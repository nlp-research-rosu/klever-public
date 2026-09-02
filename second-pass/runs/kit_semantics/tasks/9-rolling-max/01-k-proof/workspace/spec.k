requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [rolling-loop]:
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

  claim [rolling-max-empty]:
    <k>
      Call(Name("rolling_max"), (list(.ValSeq), .Exprs))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "rolling_max" |->
          closureVal(
            ("numbers", .ParamNames),
            Expr(Str("Return the maximum seen at each position in numbers."))
            Assign(Name("result"), ListExpr(.Exprs))
            If(
              Name("numbers"),
              Assign(
                Name("current"),
                Subscript(Name("numbers"), Int(0)))
              Assign(Name("number"), Name("current"))
              For(
                Name("number"),
                Name("numbers"),
                If(
                  Compare(
                    Name("number"),
                    CmpOp(">", Name("current"))),
                  Assign(Name("current"), Name("number")) .Stmts,
                  .Stmts)
                Expr(Call(
                  Attribute(Name("result"), "append"),
                  (Name("current"), .Exprs))) .Stmts)
              .Stmts,
              .Stmts)
            Return(Name("result")) .Stmts,
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(rollingMax(.ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [rolling-max-nonempty]:
    <k>
      Call(
        Name("rolling_max"),
        (list(vCons(H:Int, T:ValSeq)), .Exprs))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "rolling_max" |->
          closureVal(
            ("numbers", .ParamNames),
            Expr(Str("Return the maximum seen at each position in numbers."))
            Assign(Name("result"), ListExpr(.Exprs))
            If(
              Name("numbers"),
              Assign(
                Name("current"),
                Subscript(Name("numbers"), Int(0)))
              Assign(Name("number"), Name("current"))
              For(
                Name("number"),
                Name("numbers"),
                If(
                  Compare(
                    Name("number"),
                    CmpOp(">", Name("current"))),
                  Assign(Name("current"), Name("number")) .Stmts,
                  .Stmts)
                Expr(Call(
                  Attribute(Name("result"), "append"),
                  (Name("current"), .Exprs))) .Stmts)
              .Stmts,
              .Stmts)
            Return(Name("result")) .Stmts,
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(rollingMax(vCons(H, T)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(T)
endmodule
