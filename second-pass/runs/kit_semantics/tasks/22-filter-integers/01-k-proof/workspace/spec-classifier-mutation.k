requires "verification.k"

module SPEC-CLASSIFIER-MUTATION
  imports VERIFICATION

  // Deliberately false opposite interpretation: integer 1 is discarded.
  claim [integer-discarded]:
    <k>
      Call(
        Name("filter_integers"),
        (list(vCons(1, .ValSeq)), .Exprs))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "filter_integers" |->
          closureVal(("values", .ParamNames), filterBody, 0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
