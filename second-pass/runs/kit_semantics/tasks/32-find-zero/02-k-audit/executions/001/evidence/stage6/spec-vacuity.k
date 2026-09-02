requires "spec.k"

module SPEC-AUDIT-VACUITY
  imports SPEC-CONNECTION

  // Fresh audit mutation: the real bisection execution returns
  // bisectFrom(NS,B,E), not that result plus 1.0.
  claim [wrong-bisect-result]:
    <k>
      #while(bisectCond, bisectBody)
      ~> (Return(Name("begin")) .Stmts)
      ~> #endcall
      => addF(bisectFrom(NS, B, E), 1.0)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope(
        .Map
          [ "poly" <- closureVal(("xs", "x"), polyBody, 0) ]
          [ "find_zero" <- closureVal("xs", findZeroBody, 0) ],
        parent(-1)))
      (-1 |-> builtinsScope)
      (1 |-> scope(
        .Map
          [ "xs" <- list(numVals(NS:NumSeq)) ]
          [ "begin" <- B:Float ]
          [ "end" <- E:Float ]
          [ "center" <- C:Float ],
        parent(0)))
      =>
         (0 |-> scope(
           .Map
             [ "poly" <- closureVal(("xs", "x"), polyBody, 0) ]
             [ "find_zero" <- closureVal("xs", findZeroBody, 0) ],
           parent(-1)))
         (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP </heap>
    <heapLoc> HL </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      => .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires validCoeffs(NS)
endmodule
