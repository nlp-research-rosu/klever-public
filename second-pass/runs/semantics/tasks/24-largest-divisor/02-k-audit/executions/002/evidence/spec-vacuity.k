requires "spec.k"

module SPEC-VACUITY
  imports LOOP-SPEC

  // Fresh false-result mutation.  The submitted program and its exact body
  // macro are unchanged; only the correct result 5 for satisfying input n=15
  // is changed to the demonstrably false result 6.
  claim
    <k>
      #loadAll(
        Module(
          FuncDef(
            "largest_divisor",
            Params("n"),
            largestDivisorBody())))
      ~> Call(Name("largest_divisor"), Int(15))
      =>
      6 ~> .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "largest_divisor" |->
          closureVal("n", largestDivisorBody(), 0),
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
    [label(falseResultAtSatisfyingInput)]
endmodule
