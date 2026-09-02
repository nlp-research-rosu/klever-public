requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [filter-loop]:
    <k>
      #loop(
        list(VS:ValSeq),
        Name("string"),
        If(
          Compare(Name("substring"), CmpOp("in", Name("string"))),
          Expr(
            Call(
              Attribute(Name("result"), "append"),
              Name("string"))),
          .Stmts))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      OUTER:Map
      L |-> scope(
        "result" |-> ref(H:Int)
        "string" |-> OLD:Val
        "strings" |-> list(ORIGINAL:ValSeq)
        "substring" |-> str(P:IntSeq),
        PAR:Parent)
      =>
      OUTER
      L |-> scope(
        "result" |-> ref(H)
        "string" |-> ?LAST:Val
        "strings" |-> list(ORIGINAL)
        "substring" |-> str(P),
        PAR)
    </scopes>
    <heap>
      H |-> list(
        ACC:ValSeq
        =>
        filterAcc(ACC, P, VS))
      HEAP:Map
    </heap>
    requires allStrVS(VS)

  claim [filter-by-substring]:
    <k>
      #loadAll(
        Module(
          ImportFrom("typing", "List")
          FuncDef(
            "filter_by_substring",
            Params("strings", "substring"),
            Assign(Name("result"), ListExpr(.Exprs))
            Assign(Name("string"), Str(""))
            For(
              Name("string"),
              Name("strings"),
              If(
                Compare(
                  Name("substring"),
                  CmpOp("in", Name("string"))),
                Expr(
                  Call(
                    Attribute(Name("result"), "append"),
                    Name("string"))),
                .Stmts))
            Return(Name("result")))))
      ~> Call(
           Name("filter_by_substring"),
           list(VS:ValSeq),
           str(P:IntSeq))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "filter_by_substring" |->
          closureVal(
            ("strings", "substring", .ParamNames),
            Assign(Name("result"), ListExpr(.Exprs))
            Assign(Name("string"), Str(""))
            For(
              Name("string"),
              Name("strings"),
              If(
                Compare(
                  Name("substring"),
                  CmpOp("in", Name("string"))),
                Expr(
                  Call(
                    Attribute(Name("result"), "append"),
                    Name("string"))),
                .Stmts))
            Return(Name("result")),
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(filterAcc(.ValSeq, P, VS))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStrVS(VS)
endmodule
