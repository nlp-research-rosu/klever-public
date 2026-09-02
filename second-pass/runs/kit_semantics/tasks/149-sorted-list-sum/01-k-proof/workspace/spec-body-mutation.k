requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Body mutation: keep odd lengths instead of even lengths. The original
  // expected result for ["aa"] must therefore become unprovable.
  claim [odd-filter-mutant]:
    <k>
      Call(
        Name("sorted_list_sum"),
        list(
          vCons(
            str(iCons(97, iCons(97, .IntSeq))),
            .ValSeq)))
      => ref(2)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "sorted_list_sum"
             |-> closureVal(
                   ("lst", .ParamNames),
                   Assign(Name("result"), ListExpr(.Exprs))
                   Assign(Name("word"), Str(""))
                   For(
                     Name("word"),
                     Name("lst"),
                     If(
                       Compare(
                         BinOp(
                           "%",
                           Call(Name("len"), Name("word")),
                           Int(2)),
                         CmpOp("!=", Int(0))),
                       Expr(
                         Call(
                           Attribute(Name("result"), "append"),
                           Name("word"))),
                       .Stmts))
                   Return(
                     Call(
                       Name("sorted"),
                       Call(Name("sorted"), Name("result")),
                       KwArg("key", Name("len")))),
                   0),
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
             vCons(
               str(iCons(97, iCons(97, .IntSeq))),
               .ValSeq))
      1 |-> list(
             vCons(
               str(iCons(97, iCons(97, .IntSeq))),
               .ValSeq))
      2 |-> list(
             sortKeyVS(
               vCons(
                 str(iCons(97, iCons(97, .IntSeq))),
                 .ValSeq),
               builtinV("len")))
    </heap>
    <heapLoc> 0 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
