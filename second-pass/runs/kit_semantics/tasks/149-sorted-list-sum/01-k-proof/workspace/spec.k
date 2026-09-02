requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [filter-loop]:
    <k>
      #loop(
        list(INPUT:ValSeq),
        Name("word"),
        If(
          Compare(
            BinOp("%", Call(Name("len"), Name("word")), Int(2)),
            CmpOp("==", Int(0))),
          Expr(
            Call(
              Attribute(Name("result"), "append"),
              Name("word"))),
          .Stmts))
      => .K ...
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
              "sorted_list_sum"
              |-> closureVal(
                    ("lst", .ParamNames),
                    sortedListSumBody,
                    0),
              parent(-1))
       1 |-> scope(
              "lst"    |-> list(WHOLE:ValSeq)
              "result" |-> ref(H:Int)
              "word"   |-> (OLD:Val => ?LAST:Val),
              parent(0))
    </scopes>
    <heap>
      H |-> list(ACC:ValSeq => scanEven(ACC, INPUT))
    </heap>
    requires stringsOnly(INPUT)

  claim [sorted-list-sum]:
    <k>
      #loadAll(sortedListSumModule)
      ~> Call(Name("sorted_list_sum"), list(INPUT:ValSeq))
      => ref(2)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> (scope(.Map, parent(-1))
             => scope(
                  "sorted_list_sum"
                  |-> closureVal(
                        ("lst", .ParamNames),
                        sortedListSumBody,
                        0),
                  parent(-1)))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(scanEven(.ValSeq, INPUT))
      1 |-> list(sortVS(scanEven(.ValSeq, INPUT)))
      2 |-> list(
             sortKeyVS(
               sortVS(scanEven(.ValSeq, INPUT)),
               builtinV("len")))
    </heap>
    <heapLoc> 0 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires stringsOnly(INPUT)
endmodule
