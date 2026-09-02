requires "verification.k"

module AUDIT-FALSE-RESULT
  imports VERIFICATION

  // Fresh audit mutation: the real loop returns firstDivisorAtOrBelow(N,D),
  // while this destination demands an off-by-one result.
  claim
    <k>
      #while(
        Compare(
          BinOp("%", Name("n"), Name("divisor")),
          CmpOp("!=", Int(0))),
        AugAssign(Name("divisor"), "-", Int(1)))
      ~> Return(Name("divisor")) .Stmts
      ~> #endcall
      => (firstDivisorAtOrBelow(N, D) +Int 1) ~> .K
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
    [label(auditFalseResult)]
endmodule
