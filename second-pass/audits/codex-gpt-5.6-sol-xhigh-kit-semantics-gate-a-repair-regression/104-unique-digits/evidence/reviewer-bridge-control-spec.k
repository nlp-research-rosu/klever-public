requires "audit-verification.k"

module REVIEWER-BRIDGE-CONTROL-SPEC
  imports AUDIT-VERIFICATION

  claim [one-true-continuation]:
    <k>
      #while(udDigitCondition, udDigitBody)
      ~> Assign(Name("value"), Int(7))
      => .K
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
            "x"      |-> list(XS:ValSeq)
            "result" |-> ref(RH:Int)
            "value"  |-> (_W:Val => 7)
            "number" |-> (1 => 0)
            "valid"  |-> (true => true),
            parent(0))
      ...
    </scopes>

  claim [two-false-continuation]:
    <k>
      #while(udDigitCondition, udDigitBody)
      ~> Assign(Name("value"), Int(7))
      => .K
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
            "x"      |-> list(XS:ValSeq)
            "result" |-> ref(RH:Int)
            "value"  |-> (_W:Val => 7)
            "number" |-> (2 => 0)
            "valid"  |-> (true => false),
            parent(0))
      ...
    </scopes>

  claim [assignment-projection-continuation]:
    <k>
      Assign(Name("number"), Int(7))
      ~> Assign(Name("value"), Int(8))
      => .K
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
            "x"      |-> list(XS:ValSeq)
            "result" |-> ref(RH:Int)
            "value"  |-> (_W:Val => 8)
            "number" |-> (_OLD:Val => 7)
            "valid"  |-> B:Bool,
            parent(0))
      ...
    </scopes>
endmodule
