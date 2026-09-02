requires "verification.k"

module FILTER-SPEC-ENTRY-ONLY
  imports FILTER-VERIFICATION

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
