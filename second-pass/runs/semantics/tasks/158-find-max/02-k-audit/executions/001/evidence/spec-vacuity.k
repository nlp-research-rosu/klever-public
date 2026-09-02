requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: on the satisfying input ["a"], the real program returns
  // "a", but this mutation requires the empty string.
  claim [false-empty-result-for-a]:
    <k> #loadAll(Module(
         FuncDef("find_max", Params("words"), findMaxFunctionBody)))
         ~> Call(Name("find_max"), list(wordVals(
              wCons(iCons(97, .IntSeq), .WordSeq))))
      => str(.IntSeq)
    </k>
    <env> 0 </env>
    <scopes>
         0 |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope
      =>
         0 |-> scope(
                "find_max" |->
                  closureVal(
                    ("words", .ParamNames),
                    findMaxFunctionBody,
                    0),
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
