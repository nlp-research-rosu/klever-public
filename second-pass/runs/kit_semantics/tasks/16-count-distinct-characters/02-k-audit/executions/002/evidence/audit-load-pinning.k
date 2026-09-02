requires "verification.k"

module AUDIT-LOAD-PINNING
  imports VERIFICATION

  claim [module-load-creates-exact-entry-binding]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "count_distinct_characters",
            Params("string"),
            Return(
              Call(
                Name("len"),
                Call(
                  Name("set"),
                  Call(Attribute(Name("string"), "lower"), .Exprs)
                )
              )
            ) .Stmts
          ) .Stmts
        )
      )
      =>
      .K
    </k>
    <env> 0 </env>
    <scopes>
      (
        0 |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope
      )
      =>
      (
        0 |-> scope(
          "count_distinct_characters" |->
            closureVal(
              ("string", .ParamNames),
              Return(
                Call(
                  Name("len"),
                  Call(
                    Name("set"),
                    Call(Attribute(Name("string"), "lower"), .Exprs)
                  )
                )
              ) .Stmts,
              0
            ),
          parent(-1)
        )
        -1 |-> builtinsScope
      )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
