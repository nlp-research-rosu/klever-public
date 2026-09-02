requires "connection-verification.k"

module MAX-ELEMENT-CONNECTION-SPEC
  imports MAX-ELEMENT-CONNECTION-VERIFICATION

  // Fixed #iterNext semantics over ordinary .ValSeq/vCons only.
  claim [expanded-max-acc]:
    <k> #maxAcc(list(expandIntVals(REST:IntSeq)), ACC:Int) ~> CONT:K
      => connectionMaxOf(ACC, REST) ~> CONT </k>

  // Exact submitted body on an ordinary vCons list representation.
  claim [expanded-universal-entry]:
    <k> #loadAll(connectionProgram)
         ~> Call(Name("max_element"),
                 (list(vCons(FIRST:Int, expandIntVals(REST:IntSeq))), .Exprs))
      => connectionMaxOf(FIRST, REST) </k>
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
