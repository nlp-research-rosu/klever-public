requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false for the satisfiable witness "abc": "ab" is omitted.
  claim [false-postcondition]:
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
          Assert(
            Compare(
              Call(Name("all_prefixes"), (Str("abc"), .Exprs)),
              CmpOp(
                "==",
                ListExpr(Str("a"), Str("abc"), .Exprs))))
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
