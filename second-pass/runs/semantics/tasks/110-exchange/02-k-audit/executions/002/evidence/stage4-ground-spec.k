requires "verification.k"

module STAGE4-GROUND-SPEC
  imports EXCHANGE-VERIFICATION

  claim [ground-yes]:
    <k>
      #loadAll(Module(exchangeDef))
      ~> Call(
           Name("exchange"),
           ( list(intVals(iCons(1, .IntSeq)))
           , list(intVals(iCons(2, .IntSeq)))
           , .Exprs))
      =>
      str(iCons(89, iCons(69, iCons(83, .IntSeq))))
    </k>
    <env> 0 </env>
    <scopes>
      ( 0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope )
      =>
      ?FINALSCOPESYES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [ground-no]:
    <k>
      #loadAll(Module(exchangeDef))
      ~> Call(
           Name("exchange"),
           ( list(intVals(iCons(1, iCons(3, .IntSeq))))
           , list(intVals(iCons(2, .IntSeq)))
           , .Exprs))
      =>
      str(iCons(78, iCons(79, .IntSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      ( 0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope )
      =>
      ?FINALSCOPESNO:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
