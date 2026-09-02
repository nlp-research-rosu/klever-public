requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false for the satisfiable empty-list input: the real result
  // is true, while this mutation requires false.
  claim [entry-false-empty]:
    <k>
      Call(
        Name("is_sorted"),
        list(.ValSeq))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "is_sorted" |->
          closureVal(
            "lst",
            Assign(
              Name("result"),
              Compare(
                Name("lst"),
                CmpOp(
                  "==",
                  Call(Name("sorted"), Name("lst")))))
            Assign(
              Name("previous"),
              TupleExpr(UnaryOp("-", Int(1))))
            Assign(Name("repeated"), Int(0))
            Assign(Name("value"), Int(0))
            For(
              Name("value"),
              Name("lst"),
              If(
                Compare(
                  TupleExpr(Name("value")),
                  CmpOp("==", Name("previous"))),
                AugAssign(Name("repeated"), "+", Int(1)) .Stmts,
                Assign(Name("repeated"), Int(1)) .Stmts)
              If(
                Compare(Name("repeated"), CmpOp(">", Int(2))),
                Assign(Name("result"), Bool(false)) .Stmts,
                .Stmts)
              Assign(
                Name("previous"),
                TupleExpr(Name("value"))))
            Return(Name("result")),
            0),
        parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "is_sorted" |->
          closureVal(
            "lst",
            Assign(
              Name("result"),
              Compare(
                Name("lst"),
                CmpOp(
                  "==",
                  Call(Name("sorted"), Name("lst")))))
            Assign(
              Name("previous"),
              TupleExpr(UnaryOp("-", Int(1))))
            Assign(Name("repeated"), Int(0))
            Assign(Name("value"), Int(0))
            For(
              Name("value"),
              Name("lst"),
              If(
                Compare(
                  TupleExpr(Name("value")),
                  CmpOp("==", Name("previous"))),
                AugAssign(Name("repeated"), "+", Int(1)) .Stmts,
                Assign(Name("repeated"), Int(1)) .Stmts)
              If(
                Compare(Name("repeated"), CmpOp(">", Int(2))),
                Assign(Name("result"), Bool(false)) .Stmts,
                .Stmts)
              Assign(
                Name("previous"),
                TupleExpr(Name("value"))))
            Return(Name("result")),
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map => 0 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
