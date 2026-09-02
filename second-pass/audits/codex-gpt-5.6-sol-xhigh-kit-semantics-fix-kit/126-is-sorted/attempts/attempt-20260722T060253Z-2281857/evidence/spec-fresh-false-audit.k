requires "verification.k"

module AUDIT-FRESH-FALSE
  imports VERIFICATION-ENTRY

  // Deliberately false on the satisfying intended-domain input [0,0,0].
  // The real program and scanSorted both return false; this mutation demands true.
  claim [triple-duplicate-is-true]:
    <k>
      #loadAll(Module(
        FuncDef("is_sorted", Params("lst"),
          Assign(Name("prev"), UnaryOp("-", Int(1)))
          Assign(Name("duplicates"), Int(0))
          Assign(Name("result"), Bool(true))
          For(Name("value"), Name("lst"),
            If(Call(Name("isinstance"), Name("value"), Name("int")),
              If(Compare(Name("value"), CmpOp("<", Name("prev"))),
                Assign(Name("result"), Bool(false)),
                .Stmts)
              If(Compare(Name("value"), CmpOp("==", Name("prev"))),
                AugAssign(Name("duplicates"), "+", Int(1)),
                Assign(Name("duplicates"), Int(0)))
              If(Compare(Name("duplicates"), CmpOp(">", Int(1))),
                Assign(Name("result"), Bool(false)),
                .Stmts)
              Assign(Name("prev"), Name("value")),
              Return(Bool(false))))
          Return(Name("result")))))
      ~> Call(Name("is_sorted"),
              (list(intVals(iCons(0, iCons(0, iCons(0, .IntSeq))))), .Exprs))
      => true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "is_sorted" |-> closureVal(
          "lst", .ParamNames,
          Assign(Name("prev"), UnaryOp("-", Int(1)))
          Assign(Name("duplicates"), Int(0))
          Assign(Name("result"), Bool(true))
          For(Name("value"), Name("lst"),
            If(Call(Name("isinstance"), Name("value"), Name("int")),
              If(Compare(Name("value"), CmpOp("<", Name("prev"))),
                Assign(Name("result"), Bool(false)),
                .Stmts)
              If(Compare(Name("value"), CmpOp("==", Name("prev"))),
                AugAssign(Name("duplicates"), "+", Int(1)),
                Assign(Name("duplicates"), Int(0)))
              If(Compare(Name("duplicates"), CmpOp(">", Int(1))),
                Assign(Name("result"), Bool(false)),
                .Stmts)
              Assign(Name("prev"), Name("value")),
              Return(Bool(false))))
          Return(Name("result")),
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
