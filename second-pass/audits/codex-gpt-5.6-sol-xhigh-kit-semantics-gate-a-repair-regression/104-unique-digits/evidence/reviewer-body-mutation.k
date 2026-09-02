requires "connection-verification.k"

module REVIEWER-BODY-MUTATION
  imports CONNECTION-VERIFICATION

  // Fresh body-sensitivity mutation: test for an even digit instead of an odd
  // digit. For N=1 this computes false, while allOddResult(1) is true.
  claim [inverted-parity-test]:
    <k>
      #while(
        udDigitCondition,
        Assign(
          Name("valid"),
          BoolOp(
            "and",
            (Name("valid"),
             Compare(
               BinOp("%", Name("number"), Int(2)),
               CmpOp("==", Int(0))))))
        Assign(
          Name("number"),
          BinOp("//", Name("number"), Int(10))))
      => .K
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
            "x"      |-> list(XS:ValSeq)
            "result" |-> ref(RH:Int)
            "value"  |-> W:Val
            "number" |-> (1 => 0)
            "valid"  |-> (true => allOddResult(1)),
            parent(0))
      ...
    </scopes>
endmodule
