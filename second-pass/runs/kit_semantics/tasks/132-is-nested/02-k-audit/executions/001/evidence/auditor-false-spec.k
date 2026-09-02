requires "verification.k"

module AUDITOR-FALSE-SPEC
  imports VERIFICATION

  // Fresh false mutation: the empty bracket string satisfies bracketInput,
  // but the exact submitted program returns false, not the required true.
  claim [empty-must-be-true]:
    <k>
      #loadAll(Module(
        FuncDef("is_nested", Params("string"),
          Assign(Name("state"), Int(0))
          Assign(Name("bracket"), Str(""))
          For(Name("bracket"), Name("string"),
            If(Compare(Name("state"), CmpOp("<", Int(2))),
              If(Compare(Name("bracket"), CmpOp("==", Str("["))),
                AugAssign(Name("state"), "+", Int(1)),
                .Stmts),
              If(Compare(Name("state"), CmpOp("<", Int(4))),
                If(Compare(Name("bracket"), CmpOp("==", Str("]"))),
                  AugAssign(Name("state"), "+", Int(1)),
                  .Stmts),
                .Stmts))
            .Stmts)
          Return(Compare(Name("state"), CmpOp("==", Int(4))))
          .Stmts)
        .Stmts))
      ~> Call(Name("is_nested"), str(.IntSeq))
      => true
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(.Map, parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires bracketInput(.IntSeq)
endmodule
