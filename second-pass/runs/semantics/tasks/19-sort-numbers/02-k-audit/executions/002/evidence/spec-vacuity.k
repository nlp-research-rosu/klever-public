requires "verification.k"

module SORT-NUMBERS-SPEC-VACUITY
  imports SORT-NUMBERS-VERIFICATION

  // Fresh audit mutation: the real helper returns 0 on the satisfiable input
  // "zero", so demanding 1 must leave a semantic result mismatch.
  claim [number-value-zero-false]:
    <k> #loadAll(solutionModule)
        ~> Call(Name("number_value"), Str("zero"))
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
endmodule
