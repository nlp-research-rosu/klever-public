requires "verification.k"

module DIGIT-SUM-GROUND-SPEC
  imports DIGIT-SUM-VERIFICATION

  claim [ground-empty]:
    <k> digitSumSpec(.IntSeq) => 0 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> digitSumBuiltins
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [ground-abAB]:
    <k>
      digitSumSpec(
        iCons(97, iCons(98, iCons(65, iCons(66, .IntSeq))))
      ) => 131
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> digitSumBuiltins
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [ground-non-ascii-uppercase]:
    <k> digitSumSpec(iCons(201, .IntSeq)) => 0 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> digitSumBuiltins
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
