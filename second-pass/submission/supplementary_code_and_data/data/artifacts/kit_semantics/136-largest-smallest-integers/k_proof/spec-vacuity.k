requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // False for the satisfiable input [-1]: the real result is (-1, None).
  claim [false-result]:
    <k>
      #loadAll(Module(
        FuncDef("largest_smallest_integers", Params("lst"), lsiBody)))
      ~> Call(
           Name("largest_smallest_integers"),
           (list(intVals(iCons(-1, .IntSeq))), .Exprs))
      => tuple(vCons(noneV, vCons(noneV, .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "largest_smallest_integers"
           |-> closureVal(("lst", .ParamNames), lsiBody, 0),
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
