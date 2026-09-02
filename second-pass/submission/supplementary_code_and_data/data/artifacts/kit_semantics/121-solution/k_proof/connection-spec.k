requires "verification-base.k"

module CONNECTION-SPEC
  imports VERIFICATION-BASE

  claim [loop]:
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
endmodule
