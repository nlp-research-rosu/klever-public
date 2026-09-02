requires "verification.k"

module REVIEWER-BODY-MUTATION-SPEC
  imports MAX-FILL-VERIFICATION

  // The executed closure body itself is changed: total starts at 1.  On the
  // empty-grid extension it returns 1, contradicting the original result 0.
  claim [mutated-executed-body]:
    <k> Call(Name("max_fill"), list(.ValSeq), 1) => 0 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "max_fill" |->
          closureVal(
            ("grid", "capacity"),
            Assign(Name("total"), Int(1))
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
