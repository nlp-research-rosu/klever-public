requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: append code 1 to the proven return value.
  claim [anti-shuffle-false-result]:
    <k>
      #loadAll(solutionModule())
      ~> Call(Name("anti_shuffle"), str(INPUT:IntSeq), .Exprs)
      => str(
           seqConcat(
             antiGo(INPUT, .IntSeq, .IntSeq),
             iCons(1, .IntSeq)))
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
