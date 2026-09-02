requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-inv]:
    <k>
      #loop(
        rangeObj(I, C, 1),
        Name("i"),
        sortEvenLoopBody)
      ~> (Return(Name("result")) .Stmts)
      ~> #endcall
      => ref(0)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( 0 |-> scope(
          "sort_even" |-> closureVal("l", sortEvenBody, 0),
          parent(-1))
        1 |-> scope(
          ( "l"      |-> list(VS)
            "result" |-> ref(0)
            "evens"  |-> ref(2)
            "i"      |-> _J ),
          parent(0))
        -1 |-> builtinsScope )
      =>
      ( 0 |-> scope(
          "sort_even" |-> closureVal("l", sortEvenBody, 0),
          parent(-1))
        -1 |-> builtinsScope )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap>
      ( 0 |-> list(
          CUR
          => fillEven(
               CUR,
               sortVS(buildVS(VS, 0, vsLen(VS), 2)),
               I,
               C))
        1 |-> list(buildVS(VS, 0, vsLen(VS), 2))
        2 |-> list(sortVS(buildVS(VS, 0, vsLen(VS), 2))) )
    </heap>
    <heapLoc> 3 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      => .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0

  claim [sort-even]:
    <k>
      #loadAll(Module(FuncDef("sort_even", Params("l"), sortEvenBody)))
      ~> Call(Name("sort_even"), list(VS))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      ( 0 |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope )
      =>
      ( 0 |-> scope(
          "sort_even" |-> closureVal("l", sortEvenBody, 0),
          parent(-1))
        -1 |-> builtinsScope )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      ( 0 |-> list(sortEvenResult(VS))
        1 |-> list(buildVS(VS, 0, vsLen(VS), 2))
        2 |-> list(sortVS(buildVS(VS, 0, vsLen(VS), 2))) )
    </heap>
    <heapLoc> 0 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
