requires "/tmp/audit-work/86-anti-shuffle/verification.k"

module AUDIT-VACUITY
  imports VERIFICATION

  // Satisfiable initial state; false obligation: anti_shuffle("") is not "!".
  claim [false-empty-result]:
    <k> FuncDef("anti_shuffle", Params("s"), antiBody)
        ~> Call(Name("anti_shuffle"), str(.IntSeq))
        => str(iCons(33, .IntSeq)) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALNEXT:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
