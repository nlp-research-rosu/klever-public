requires "verification.k"

module SPEC-AUDITOR-VACUITY
  imports EXCHANGE-VERIFICATION

  // Deliberately false: exchange([1], [2]) has one odd element in the first
  // list and one even element in the second list, so the real result is YES.
  claim [false-ground-result]:
    <k>
      #loadAll(Module(exchangeDef))
      ~> Call(
           Name("exchange"),
           ( list(intVals(iCons(1, .IntSeq)))
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
