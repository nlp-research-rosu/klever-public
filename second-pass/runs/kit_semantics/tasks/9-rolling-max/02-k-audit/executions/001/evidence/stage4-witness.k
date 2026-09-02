requires "verification.k"

module STAGE4-WITNESS
  imports VERIFICATION

  claim [entry-empty-witness]:
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
      0 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [entry-nonempty-witness]:
    <k>
      Call(
        Name("rolling_max"),
        (list(vCons(1, vCons(-2, vCons(3, vCons(2, .ValSeq))))), .Exprs))
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
      0 |-> list(vCons(1, vCons(1, vCons(3, vCons(3, .ValSeq)))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [loop-witness]:
    <k>
      #loop(
        list(vCons(2, vCons(-1, vCons(3, .ValSeq)))),
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
      0 |-> scope(.Map, parent(-1))
      1 |-> scope(
        "current" |-> (1 => 3)
        "number"  |-> (1 => 3)
        "numbers" |-> list(vCons(1, vCons(2, vCons(-1, vCons(3, .ValSeq)))))
        "result"  |-> ref(0),
        parent(0))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      0 |-> list(
        vCons(1, .ValSeq)
        =>
        vCons(1, vCons(2, vCons(2, vCons(3, .ValSeq)))))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
