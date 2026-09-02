requires "verification.k"

module GROUND-MAIN-WITNESSES
  imports X-OR-Y-SUMMARY

  claim
    <k> #xOrY(1, 7, 9) => 9 </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(main_n1)]

  claim
    <k> #xOrY(2, 11, 13) => 11 </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(main_n2)]

  claim
    <k> #xOrY(7, 34, 12) => 34 </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(main_n7)]

  claim
    <k> #xOrY(15, 8, 5) => 5 </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(main_n15)]
endmodule

module GROUND-LOOP-WITNESS
  imports X-OR-Y-VERIFICATION

  claim
    <k>
      #loop(rangeObj(2, 9, 1), Name("divisor"), xOrYLoopBody)
      ~> (Return(Name("x")) .Stmts)
      ~> #endcall
      => #pop
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
      1 |-> scope(
        "divisor" |-> (99 => 3)
        "n" |-> 9
        "x" |-> 91
        "y" |-> 92,
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet => retV(92) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(loop_n9)]
endmodule
