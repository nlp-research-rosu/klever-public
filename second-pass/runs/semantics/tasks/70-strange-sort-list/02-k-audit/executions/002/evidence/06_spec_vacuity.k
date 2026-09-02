requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // AUDITOR MUTATION: the returned list is falsely required to be empty for
  // every INPUT.  INPUT=vCons(1,.ValSeq) is a satisfying counterexample.
  claim [false-empty-result]:
    <k>
      Call(
        closureVal(("lst", .ParamNames), strangeBody(), 0),
        list(INPUT:ValSeq))
      =>
      ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(sortVS(INPUT))
      1 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
