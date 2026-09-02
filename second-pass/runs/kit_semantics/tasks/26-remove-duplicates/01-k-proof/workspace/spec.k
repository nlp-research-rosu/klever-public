requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [remove-duplicates-loop]:
    <k>
      #loop(
        list(REST:ValSeq),
        Name("number"),
        If(
          Compare(
            Call(
              Attribute(Name("numbers"), "count"),
              (Name("number"), .Exprs)),
            CmpOp("==", Int(1))),
          Expr(
            Call(
              Attribute(Name("result"), "append"),
              (Name("number"), .Exprs))),
          .Stmts))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "numbers" |-> list(ALL:ValSeq)
        "result"  |-> ref(H:Int)
        "number"  |-> (N:Val => ?N:Val),
        parent(0))
      ...
    </scopes>
    <heap>
      ...
      H |-> list(ACC:ValSeq => rdAcc(ACC, REST, ALL))
      ...
    </heap>
    requires allInts(REST) andBool allInts(ALL)

  claim [remove-duplicates]:
    <k>
      #loadAll(
        Module(
          ImportFrom("typing", "List")
          FuncDef(
            "remove_duplicates",
            Params("numbers"),
            Assign(Name("result"), ListExpr(.Exprs))
            Assign(Name("number"), Int(0))
            For(
              Name("number"),
              Name("numbers"),
              If(
                Compare(
                  Call(
                    Attribute(Name("numbers"), "count"),
                    (Name("number"), .Exprs)),
                  CmpOp("==", Int(1))),
                Expr(
                  Call(
                    Attribute(Name("result"), "append"),
                    (Name("number"), .Exprs))),
                .Stmts))
            Return(Name("result")))))
      ~> Call(
           Name("remove_duplicates"),
           (list(INPUT:ValSeq), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> (scope(.Map, parent(-1))
              => scope(
                   "remove_duplicates" |->
                     closureVal(
                       ("numbers", .ParamNames),
                       Assign(Name("result"), ListExpr(.Exprs))
                       Assign(Name("number"), Int(0))
                       For(
                         Name("number"),
                         Name("numbers"),
                         If(
                           Compare(
                             Call(
                               Attribute(Name("numbers"), "count"),
                               (Name("number"), .Exprs)),
                             CmpOp("==", Int(1))),
                           Expr(
                             Call(
                               Attribute(Name("result"), "append"),
                               (Name("number"), .Exprs))),
                           .Stmts))
                       Return(Name("result")),
                       0),
                   parent(-1)))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map => 0 |-> list(rdAcc(.ValSeq, INPUT, INPUT))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(INPUT)
endmodule
