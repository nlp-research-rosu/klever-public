requires "verification.k"

module REVIEWER-NONVACUITY-SPEC
  imports MAX-FILL-VERIFICATION

  // Fresh false result mutation.  The precondition is realizable: [[1]] is a
  // binary one-row grid and capacity 1 is positive.  The real result is 1.
  claim [false-off-by-one-result]:
    <k> Call(
          Name("max_fill"),
          list(vCons(list(vCons(1, .ValSeq)), .ValSeq)),
          1)
          => 2 </k>
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
