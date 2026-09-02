requires "verification.k"

module SORT-NUMBERS-SPEC-VACUITY-MAIN
  imports SORT-NUMBERS-VERIFICATION

  // The satisfying concrete substitution is WORDS =
  // nw(threeW,nw(oneW,nw(fiveW,.NumWords))). Both Python implementations
  // return "one three five", so the reversed target below is deliberately false.
  claim [sort-numbers-example-false]:
    <k> #loadAll(solutionModule)
        ~> Call(
             Name("sort_numbers"),
             str(encodedWords(
               nw(threeW, nw(oneW, nw(fiveW, .NumWords))))))
        => str(strToCodes("five three one")) </k>
    <env> 0 </env>
    <scopes> (0 |-> scope(.Map, parent(-1)))
             (-1 |-> builtinsScope) => ?_:Map </scopes>
    <scopeLoc> 1 => ?_:Int </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <stack> .List => ?_:List </stack>
    <ret> noRet => ?_:RetState </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
