requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [filter-loop]:
    <k>
      #loop(
        list(INPUT:ValSeq),
        Name("string"),
        filterLoopBody)
      ~> (Return(Name("result")) .Stmts):Stmts
      ~> #endcall
      => ref(H:Int)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (SC:Map
       1 |-> scope(
              "strings" |-> list(ORIGINAL:ValSeq)
              "prefix" |-> str(P:IntSeq)
              "result" |-> ref(H)
              "string" |-> str(OLD:IntSeq),
              parent(0)))
      => SC
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap>
      HP:Map
      H |-> list(
             ACC:ValSeq
             => filterPrefixAcc(ACC, INPUT, P))
    </heap>
    <heapLoc> NEXT:Int </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires allStrings(INPUT)

  claim [filter-program]:
    <k>
      #loadAll(filterByPrefixProgram)
      ~> Call(
           Name("filter_by_prefix"),
           list(INPUT:ValSeq),
           str(PREFIX:IntSeq))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             .Map
             => "filter_by_prefix" |->
                  closureVal(
                    ("strings", "prefix"),
                    filterFunctionBody,
                    0),
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(
           filterPrefixAcc(.ValSeq, INPUT, PREFIX))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires allStrings(INPUT)
endmodule
