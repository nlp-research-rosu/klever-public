requires "verification.k"

module AUDIT-STANDARD-LIST-WITNESS
  imports DOUBLE-THE-DIFFERENCE-VERIFICATION

  // Same mixed sequence as audit-witness.k, now represented with the fixed
  // semantics' ordinary .ValSeq/vCons constructors rather than numVals.
  claim [entry-standard-list-witness]:
    <k>
      Call(
        Name("double_the_difference"),
        list(
          vCons(3.0,
          vCons(3,
          vCons(-5,
          vCons(2.5,
          vCons(7, .ValSeq)))))))
      => 58
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "double_the_difference" |->
          closureVal(
            "lst",
            Assign(Name("total"), Int(0))
            Assign(Name("number"), Int(0))
            For(
              Name("number"),
              Name("lst"),
              If(
                BoolOp(
                  "and",
                  Call(
                    Name("isinstance"),
                    Name("number"),
                    Name("int")),
                  Compare(
                    Name("number"),
                    CmpOp(">", Int(0))),
                  Compare(
                    BinOp("%", Name("number"), Int(2)),
                    CmpOp("==", Int(1)))),
                AugAssign(
                  Name("total"),
                  "+",
                  BinOp("**", Name("number"), Int(2))),
                .Stmts))
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
