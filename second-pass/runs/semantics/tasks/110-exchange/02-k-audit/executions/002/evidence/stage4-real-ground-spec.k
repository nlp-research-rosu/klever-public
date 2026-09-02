requires "verification.k"

module STAGE4-REAL-GROUND-SPEC
  imports EXCHANGE-VERIFICATION

  claim [real-ground-yes]:
    <k>
      #loadAll(Module(exchangeDef))
      ~> Call(
           Name("exchange"),
           ( list(vCons(1, .ValSeq))
           , list(vCons(2, .ValSeq))
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

  claim [real-ground-no]:
    <k>
      #loadAll(Module(exchangeDef))
      ~> Call(
           Name("exchange"),
           ( list(vCons(1, vCons(3, .ValSeq)))
           , list(vCons(2, .ValSeq))
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
