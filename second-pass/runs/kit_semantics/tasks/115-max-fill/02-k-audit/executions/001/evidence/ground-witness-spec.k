requires "verification.k"

module REVIEWER-GROUND-WITNESS-SPEC
  imports MAX-FILL-VERIFICATION

  claim [formal-precondition-and-summary]:
    <k> .K => .K </k>
    ensures
      allRows(vCons(list(vCons(1, .ValSeq)), .ValSeq))
      andBool gridCost(
        vCons(list(vCons(1, .ValSeq)), .ValSeq),
        1) ==Int 1

  claim [ground-entry-execution]:
    <k> Call(
          Name("max_fill"),
          list(vCons(list(vCons(1, .ValSeq)), .ValSeq)),
          1)
          => 1 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "max_fill" |->
          closureVal(
            ("grid", "capacity"),
            Assign(Name("total"), Int(0))
            Assign(Name("row"), Int(0))
            For(
              Name("row"),
              Name("grid"),
              AugAssign(
                Name("total"),
                "+",
                BinOp(
                  "//",
                  BinOp(
                    "-",
                    BinOp(
                      "+",
                      Call(Name("sum"), Name("row")),
                      Name("capacity")),
                    Int(1)),
                  Name("capacity"))))
            Return(Name("total")),
            0),
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
endmodule
