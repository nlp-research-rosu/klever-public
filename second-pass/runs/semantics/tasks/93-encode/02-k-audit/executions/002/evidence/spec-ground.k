requires "verification.k"

module ENCODE-GROUND-SPEC
  imports ENCODE-VERIFICATION

  // Ground instance "aZ" -> "Cz" of the end-to-end theorem.
  claim [encode-ground-aZ]:
    <k>
      Call(
        closureVal(
          ("message", .ParamNames),
          encodeFunctionBody,
          0),
        (str(iCons(97, iCons(90, .IntSeq))), .Exprs))
      =>
      str(iCons(67, iCons(122, .IntSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
