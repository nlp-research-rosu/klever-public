requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // The real program returns 2 for [4, 2, 6, 7]; requiring 3 must be rejected.
  claim [wrong-result]:
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
            list(vCons(4, vCons(2, vCons(6, vCons(7, .ValSeq)))))))
          .Stmts))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
        "add"     |-> ?ADD:Val
        "$result" |-> 3,
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
