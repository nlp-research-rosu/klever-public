requires "verification.k"

module AUDIT-BRIDGE-CONTINUATION
  imports FACTORIZE-VERIFICATION

  // A concrete loop followed by an observable scope update. The same claim is
  // run once with only fixed semantics and once with the promoted loop rule.
  claim [loop-preserves-continuation]:
    <k>
      #while(Compare(Name("n"), CmpOp(">", Int(1))), factorizeStep)
      ~> Assign(Name("after"), Int(99))
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        ("n" |-> 4
         "divisor" |-> 2
         "factors" |-> ref(0)),
        parent(0))
      =>
      1 |-> scope(
        ("n" |-> 1
         "divisor" |-> 2
         "factors" |-> ref(0)
         "after" |-> 99),
        parent(0))
    </scopes>
    <heap>
      0 |-> list(.ValSeq)
      =>
      0 |-> list(vCons(2, vCons(2, .ValSeq)))
    </heap>
endmodule
