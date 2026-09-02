requires "spec.k"

module SPEC-GROUND-WITNESS
  imports MAX-FILL-VERIFICATION

  // Realizable contract input: grid [[1]], capacity 2. Python returns 1.
  claim [one-cell-capacity-two]:
    <k> #runMaxFill(gCons(iCons(1, .IntSeq), .GridRows), 2)
      => 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
