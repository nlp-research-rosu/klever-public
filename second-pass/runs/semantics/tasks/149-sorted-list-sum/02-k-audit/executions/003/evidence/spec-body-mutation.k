requires "verification.k"

module SPEC-BODY-MUTATION
  imports HUMANEVAL-VERIFICATION

  // Material mutation of the actual function term: retain odd-length strings
  // while leaving the original even-filter postcondition unchanged.
  claim
    <k>
      FuncDef(
        "sorted_list_sum",
        Params("lst"),
        Assign(Name("even_words"), ListExpr(.Exprs))
        For(
          Name("word"),
          Name("lst"),
          If(
            Compare(
              BinOp("%", Call(Name("len"), Name("word")), Int(2)),
              CmpOp("==", Int(1))),
            Expr(
              Call(
                Attribute(Name("even_words"), "append"),
                Name("word"))),
            .Stmts))
        Return(
          Call(
            Name("sorted"),
            Call(Name("sorted"), Name("even_words")),
            KwArg("key", Name("len")))))
      ~> Call(Name("sorted_list_sum"), list(strVals(INPUT:StrList)))
    =>
      ref(2)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0  |-> scope(
              .Map [
                "sorted_list_sum" <-
                  closureVal(
                    ("lst", .ParamNames),
                    Assign(Name("even_words"), ListExpr(.Exprs))
                    For(
                      Name("word"),
                      Name("lst"),
                      If(
                        Compare(
                          BinOp("%", Call(Name("len"), Name("word")), Int(2)),
                          CmpOp("==", Int(1))),
                        Expr(
                          Call(
                            Attribute(Name("even_words"), "append"),
                            Name("word"))),
                        .Stmts))
                    Return(
                      Call(
                        Name("sorted"),
                        Call(Name("sorted"), Name("even_words")),
                        KwArg("key", Name("len")))),
                    0)
              ],
              parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
    =>
      .Map
        [ 0 <- list(evenAppend(.ValSeq, INPUT)) ]
        [ 1 <- list(sortVS(evenAppend(.ValSeq, INPUT))) ]
        [ 2 <- list(
                 sortKeyVS(
                   sortVS(evenAppend(.ValSeq, INPUT)),
                   builtinV("len"))) ]
    </heap>
    <heapLoc> 0 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
