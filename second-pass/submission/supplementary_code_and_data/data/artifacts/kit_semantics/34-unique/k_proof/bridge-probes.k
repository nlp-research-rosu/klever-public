requires "verification.k"

module MEMBER-PROBE-BASE
  imports VERIFICATION-BASE

  claim [present-continuation]:
    <k>
      #memberAcc(
        2,
        list(vCons(1, vCons(2, vCons(3, .ValSeq)))))
      ~> #notB
      => false
    </k>

  claim [absent-continuation]:
    <k>
      #memberAcc(
        4,
        list(vCons(1, vCons(2, vCons(3, .ValSeq)))))
      ~> #notB
      => true
    </k>
endmodule

module MEMBER-PROBE-BRIDGED
  imports VERIFICATION-MEMBER

  claim [present-continuation]:
    <k>
      #memberAcc(
        2,
        list(vCons(1, vCons(2, vCons(3, .ValSeq)))))
      ~> #notB
      => false
    </k>

  claim [absent-continuation]:
    <k>
      #memberAcc(
        4,
        list(vCons(1, vCons(2, vCons(3, .ValSeq)))))
      ~> #notB
      => true
    </k>
endmodule

module LOOP-PROBE-FIXED
  imports VERIFICATION-MEMBER

  claim [observable-continuation]:
    <k>
      #loop(
        list(vCons(2, vCons(1, vCons(2, .ValSeq)))),
        Name("x"),
        If(
          Compare(Name("x"), CmpOp("not in", Name("result"))),
          Expr(Call(Attribute(Name("result"), "append"), Name("x"))),
          .Stmts))
      ~> Assign(Name("x"), Int(99))
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        ("l" |-> ref(0))
        ("result" |-> ref(1))
        ("x" |-> (noneV => 99)),
        parent(0))
    </scopes>
    <heap>
      1 |-> list(
        .ValSeq
        => vCons(2, vCons(1, .ValSeq)))
    </heap>
endmodule

module LOOP-PROBE-BRIDGED
  imports VERIFICATION

  claim [observable-continuation]:
    <k>
      #loop(
        list(vCons(2, vCons(1, vCons(2, .ValSeq)))),
        Name("x"),
        If(
          Compare(Name("x"), CmpOp("not in", Name("result"))),
          Expr(Call(Attribute(Name("result"), "append"), Name("x"))),
          .Stmts))
      ~> Assign(Name("x"), Int(99))
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        ("l" |-> ref(0))
        ("result" |-> ref(1))
        ("x" |-> (noneV => 99)),
        parent(0))
    </scopes>
    <heap>
      1 |-> list(
        .ValSeq
        => vCons(2, vCons(1, .ValSeq)))
    </heap>
endmodule
