requires "verification.k"

module AUDIT-LOOP-GENERALIZED
  imports VERIFICATION

  claim [loop-generalized-builtins-rest]:
    <k>
      #loop(list(intVals(IS)), Name("value"),
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
      ~> (Return(Name("result")) .Stmts) ~> #endcall
      => scanSorted(RESULT, PREV, DUPLICATES, IS)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      0 |-> scope(
        "is_sorted" |-> closureVal(
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
      -1 |-> scope(
        "isinstance" |-> builtinV("isinstance")
        "int" |-> typeV("int")
        BUILTINREST,
        root)
      (1 |-> scope(
        ("lst" |-> list(intVals(ORIGINAL))
         "value" |-> OLDVALUE
         "prev" |-> PREV
         "duplicates" |-> DUPLICATES
         "result" |-> RESULT),
        parent(0)) => .Map)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires DUPLICATES >=Int 0
endmodule
