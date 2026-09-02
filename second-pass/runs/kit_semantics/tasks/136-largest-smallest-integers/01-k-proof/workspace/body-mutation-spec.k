requires "body-mutation.k"

module BODY-MUTATION-SPEC
  imports BODY-MUTATION

  // The mutated body returns (-3, None), so the correct (-1, None)
  // postcondition must not close.
  claim [mutated-body-rejected]:
    <k>
      #loadAll(Module(
        FuncDef(
          "largest_smallest_integers",
          Params("lst"),
          lsiMutantBody)))
      ~> Call(
           Name("largest_smallest_integers"),
           (list(vCons(-3, vCons(-1, .ValSeq))), .Exprs))
      => tuple(vCons(-1, vCons(noneV, .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "largest_smallest_integers"
           |-> closureVal(("lst", .ParamNames), lsiMutantBody, 0),
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
