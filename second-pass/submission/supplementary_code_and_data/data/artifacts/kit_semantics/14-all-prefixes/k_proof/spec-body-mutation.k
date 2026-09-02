requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Mutation: reset prefix to the current character instead of extending it.
  claim [changed-body]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "all_prefixes",
            Params("string"),
            Assign(Name("prefixes"), ListExpr(.Exprs))
            Assign(Name("prefix"), Str(""))
            Assign(Name("char"), Str(""))
            For(
              Name("char"),
              Name("string"),
              Assign(Name("prefix"), Name("char"))
              Expr(
                Call(
                  Attribute(Name("prefixes"), "append"),
                  (Name("prefix"), .Exprs)))
              .Stmts)
            Return(Name("prefixes"))
            .Stmts)
          Assert(
            Compare(
              Call(Name("all_prefixes"), (Str("abc"), .Exprs)),
              CmpOp(
                "==",
                ListExpr(Str("a"), Str("ab"), Str("abc"), .Exprs))))
          .Stmts))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
