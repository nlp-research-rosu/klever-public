requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-invariant]:
    <k>
      #while(
        Compare(
          Name("i"),
          CmpOp("<", Call(Name("len"), (Name("l"), .Exprs)))),
        If(
          Compare(
            BinOp("%", Name("i"), Int(3)),
            CmpOp("==", Int(0))),
          (Expr(
             Call(
               Attribute(Name("result"), "append"),
               (Subscript(
                  Name("thirds"),
                  BinOp("//", Name("i"), Int(3))),
                .Exprs)))
           .Stmts),
          (Expr(
             Call(
               Attribute(Name("result"), "append"),
               (Subscript(Name("l"), Name("i")), .Exprs)))
           .Stmts))
        AugAssign(Name("i"), "+", Int(1))
        .Stmts)
      => .K
      ...
    </k>
    <env> L </env>
    <scopes>
      ...
      L |-> scope(
        "i" |-> (I => N)
        "l" |-> list(VS)
        "result" |-> ref(OUT)
        "thirds" |-> ref(THIRD),
        parent(0))
      0 |-> scope(MODULESCOPE, parent(-1))
      -1 |-> builtinsScope
      ...
    </scopes>
    <heap>
      ...
      OUT |-> list(
        A
        => valSeqConcat(A, mergeThirdFrom(VS, SV, I, N)))
      THIRD |-> list(SV)
      ...
    </heap>
    requires 0 <=Int I
     andBool I <=Int N
     andBool N ==Int vsLen(VS)
     andBool notBool ("len" in_keys(MODULESCOPE))

  claim [sort-third]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "sort_third",
            Params("l", .ParamNames),
            Assign(
              Name("thirds"),
              Call(
                Name("sorted"),
                (Subscript(
                   Name("l"),
                   Slice(NoBound, NoBound, Int(3))),
                 .Exprs)))
            Assign(Name("result"), ListExpr(.Exprs))
            Assign(Name("i"), Int(0))
            While(
              Compare(
                Name("i"),
                CmpOp(
                  "<",
                  Call(Name("len"), (Name("l"), .Exprs)))),
              If(
                Compare(
                  BinOp("%", Name("i"), Int(3)),
                  CmpOp("==", Int(0))),
                (Expr(
                   Call(
                     Attribute(Name("result"), "append"),
                     (Subscript(
                        Name("thirds"),
                        BinOp("//", Name("i"), Int(3))),
                      .Exprs)))
                 .Stmts),
                (Expr(
                   Call(
                     Attribute(Name("result"), "append"),
                     (Subscript(Name("l"), Name("i")), .Exprs)))
                 .Stmts))
              AugAssign(Name("i"), "+", Int(1))
              .Stmts)
            Return(Name("result"))
            .Stmts)
          .Stmts))
      ~> Call(
           Name("sort_third"),
           (list(VS), .Exprs))
      => ref(2)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(
         "sort_third" |->
           closureVal(
             ("l", .ParamNames),
             Assign(
               Name("thirds"),
               Call(
                 Name("sorted"),
                 (Subscript(
                    Name("l"),
                    Slice(NoBound, NoBound, Int(3))),
                  .Exprs)))
             Assign(Name("result"), ListExpr(.Exprs))
             Assign(Name("i"), Int(0))
             While(
               Compare(
                 Name("i"),
                 CmpOp(
                   "<",
                   Call(Name("len"), (Name("l"), .Exprs)))),
               If(
                 Compare(
                   BinOp("%", Name("i"), Int(3)),
                   CmpOp("==", Int(0))),
                 (Expr(
                    Call(
                      Attribute(Name("result"), "append"),
                      (Subscript(
                         Name("thirds"),
                         BinOp("//", Name("i"), Int(3))),
                       .Exprs)))
                  .Stmts),
                 (Expr(
                    Call(
                      Attribute(Name("result"), "append"),
                      (Subscript(Name("l"), Name("i")), .Exprs)))
                  .Stmts))
               AugAssign(Name("i"), "+", Int(1))
               .Stmts)
             Return(Name("result"))
             .Stmts,
             0),
         parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      (0 |-> list(buildVS(VS, 0, vsLen(VS), 3))
       1 |-> list(sortVS(buildVS(VS, 0, vsLen(VS), 3)))
       2 |-> list(sortThirdResult(VS)))
    </heap>
    <heapLoc> 0 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
