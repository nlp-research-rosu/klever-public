requires "verification.k"

module SPEC-VACUITY
  imports MAX-ELEMENT-VERIFICATION

  claim [max-acc]:
    <k> #maxAcc(list(intVals(REST:IntSeq)), ACC:Int) ~> CONT:K
      => maxOf(ACC, REST) ~> CONT </k>

  // False by one for every satisfying non-empty integer input.
  claim [false-universal-entry]:
    <k> #loadAll(maxElementProgram)
         ~> Call(Name("max_element"),
                 (list(vCons(FIRST:Int, intVals(REST:IntSeq))), .Exprs))
      => maxOf(FIRST, REST) +Int 1 </k>
    <env> 0 </env>
    <scopes> (0 |-> scope(.Map, parent(-1))
              -1 |-> builtinsScope)
          => ?FINALSCOPES:Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
