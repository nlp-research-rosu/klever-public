requires "body-mutant.k"

module SPEC-BODY-MUTANT
  imports BODY-MUTANT

  // The mutant appends "bcd" unconditionally, so the original filtered
  // postcondition must be rejected.
  claim [unconditional-append-mutant]:
    <k>
      #loadAll(filterByPrefixMutantProgram)
      ~> Call(
           Name("filter_by_prefix"),
           list(
             vCons(
               str(strToCodes("abc")),
               vCons(
                 str(strToCodes("bcd")),
                 .ValSeq))),
           str(strToCodes("a")))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             .Map
             => "filter_by_prefix" |->
                  closureVal(
                    ("strings", "prefix"),
                    mutantFunctionBody,
                    0),
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(
           vCons(
             str(strToCodes("abc")),
             .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
