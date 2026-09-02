requires "verification.k"

module BRIDGE-SENSITIVITY
  imports VERIFICATION

  // The submitted bridge must not match this materially changed loop body.
  // At LENGTH=3 and DIVISOR=2, the changed test (remainder == 1) returns NO,
  // whereas the submitted body and primeFrom(3,2) return YES.
  claim
    <k> #loop(rangeObj(2, 3, 1),
              Name("divisor"),
              If(Compare(BinOp("%", Name("length"), Name("divisor")),
                         CmpOp("==", Int(1))),
                 Return(Str("NO")) .Stmts,
                 .Stmts)
              .Stmts)
        ~> (Return(Str("YES")) .Stmts) ~> #endcall
      => yesV
    </k>
    <env> 1 => 0 </env>
    <scopes>
      SC:Map
      1 |-> scope(
        "interval1" |-> tuple(vCons(0, vCons(3, .ValSeq)))
        "interval2" |-> tuple(vCons(0, vCons(3, .ValSeq)))
        "left"      |-> 0
        "right"     |-> 3
        "length"    |-> 3
        "divisor"   |-> 2,
        parent(0))
      => SC
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    [label(changed-body-must-not-use-bridge)]

endmodule
