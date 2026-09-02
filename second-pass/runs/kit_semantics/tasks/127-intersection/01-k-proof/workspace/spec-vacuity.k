requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: these intervals intersect in length 2, so the real
  // result is "YES", not "NO".
  claim [wrong-prime-result]:
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("intersection"),
              TupleExpr(Int(-3), Int(-1)),
              TupleExpr(Int(-5), Int(5)))
      => str(strToCodes("NO"))
    </k>
    <env> 0 </env>
    <scopes>
      (0  |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
