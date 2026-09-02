requires "verification.k"

module SPEC
  imports VERIFICATION

  // The exact program-defined key lambda.  These exhaustive sign cases cover
  // every integer while making the fixed semantics' guarded bin rules usable.
  claim [key-nonnegative]:
    <k>
      Call(
        Lambda(
          Params("value", .ParamNames),
          CellVars(.ParamNames),
          FreeVars(.ParamNames),
          Call(
            Attribute(
              Call(Name("bin"), Name("value"), .Exprs),
              "count"),
            Str("1"),
            .Exprs)),
        Int(I:Int),
        .Exprs)
      => popcountAbs(I)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0

  claim [key-negative]:
    <k>
      Call(
        Lambda(
          Params("value", .ParamNames),
          CellVars(.ParamNames),
          FreeVars(.ParamNames),
          Call(
            Attribute(
              Call(Name("bin"), Name("value"), .Exprs),
              "count"),
            Str("1"),
            .Exprs)),
        Int(I:Int),
        .Exprs)
      => popcountAbs(I)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I <Int 0

  // Whole-program partial correctness over an arbitrary finite integer list.
  // Heap location 0 is the caller-owned input; locations 1 and 2 are the two
  // new lists allocated by the two stable sorted() calls.
  claim [sort-array]:
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
      ref(2)
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
      0 |-> list(VS:ValSeq)
      =>
      0 |-> list(VS)
      1 |-> list(sortVS(VS))
      2 |-> list(
             sortKeyVS(
               sortVS(VS),
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
    requires allIntVS(VS)
endmodule
