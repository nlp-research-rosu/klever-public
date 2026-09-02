requires "verification.k"

module PLUCK-SPEC-FALSE-RESULT
  imports PLUCK-VERIFICATION

  claim [pluck-loop]:
    <k>
      #loop(
        list(VS:ValSeq),
        Name("value"),
        If(
          Compare(
            BinOp("%", Name("value"), Int(2)),
            CmpOp("==", Int(0))),
          If(
            Compare(
              Name("smallest"),
              CmpOp("==", UnaryOp("-", Int(1)))),
            Assign(Name("smallest"), Name("value"))
            Assign(Name("smallest_index"), Name("index")),
            If(
              Compare(Name("value"), CmpOp("<", Name("smallest"))),
              Assign(Name("smallest"), Name("value"))
              Assign(Name("smallest_index"), Name("index")),
              .Stmts)),
          .Stmts)
        AugAssign(Name("index"), "+", Int(1)))
      ~> K:K
      => K
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        "arr" |-> ARR:Val
        "smallest" |-> B:Int
        "smallest_index" |-> BI:Int
        "index" |-> I:Int
        "value" |-> LAST:Int,
        P:Parent)
      => L |-> scope(
        "arr" |-> ARR
        "smallest" |-> stateBest(scanPluck(VS, B, BI, I, LAST))
        "smallest_index" |-> stateBestIndex(scanPluck(VS, B, BI, I, LAST))
        "index" |-> stateIndex(scanPluck(VS, B, BI, I, LAST))
        "value" |-> stateLast(scanPluck(VS, B, BI, I, LAST)),
        P) ...
    </scopes>
    requires allNonNegative(VS)

  claim [pluck-correct-false-result]:
    <k>
      #loadAll(
        Module(
          FuncDef("pluck", Params("arr"),
            Assign(Name("smallest"), UnaryOp("-", Int(1)))
            Assign(Name("smallest_index"), UnaryOp("-", Int(1)))
            Assign(Name("index"), Int(0))
            Assign(Name("value"), Int(0))
            For(Name("value"), Name("arr"),
              If(
                Compare(
                  BinOp("%", Name("value"), Int(2)),
                  CmpOp("==", Int(0))),
                If(
                  Compare(
                    Name("smallest"),
                    CmpOp("==", UnaryOp("-", Int(1)))),
                  Assign(Name("smallest"), Name("value"))
                  Assign(Name("smallest_index"), Name("index")),
                  If(
                    Compare(
                      Name("value"),
                      CmpOp("<", Name("smallest"))),
                    Assign(Name("smallest"), Name("value"))
                    Assign(Name("smallest_index"), Name("index")),
                    .Stmts)),
                .Stmts)
              AugAssign(Name("index"), "+", Int(1)))
            If(
              Compare(
                Name("smallest"),
                CmpOp("==", UnaryOp("-", Int(1)))),
              Return(ListExpr(.Exprs)),
              .Stmts)
            Return(
              ListExpr(
                Name("smallest"),
                Name("smallest_index")))))
        )
      ~> Call(Name("pluck"), list(VS:ValSeq))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "pluck" |-> closureVal(
          "arr",
          Assign(Name("smallest"), UnaryOp("-", Int(1)))
          Assign(Name("smallest_index"), UnaryOp("-", Int(1)))
          Assign(Name("index"), Int(0))
          Assign(Name("value"), Int(0))
          For(Name("value"), Name("arr"),
            If(
              Compare(
                BinOp("%", Name("value"), Int(2)),
                CmpOp("==", Int(0))),
              If(
                Compare(
                  Name("smallest"),
                  CmpOp("==", UnaryOp("-", Int(1)))),
                Assign(Name("smallest"), Name("value"))
                Assign(Name("smallest_index"), Name("index")),
                If(
                  Compare(
                    Name("value"),
                    CmpOp("<", Name("smallest"))),
                  Assign(Name("smallest"), Name("value"))
                  Assign(Name("smallest_index"), Name("index")),
                  .Stmts)),
              .Stmts)
            AugAssign(Name("index"), "+", Int(1)))
          If(
            Compare(
              Name("smallest"),
              CmpOp("==", UnaryOp("-", Int(1)))),
            Return(ListExpr(.Exprs)),
            .Stmts)
          Return(
            ListExpr(
              Name("smallest"),
              Name("smallest_index"))),
          0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(0, pluckResult(VS))) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allNonNegative(VS)
endmodule
