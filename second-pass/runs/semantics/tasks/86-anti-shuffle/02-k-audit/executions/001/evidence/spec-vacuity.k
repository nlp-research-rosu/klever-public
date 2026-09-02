requires "verification.k"

module SPEC-VACUITY
  imports ANTI-SHUFFLE-VERIFICATION

  // False for the satisfiable input "ba": the real and claimed result is "ab",
  // not the empty string.
  claim [anti-shuffle-false-empty]:
    <k>
      Call(
        closureVal(("s", .ParamNames), antiBody, 0),
        (str(iCons(98, iCons(97, .IntSeq))), .Exprs))
      =>
      str(.IntSeq)
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
