requires "verification.k"

module SPEC
  imports VERIFICATION

  // Circularity for the exact source loop.  IS is an arbitrary finite suffix,
  // so this is an unbounded structural theorem, not a bounded unrolling.
  claim [add-loop]:
    <k>
      #loop(
        list(VS:ValSeq),
        Name("value"),
        If(
          Name("odd"),
          If(
            Compare(
              BinOp("%", Name("value"), Int(2)),
              CmpOp("==", Int(0))),
            AugAssign(Name("result"), "+", Name("value")) .Stmts,
            .Stmts) .Stmts,
          .Stmts)
        Assign(Name("odd"), UnaryOp("not", Name("odd"))) .Stmts)
      => .K ...
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        "lst"    |-> INPUT:Val
        "result" |-> (ACC:Int => ACC +Int addSummary(VS, ODD))
        "odd"    |-> (ODD:Bool => ?FINALODD:Bool)
        "value"  |-> (_CURRENT:Val => ?FINALVALUE:Val),
        P:Parent)
      ...
    </scopes>
    requires allInts(VS)

  // Whole-entry theorem.  The exact translated body is defined, looked up,
  // called, and executed under MPY.  The precondition is precisely the
  // contract's non-empty, otherwise-unbounded finite integer-list domain.
  claim [add-entry]:
    <k>
      #loadAll(Module(
        FuncDef(
          "add",
          Params("lst"),
          Assign(Name("result"), Int(0))
          Assign(Name("odd"), Bool(false))
          Assign(Name("value"), Int(0))
          For(
            Name("value"),
            Name("lst"),
            If(
              Name("odd"),
              If(
                Compare(
                  BinOp("%", Name("value"), Int(2)),
                  CmpOp("==", Int(0))),
                AugAssign(Name("result"), "+", Name("value")) .Stmts,
                .Stmts) .Stmts,
              .Stmts)
            Assign(Name("odd"), UnaryOp("not", Name("odd"))) .Stmts)
          Return(Name("result")) .Stmts)
        Assign(
          Name("$result"),
          Call(
            Name("add"),
            list(VS:ValSeq))) .Stmts))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
        "add"     |-> ?ADD:Val
        "$result" |-> addSummary(VS, false),
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
    requires allInts(VS) andBool VS =/=K .ValSeq
endmodule
