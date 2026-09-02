requires "verification.k"

module AUDIT-GROUND-WITNESS
  imports VERIFICATION

  claim [ground-loop-state]:
    <k> #loop(
          list(wordVals(wCons(
            iCons(97, iCons(98, .IntSeq)),
            .WordSeq))),
          Name("word"),
          findMaxLoopBody)
         ~> .K
      => .K
    </k>
    <env> 1 </env>
    <scopes>
          1 |-> scope(
            ("words" |-> list(wordVals(
              wCons(iCons(98, iCons(97, .IntSeq)),
              wCons(iCons(97, iCons(98, .IntSeq)), .WordSeq)))))
            ("best" |-> str(iCons(98, iCons(97, .IntSeq))))
            ("max_unique" |-> 2)
            ("word" |-> str(iCons(98, iCons(97, .IntSeq))))
            ("unique" |-> 2),
            parent(0))
          0 |-> scope(
            "find_max" |->
              closureVal(
                ("words", .ParamNames),
                findMaxFunctionBody,
                0),
            parent(-1))
         -1 |-> builtinsScope
      =>
          1 |-> scope(
            ("words" |-> list(wordVals(
              wCons(iCons(98, iCons(97, .IntSeq)),
              wCons(iCons(97, iCons(98, .IntSeq)), .WordSeq)))))
            ("best" |-> str(iCons(97, iCons(98, .IntSeq))))
            ("max_unique" |-> 2)
            ("word" |-> str(iCons(97, iCons(98, .IntSeq))))
            ("unique" |-> 2),
            parent(0))
          0 |-> scope(
            "find_max" |->
              closureVal(
                ("words", .ParamNames),
                findMaxFunctionBody,
                0),
            parent(-1))
         -1 |-> builtinsScope
    </scopes>

  claim [ground-entry-state]:
    <k> #loadAll(Module(
         FuncDef("find_max", Params("words"), findMaxFunctionBody)))
         ~> Call(Name("find_max"), list(wordVals(
              wCons(iCons(98, iCons(97, .IntSeq)),
              wCons(iCons(97, iCons(98, .IntSeq)), .WordSeq)))))
      => str(iCons(97, iCons(98, .IntSeq)))
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
