requires "verification.k"

module AUDIT-FRESH-VACUITY
  imports VERIFICATION

  // Deliberately false result mutation. For the satisfying primary-entry
  // witness VS=[2,3,4,5,2], H=0, HEAP=.Map, NEXT=1, the actual result is 44,
  // while this claim requires 45.
  claim [wrong-result-45]:
    <k>
      #loadAll(Module(sumSquaresDef))
      ~> Call(Name("sum_squares"), ref(0))
      =>
      45
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?GLOBALS:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      0 |-> list(vCons(2, vCons(3, vCons(4, vCons(5, vCons(2, .ValSeq))))))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
