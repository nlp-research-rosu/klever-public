requires "verification.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION

  // Material mutation: add 1 instead of the selected list value.  Keeping the
  // real expected result 2 must make this connection claim fail.
  claim [mutated-body]:
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
                AugAssign(Name("result"), "+", Int(1)) .Stmts,
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
        "$result" |-> 2,
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
