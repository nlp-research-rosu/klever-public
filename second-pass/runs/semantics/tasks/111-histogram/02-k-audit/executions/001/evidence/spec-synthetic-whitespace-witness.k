requires "verification.k"

module SYNTHETIC-WHITESPACE-WITNESS
  imports VERIFICATION

  // A is the concrete code sequence for "a b". The synthetic split abstraction
  // treats the whole whitespace-containing A as one token.
  claim
    <k>
      #loadAll(histogramCheck(
        str(tokenText(vCons(
          str(iCons(97, iCons(32, iCons(98, .IntSeq)))),
          .ValSeq))),
        DictExpr(Entry(
          str(iCons(97, iCons(32, iCons(98, .IntSeq)))),
          Int(1)))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
