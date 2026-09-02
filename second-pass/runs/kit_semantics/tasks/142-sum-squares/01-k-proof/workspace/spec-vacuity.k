requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the empty-list result is 0, not 1.
  claim [wrong-result]:
    <k>
      #loadAll(Module(sumSquaresDef))
      ~> Call(Name("sum_squares"), ref(0))
      =>
      1
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?GLOBALS:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> 0 |-> list(.ValSeq) </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
