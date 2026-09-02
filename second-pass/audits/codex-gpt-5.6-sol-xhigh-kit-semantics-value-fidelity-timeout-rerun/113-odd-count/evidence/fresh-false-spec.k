requires "/tmp/audit-work/source/verification.k"

module FRESH-FALSE-SPEC
  imports VERIFICATION

  claim [odd-loop]:
    <k>
      #loop(
        list(INPUT:ValSeq),
        Name("s"),
        oddLoopBody)
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
               "odd_count" |-> closureVal(
                 ("lst", .ParamNames),
                 oddBody,
                 0),
               parent(-1))
      1  |-> scope(
               "count"  |-> (PREVN:Int => ?FINALN:Int)
               "lst"    |-> list(ORIGINAL:ValSeq)
               "result" |-> ref(0)
               "s"      |-> (PREVS:Val => ?FINALS:Val),
               parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      0 |-> list(ACC:ValSeq => oddRun(ACC, INPUT))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStringValues(INPUT)

  // Deliberately false: demand one extra None at the end of every result list.
  // Satisfying counterexample: INPUT=.ValSeq. Execution returns [], but this
  // postcondition demands [None].
  claim [odd-count-false]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "odd_count",
            Params(("lst", .ParamNames)),
            oddBody)))
      ~> Call(
           Name("odd_count"),
           (list(INPUT:ValSeq), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "odd_count" |-> closureVal(
                 ("lst", .ParamNames),
                 oddBody,
                 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
             valSeqConcat(
               oddRun(emptyOutput, INPUT),
               vCons(noneV, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStringValues(INPUT)
endmodule
