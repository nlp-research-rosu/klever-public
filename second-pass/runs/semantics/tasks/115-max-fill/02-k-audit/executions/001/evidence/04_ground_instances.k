requires "verification.k"

module MAX-FILL-GROUND-INSTANCES
  imports MAX-FILL-VERIFICATION

  claim [ground-empty]:
    <k> #runMaxFill(.GridRows, 1) => 0 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?FINALSCOPES0:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [ground-single-one]:
    <k> #runMaxFill(gCons(iCons(1, .IntSeq), .GridRows), 1) => 1 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?FINALSCOPES1:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // [[1,1,1], [0,1,0]] with capacity 2: ceil(3/2)+ceil(1/2)=3.
  claim [ground-two-rows]:
    <k>
      #runMaxFill(
        gCons(
          iCons(1, iCons(1, iCons(1, .IntSeq))),
          gCons(iCons(0, iCons(1, iCons(0, .IntSeq))), .GridRows)),
        2)
      => 3
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?FINALSCOPES2:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
