requires "verification.k"

module FILTER-SPEC-LABELED
  imports FILTER-VERIFICATION

  claim [loop-target]:
    <k> #loop(list(strVals(SS:StrSeq)), Name("string"), filterLoopBody)
         ~> CONT:K
      => CONT
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        (.Map [ "strings" <- list(strVals(ORIG:StrSeq)) ]
              [ "substring" <- str(P:IntSeq) ]
              [ "result" <- ref(H:Int) ]
              [ "string" <- str(CUR:IntSeq) ])
        =>
        (.Map [ "strings" <- list(strVals(ORIG)) ]
              [ "substring" <- str(P) ]
              [ "result" <- ref(H) ]
              [ "string" <- str(lastCodes(CUR, SS)) ]),
        parent(0)) ...
    </scopes>
    <heap>
      ... H:Int |-> list(ACC:ValSeq
                         => filterAccStrings(ACC, P, SS)) ...
    </heap>

  claim [entry-target]:
    <k> #loadAll(filterProgram)
         ~> Call(Name("filter_by_substring"),
                 (list(strVals(SS:StrSeq)), str(P:IntSeq), .Exprs))
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
    <heap> .Map => (0 |-> list(filterStrings(P, SS))) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
