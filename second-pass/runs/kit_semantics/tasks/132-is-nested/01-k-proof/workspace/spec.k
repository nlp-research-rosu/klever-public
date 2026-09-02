requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop]:
    <k>
      #loop(
        str(CS:IntSeq),
        Name("bracket"),
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
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      ...
      1 |-> scope(
        "state"   |-> (S:Int => nestedScan(CS, S))
        "bracket" |-> (_BR:Val => ?BR:Val)
        "string"  |-> str(INPUT:IntSeq),
        parent(0))
      ...
    </scopes>
    requires bracketInput(CS)
      andBool S >=Int 0
      andBool S <=Int 4

  claim [program]:
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
      ~> Call(Name("is_nested"), str(CS:IntSeq))
      => ?RESULT:Bool
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        .Map
        =>
        "is_nested" |-> closureVal(
          "string", .ParamNames,
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
          .Stmts,
          0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires bracketInput(CS)
    ensures ?RESULT ==Bool nestedResult(CS)
endmodule
