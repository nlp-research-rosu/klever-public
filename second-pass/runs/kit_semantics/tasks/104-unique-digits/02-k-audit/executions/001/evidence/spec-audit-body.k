requires "verification.k"

module SPEC-AUDIT-BODY
  imports VERIFICATION

  // Inner decimal digit-loop circularity.
  claim [digit-loop]:
    <k>
      #while(
        Compare(Name("number"), CmpOp(">", Int(0))),
        AugAssign(
          Name("bad"),
          "+",
          Compare(
            BinOp("%", Name("number"), Int(7)),
            CmpOp("==", Int(0))))
        AugAssign(Name("number"), "//", Int(10))
        .Stmts)
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "x"      |-> X:Val
        "result" |-> R:Val
        "value"  |-> V:Val
        "number" |-> (N:Int => scanNumber(N))
        "bad"    |-> (B:Int => scanBad(B, N)),
        parent(0))
      ...
    </scopes>

  // Outer list-loop circularity.  The loop consumes the exact embedded suffix
  // XS and updates every persistent local and the result heap object.
  claim [outer-loop]:
    <k>
      #loop(
        list(XS:ValSeq),
        Name("value"),
        Assign(
          Name("number"),
          Call(
            Name("sum"),
            (TupleExpr((Name("value"), .Exprs)), .Exprs)))
        Assign(Name("bad"), Int(0))
        While(
          Compare(Name("number"), CmpOp(">", Int(0))),
          AugAssign(
            Name("bad"),
            "+",
            Compare(
              BinOp("%", Name("number"), Int(7)),
              CmpOp("==", Int(0))))
          AugAssign(Name("number"), "//", Int(10))
          .Stmts)
        If(
          Compare(Name("bad"), CmpOp("==", Int(0))),
          Expr(
            Call(
              Attribute(Name("result"), "append"),
              (Name("value"), .Exprs)))
          .Stmts,
          .Stmts)
        .Stmts)
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(
        "unique_digits" |->
          closureVal(
            "x", .ParamNames,
            Assign(Name("result"), ListExpr(.Exprs))
            Assign(Name("value"), Int(0))
            Assign(Name("number"), Int(0))
            Assign(Name("bad"), Int(0))
            For(
              Name("value"), Name("x"),
              Assign(
                Name("number"),
                Call(
                  Name("sum"),
                  (TupleExpr((Name("value"), .Exprs)), .Exprs)))
              Assign(Name("bad"), Int(0))
              While(
                Compare(Name("number"), CmpOp(">", Int(0))),
                AugAssign(
                  Name("bad"),
                  "+",
                  Compare(
                    BinOp("%", Name("number"), Int(7)),
                    CmpOp("==", Int(0))))
                AugAssign(Name("number"), "//", Int(10))
                .Stmts)
              If(
                Compare(Name("bad"), CmpOp("==", Int(0))),
                Expr(
                  Call(
                    Attribute(Name("result"), "append"),
                    (Name("value"), .Exprs)))
                .Stmts,
                .Stmts)
              .Stmts)
            Return(Call(Name("sorted"), (Name("result"), .Exprs)))
            .Stmts,
            0),
        parent(-1))
      1 |-> scope(
        "x"      |-> list(ALL:ValSeq)
        "result" |-> ref(0)
        "value"  |-> (V:Val => afterValue(XS, V))
        "number" |-> (N:Int => afterNumber(XS, N))
        "bad"    |-> (B:Int => afterBad(XS, B)),
        parent(0))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      0 |-> list(ACC:ValSeq => collect(ACC, XS))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> ListItem(frame(CALLER:K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires integerVals(XS)

  // Whole-program entry claim: execute the exact translated function body,
  // call it on an arbitrary finite list of positive integers, and constrain
  // both the retained accumulator and the returned sorted list.
  claim [program]:
    <k>
      FuncDef(
        "unique_digits", Params("x"),
        Assign(Name("result"), ListExpr(.Exprs))
        Assign(Name("value"), Int(0))
        Assign(Name("number"), Int(0))
        Assign(Name("bad"), Int(0))
        For(
          Name("value"), Name("x"),
          Assign(
            Name("number"),
            Call(
              Name("sum"),
              (TupleExpr((Name("value"), .Exprs)), .Exprs)))
          Assign(Name("bad"), Int(0))
          While(
            Compare(Name("number"), CmpOp(">", Int(0))),
            AugAssign(
              Name("bad"),
              "+",
              Compare(
                BinOp("%", Name("number"), Int(7)),
                CmpOp("==", Int(0))))
            AugAssign(Name("number"), "//", Int(10))
            .Stmts)
          If(
            Compare(Name("bad"), CmpOp("==", Int(0))),
            Expr(
              Call(
                Attribute(Name("result"), "append"),
                (Name("value"), .Exprs)))
            .Stmts,
            .Stmts)
          .Stmts)
        Return(Call(Name("sorted"), (Name("result"), .Exprs)))
        .Stmts)
      ~> Call(
           Name("unique_digits"),
           (list(XS:ValSeq), .Exprs))
      => ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> (scope(.Map, parent(-1))
             =>
             scope(
               "unique_digits" |->
                 closureVal(
                   "x", .ParamNames,
                   Assign(Name("result"), ListExpr(.Exprs))
                   Assign(Name("value"), Int(0))
                   Assign(Name("number"), Int(0))
                   Assign(Name("bad"), Int(0))
                   For(
                     Name("value"), Name("x"),
                     Assign(
                       Name("number"),
                       Call(
                         Name("sum"),
                         (TupleExpr((Name("value"), .Exprs)), .Exprs)))
                     Assign(Name("bad"), Int(0))
                     While(
                       Compare(Name("number"), CmpOp(">", Int(0))),
                       AugAssign(
                         Name("bad"),
                         "+",
                         Compare(
                           BinOp("%", Name("number"), Int(7)),
                           CmpOp("==", Int(0))))
                       AugAssign(Name("number"), "//", Int(10))
                       .Stmts)
                     If(
                       Compare(Name("bad"), CmpOp("==", Int(0))),
                       Expr(
                         Call(
                           Attribute(Name("result"), "append"),
                           (Name("value"), .Exprs)))
                       .Stmts,
                       .Stmts)
                     .Stmts)
                   Return(
                     Call(Name("sorted"), (Name("result"), .Exprs)))
                   .Stmts,
                   0),
               parent(-1)))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(collect(.ValSeq, XS))
      1 |-> list(sortVS(collect(.ValSeq, XS)))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires integerVals(XS)
endmodule
