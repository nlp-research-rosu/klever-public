requires "verification.k"

module GROUND-SPEC
  imports VERIFICATION

  // Satisfiable entry instance: input [-3, -1, 0, 4, 2].
  claim [mixed-input]:
    <k>
      #loadAll(Module(
        FuncDef("largest_smallest_integers", Params("lst"), lsiBody)))
      ~> Call(
           Name("largest_smallest_integers"),
           (list(intVals(
             iCons(-3, iCons(-1, iCons(0, iCons(4, iCons(2, .IntSeq))))))),
            .Exprs))
      => tuple(vCons(-1, vCons(2, .ValSeq)))
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
