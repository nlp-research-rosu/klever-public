requires "verification.k"

module AUDITOR-VACUITY
  imports VERIFICATION

  // Fresh false mutation: prefix code 90 to the actual symbolic result.
  // The empty-input witness should return .IntSeq, not iCons(90, .IntSeq).
  claim [false-prefixed-result]:
    <k>
      #loadAll(solutionModule())
      ~> Call(Name("anti_shuffle"), str(INPUT:IntSeq), .Exprs)
      => str(iCons(90, antiGo(INPUT, .IntSeq, .IntSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
             "anti_shuffle" |->
               closureVal(("s", .ParamNames), solutionBody(), 0),
             parent(-1))
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
