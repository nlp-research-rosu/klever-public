requires "verification.k"

module STAGE4-GROUND-SPEC
  imports ANTI-SHUFFLE-VERIFICATION

  // Satisfying instance of the entry claim: s = "ba a", result = "ab a".
  claim [ground-ba-a]:
    <k>
      Call(
        closureVal(("s", .ParamNames), antiBody, 0),
        (str(
          iCons(98,
          iCons(97,
          iCons(32,
          iCons(97, .IntSeq))))),
         .Exprs))
      =>
      str(
        iCons(97,
        iCons(98,
        iCons(32,
        iCons(97, .IntSeq)))))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?HFINAL:Map </heap>
    <heapLoc> 0 => ?NFINAL:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
