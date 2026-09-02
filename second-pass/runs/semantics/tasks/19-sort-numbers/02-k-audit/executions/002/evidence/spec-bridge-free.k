requires "verification-bridge-free.k"

module SORT-NUMBERS-BRIDGE-FREE-SPEC
  imports SORT-NUMBERS-BRIDGE-FREE

  claim [number-value-zero]:
    <k> #loadAll(solutionModule)
        ~> Call(Name("number_value"), Str("zero"))
        => 0 </k>
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

  claim [number-value-one]:
    <k> #loadAll(solutionModule)
        ~> Call(Name("number_value"), Str("one"))
        => 1 </k>
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

  claim [number-value-two]:
    <k> #loadAll(solutionModule)
        ~> Call(Name("number_value"), Str("two"))
        => 2 </k>
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

  claim [number-value-three]:
    <k> #loadAll(solutionModule)
        ~> Call(Name("number_value"), Str("three"))
        => 3 </k>
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

  claim [number-value-four]:
    <k> #loadAll(solutionModule)
        ~> Call(Name("number_value"), Str("four"))
        => 4 </k>
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

  claim [number-value-five]:
    <k> #loadAll(solutionModule)
        ~> Call(Name("number_value"), Str("five"))
        => 5 </k>
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

  claim [number-value-six]:
    <k> #loadAll(solutionModule)
        ~> Call(Name("number_value"), Str("six"))
        => 6 </k>
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

  claim [number-value-seven]:
    <k> #loadAll(solutionModule)
        ~> Call(Name("number_value"), Str("seven"))
        => 7 </k>
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

  claim [number-value-eight]:
    <k> #loadAll(solutionModule)
        ~> Call(Name("number_value"), Str("eight"))
        => 8 </k>
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

  claim [number-value-nine]:
    <k> #loadAll(solutionModule)
        ~> Call(Name("number_value"), Str("nine"))
        => 9 </k>
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

  // WORDS ranges over arbitrary-length sequences containing only valid
  // numeral words. MPY-SORT's sortKeyVS is the supplied trusted symbolic
  // semantics for keyed sorted().
  claim [sort-numbers-symbolic]:
    <k> #loadAll(solutionModule)
        ~> Call(Name("sort_numbers"), str(encodedWords(WORDS:NumWords)))
        => numericOutput(WORDS) </k>
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
