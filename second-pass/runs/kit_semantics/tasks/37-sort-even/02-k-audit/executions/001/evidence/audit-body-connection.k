requires "verification-body-mutated.k"

module AUDIT-BODY-CONNECTION
  imports VERIFICATION-NO-BRIDGE

  // Bridge-free universal connection theorem for the exact operational rule
  // in module VERIFICATION.
  claim [loop-connection]:
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
        -1 |-> B:Scope )
      =>
      ( 0 |-> scope(
          "sort_even" |-> closureVal("l", sortEvenBody, 0),
          parent(-1))
        -1 |-> B )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap>
      ( 0 |-> list(
          CUR
          => fillEven(
               CUR,
               SORTED,
               I,
               C))
        1 |-> list(SLICE)
        2 |-> list(SORTED) )
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
endmodule
