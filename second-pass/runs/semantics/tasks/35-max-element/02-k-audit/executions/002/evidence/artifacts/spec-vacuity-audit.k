requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports MAX-ELEMENT-VERIFICATION

  // Fresh false result obligation. Witness:
  // FIRST=1, REST=iCons(2,iCons(3,.IntSeq)); actual maximum is 3, target is 4.
  claim
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
