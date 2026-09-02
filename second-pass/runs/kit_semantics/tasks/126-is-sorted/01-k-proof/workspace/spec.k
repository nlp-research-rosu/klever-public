requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [scan-loop]:
    <k>
      #loop(
        list(REMAINING:ValSeq),
        Name("value"),
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
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "lst" |-> list(INPUT:ValSeq)
        "previous" |->
          (tuple(vCons(P:Val, .ValSeq))
            => tuple(vCons(scanPrevious(P, REMAINING), .ValSeq)))
        "repeated" |-> (C:Int => scanRepeated(P, C, REMAINING))
        "result" |->
          (B:Bool => scanDuplicates(P, C, B, REMAINING))
        "value" |-> (V:Val => scanValue(V, REMAINING)),
        parent(0))
      ...
    </scopes>
    <scopeLoc> SCOPELOC:Int </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HEAPLOC:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> RET:RetState </ret>
    <exc> EXC:Exc </exc>
    <exit-code> EXIT:Int </exit-code>

  claim [entry]:
    <k>
      Call(
        Name("is_sorted"),
        list(VS:ValSeq))
      => sortedWithAtMostTwo(VS)
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
      .Map => 0 |-> list(sortVS(VS))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires nonNegativeVals(VS)
endmodule
