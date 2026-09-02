requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the exact program returns the second newly allocated
  // list at ref(2), not the intermediate numeric sort at ref(1).
  claim [wrong-result]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "sort_array",
            Params("arr", .ParamNames),
            Return(
              Call(
                Name("sorted"),
                Call(
                  Name("sorted"),
                  Name("arr"),
                  .Exprs),
                KwArg(
                  "key",
                  Lambda(
                    Params("value", .ParamNames),
                    CellVars(.ParamNames),
                    FreeVars(.ParamNames),
                    Call(
                      Attribute(
                        Call(Name("bin"), Name("value"), .Exprs),
                        "count"),
                      Str("1"),
                      .Exprs))),
                .Exprs))
            .Stmts)))
      ~> Call(Name("sort_array"), ref(0), .Exprs)
      =>
      ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
              .Map[
                "sort_array" <-
                  closureVal(
                    ("arr", .ParamNames),
                    Return(
                      Call(
                        Name("sorted"),
                        Call(
                          Name("sorted"),
                          Name("arr"),
                          .Exprs),
                        KwArg(
                          "key",
                          Lambda(
                            Params("value", .ParamNames),
                            CellVars(.ParamNames),
                            FreeVars(.ParamNames),
                            Call(
                              Attribute(
                                Call(Name("bin"), Name("value"), .Exprs),
                                "count"),
                              Str("1"),
                              .Exprs))),
                        .Exprs))
                    .Stmts,
                    0)],
              parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      0 |-> list(vCons(3, .ValSeq))
      =>
      0 |-> list(vCons(3, .ValSeq))
      1 |-> list(sortVS(vCons(3, .ValSeq)))
      2 |-> list(
             sortKeyVS(
               sortVS(vCons(3, .ValSeq)),
               closureValC(
                 ("value", .ParamNames),
                 .ParamNames,
                 Return(
                   Call(
                     Attribute(
                       Call(Name("bin"), Name("value"), .Exprs),
                       "count"),
                     Str("1"),
                     .Exprs))
                 .Stmts,
                 .Map)))
    </heap>
    <heapLoc> 1 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
