requires "verification.k"

module FILTER-SPEC-GROUND-WITNESS
  imports FILTER-VERIFICATION

  claim [documented-example]:
    <k> #loadAll(filterProgram)
         ~> Call(Name("filter_by_substring"),
                 (list(strVals(
                    ssCons(iCons(97, iCons(98, iCons(99, .IntSeq))),
                    ssCons(iCons(98, iCons(97, iCons(99, iCons(100, .IntSeq)))),
                    ssCons(iCons(99, iCons(100, iCons(101, .IntSeq))),
                    ssCons(iCons(97, iCons(114, iCons(114, iCons(97, iCons(121, .IntSeq))))),
                           .StrSeq)))))),
                  str(iCons(97, .IntSeq)), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(("filter_by_substring"
                    |-> closureVal(("strings", "substring"), filterBody, 0)),
                   parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
        vCons(str(iCons(97, iCons(98, iCons(99, .IntSeq)))),
        vCons(str(iCons(98, iCons(97, iCons(99, iCons(100, .IntSeq))))),
        vCons(str(iCons(97, iCons(114, iCons(114, iCons(97, iCons(121, .IntSeq)))))),
              .ValSeq))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
