requires "verification.k"

module AUDIT-END-TO-END
  imports VERIFICATION

  claim
    <k>
      #while(
        Compare(
          BinOp("%", Name("n"), Name("divisor")),
          CmpOp("!=", Int(0))),
        AugAssign(Name("divisor"), "-", Int(1)))
      ~> Return(Name("divisor")) .Stmts
      ~> #endcall
      => firstDivisorAtOrBelow(N, D) ~> .K
    </k>
    <env> 1 => 0 </env>
    <scopes>
      SC:Map
      1 |-> scope(
        "n" |-> N
        "divisor" |-> D,
        parent(0))
      =>
      SC
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >Int 1 andBool D >=Int 1 andBool D <Int N
    [label(auditLoop)]

  claim
    <k>
      #loadAll(
        Module(
          FuncDef(
            "largest_divisor",
            Params("n"),
            largestDivisorBody())))
      ~> Call(Name("largest_divisor"), Int(N))
      =>
      largestProperDivisor(N) ~> .K
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
    requires N >Int 1
    [label(auditEntry)]
endmodule
