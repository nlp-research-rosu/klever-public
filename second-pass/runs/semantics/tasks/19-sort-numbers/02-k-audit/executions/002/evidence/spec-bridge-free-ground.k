requires "verification-bridge-free.k"

module SORT-NUMBERS-BRIDGE-FREE-GROUND-SPEC
  imports SORT-NUMBERS-BRIDGE-FREE

  claim [bridge-free-empty]:
    <k> #loadAll(solutionModule)
        ~> Call(Name("sort_numbers"), str(encodedWords(.NumWords)))
        => numericOutput(.NumWords) </k>
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

  claim [bridge-free-example]:
    <k> #loadAll(solutionModule)
        ~> Call(
             Name("sort_numbers"),
             str(encodedWords(
               nw(threeW, nw(oneW, nw(fiveW, .NumWords))))))
        => numericOutput(
             nw(threeW, nw(oneW, nw(fiveW, .NumWords)))) </k>
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
