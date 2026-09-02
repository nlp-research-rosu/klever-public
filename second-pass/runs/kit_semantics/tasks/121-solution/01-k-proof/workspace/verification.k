requires "verification-base.k"

module VERIFICATION
  imports VERIFICATION-BASE

  // Exact loop-only bridge justified independently by CONNECTION-SPEC.loop.
  // The arbitrary continuation and omitted cells are equally general in that
  // bridge-free theorem and are preserved unchanged.
  rule
    <k>
      #loop(
        list(REST:ValSeq),
        Name("value"),
        If(
          Compare(
            BinOp("%", Name("position"), Int(2)),
            CmpOp("==", Int(0))
          ),
          If(
            Compare(
              BinOp("%", Name("value"), Int(2)),
              CmpOp("!=", Int(0))
            ),
            AugAssign(Name("result"), "+", Name("value")) .Stmts,
            .Stmts
          ) .Stmts,
          .Stmts
        )
        AugAssign(Name("position"), "+", Int(1)) .Stmts
      )
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "lst"      |-> list(ALL:ValSeq)
        "position" |-> (POSITION:Int => POSITION +Int vsLen(REST))
        "result"   |-> (ACC:Int => ACC +Int oddAtEvenSum(REST, POSITION))
        "value"    |-> (CURRENT:Val => lastAfter(REST, CURRENT)),
        PARENT:Parent
      )
      ...
    </scopes>
    requires allInts(REST) andBool POSITION >=Int 0
    [priority(40)]
endmodule
