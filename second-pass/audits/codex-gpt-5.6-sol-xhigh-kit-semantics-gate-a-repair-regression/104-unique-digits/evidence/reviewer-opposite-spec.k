requires "audit-verification.k"

module REVIEWER-OPPOSITE-SPEC
  imports AUDIT-VERIFICATION

  claim [wrong-one-false]:
    <k> #while(udDigitCondition, udDigitBody) => .K </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
            "x"      |-> list(XS:ValSeq)
            "result" |-> ref(RH:Int)
            "value"  |-> W:Val
            "number" |-> (1 => 0)
            "valid"  |-> (true => false),
            parent(0))
      ...
    </scopes>
endmodule
