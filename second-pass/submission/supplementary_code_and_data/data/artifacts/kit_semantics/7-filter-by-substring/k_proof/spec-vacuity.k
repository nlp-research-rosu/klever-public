requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false for the satisfiable witness strings=[],
  // substring="a": the claimed result contains one empty string.
  claim [false-postcondition]:
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
           list(.ValSeq),
           str(iCons(97, .IntSeq)))
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
      0 |-> list(vCons(str(.IntSeq), .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
