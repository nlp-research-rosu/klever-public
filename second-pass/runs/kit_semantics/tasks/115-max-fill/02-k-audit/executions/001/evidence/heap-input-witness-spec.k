requires "verification.k"

module REVIEWER-HEAP-INPUT-WITNESS-SPEC
  imports MAX-FILL-VERIFICATION

  // A normal source ListExpr allocates rows and the outer grid as heap
  // objects.  This ground state models [[1]] after those allocations and
  // checks the supplied dereference paths through For and sum.
  claim [heap-backed-grid]:
    <k> Call(Name("max_fill"), ref(1), 1) => 1 </k>
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
    <heap>
      0 |-> list(vCons(1, .ValSeq))
      1 |-> list(vCons(ref(0), .ValSeq))
    </heap>
    <heapLoc> 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
