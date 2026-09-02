requires "verification.k"

module SPEC-REVIEWER-VACUITY
  imports VERIFICATION

  // Satisfying input ["abc"], "a"; the real result is ["abc"].
  // This fresh mutation falsely requires the allocated result list to be empty.
  claim [false-ground-result]:
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
           list(
             vCons(
               str(iCons(97, iCons(98, iCons(99, .IntSeq)))),
               .ValSeq)),
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
      0 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
