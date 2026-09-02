requires "verification.k"

module FRESH-VACUITY-SPEC
  imports VERIFICATION-WITH-LOOP

  // Fresh false mutation. The empty input satisfies positiveIntSeq, and both
  // Python implementations return an empty list. This mutation instead
  // requires the accumulated and returned lists to contain 1.
  claim [empty-returns-one]:
    <k> #loadAll(uniqueDigitsModule)
        ~> Call(Name("unique_digits"), (list(intsToVals(.IntSeq)), .Exprs))
        => ref(1) </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope("unique_digits" |-> uniqueDigitsClosure, parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => (0 |-> list(vCons(1, .ValSeq))
          1 |-> list(sortVS(vCons(1, .ValSeq))))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
