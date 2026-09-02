requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-invariant]:
    <k>
      #loop(
        str(R:IntSeq),
        Name("char"),
        Assign(
          Name("prefix"),
          BinOp("+", Name("prefix"), Name("char")))
        Expr(
          Call(
            Attribute(Name("prefixes"), "append"),
            (Name("prefix"), .Exprs)))
        .Stmts)
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "string"   |-> str(INPUT:IntSeq)
        "prefixes" |-> ref(H:Int)
        "prefix"   |-> (str(P:IntSeq) => str(finishPrefix(P, R)))
        "char"     |-> (CH:Val => finishChar(CH, R)),
        parent(0))
      ...
    </scopes>
    <heap>
      ...
      H |-> (list(ACC:ValSeq) => list(prefixesAcc(P, R, ACC)))
      ...
    </heap>

  claim [all-prefixes]:
    <k>
      #loadAll(
        Module(
          ImportFrom("typing", "List")
          FuncDef(
            "all_prefixes",
            Params("string"),
            Assign(Name("prefixes"), ListExpr(.Exprs))
            Assign(Name("prefix"), Str(""))
            Assign(Name("char"), Str(""))
            For(
              Name("char"),
              Name("string"),
              Assign(
                Name("prefix"),
                BinOp("+", Name("prefix"), Name("char")))
              Expr(
                Call(
                  Attribute(Name("prefixes"), "append"),
                  (Name("prefix"), .Exprs)))
              .Stmts)
            Return(Name("prefixes"))
            .Stmts)
          Assign(
            Name("result"),
            Call(Name("all_prefixes"), (Name("input"), .Exprs)))
          .Stmts))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(
        "input" |-> str(INPUT:IntSeq),
        parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(
        "input" |-> str(INPUT)
        "all_prefixes" |-> closureVal(
          "string",
          .ParamNames,
          Assign(Name("prefixes"), ListExpr(.Exprs))
          Assign(Name("prefix"), Str(""))
          Assign(Name("char"), Str(""))
          For(
            Name("char"),
            Name("string"),
            Assign(
              Name("prefix"),
              BinOp("+", Name("prefix"), Name("char")))
            Expr(
              Call(
                Attribute(Name("prefixes"), "append"),
                (Name("prefix"), .Exprs)))
            .Stmts)
          Return(Name("prefixes"))
          .Stmts,
          0)
        "result" |-> ref(0),
        parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(prefixesAcc(.IntSeq, INPUT, .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
