requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [pluck-loop]:
    <k>
      #loop(
        list(vCons(HEAD:Val, REST:ValSeq)),
        Name("value"),
        Assign(Name("value"), BinOp("+", Name("value"), Int(0)))
        If(
          Compare(
            BinOp("%", Name("value"), Int(2)),
            CmpOp("==", Int(0))),
          If(
            Compare(Name("smallest"), CmpOp("<", Int(0))),
            Assign(Name("smallest"), Name("value"))
            Assign(Name("smallest_index"), Name("index")),
            If(
              Compare(Name("value"), CmpOp("<", Name("smallest"))),
              Assign(Name("smallest"), Name("value"))
              Assign(Name("smallest_index"), Name("index")),
              .Stmts)),
          .Stmts)
        AugAssign(Name("index"), "+", Int(1)))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "arr"            |-> list(ORIGINAL:ValSeq)
        "smallest"       |-> (BEST:Int
                              => scanBest(
                                   vCons(HEAD, REST), POS, BEST))
        "smallest_index" |-> (BEST_INDEX:Int
                              => scanBestIndex(
                                   vCons(HEAD, REST),
                                   POS,
                                   BEST,
                                   BEST_INDEX))
        "index"          |-> (POS:Int
                              => afterIndex(vCons(HEAD, REST), POS))
        "value"          |-> (_OLD:Val => ?FINAL_VALUE:Val),
        parent(0))
      ...
    </scopes>
    requires POS >=Int 0
      andBool definedProjectInt(HEAD)
      andBool projectIntTotal(HEAD) >=Int 0
      andBool allNonNegative(REST)

  claim [pluck-entry]:
    <k>
      Call(Name("pluck"), list(INPUT:ValSeq))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        "pluck" |-> closureVal(
          "arr",
          Assign(Name("smallest"), UnaryOp("-", Int(1)))
          Assign(Name("smallest_index"), Int(0))
          Assign(Name("index"), Int(0))
          Assign(Name("value"), Int(0))
          For(
            Name("value"),
            Name("arr"),
            Assign(Name("value"), BinOp("+", Name("value"), Int(0)))
            If(
              Compare(
                BinOp("%", Name("value"), Int(2)),
                CmpOp("==", Int(0))),
              If(
                Compare(Name("smallest"), CmpOp("<", Int(0))),
                Assign(Name("smallest"), Name("value"))
                Assign(Name("smallest_index"), Name("index")),
                If(
                  Compare(Name("value"), CmpOp("<", Name("smallest"))),
                  Assign(Name("smallest"), Name("value"))
                  Assign(Name("smallest_index"), Name("index")),
                  .Stmts)),
              .Stmts)
            AugAssign(Name("index"), "+", Int(1)))
          If(
            Compare(Name("smallest"), CmpOp("<", Int(0))),
            Return(ListExpr(.Exprs)),
            .Stmts)
          Return(ListExpr(Name("smallest"), Name("smallest_index"))),
          0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> resultList(
                  scanBest(INPUT, 0, -1),
                  scanBestIndex(INPUT, 0, -1, 0))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allNonNegative(INPUT)
endmodule
