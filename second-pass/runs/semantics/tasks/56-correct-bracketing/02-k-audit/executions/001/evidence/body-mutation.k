requires "verification.k"

module BODY-MUTATION
  imports VERIFICATION

  // The submitted then-branch increments depth. This ground mutation decrements
  // it instead. On "<>" it returns false immediately, so the original expected
  // result true must be rejected.
  claim [wrong-open-update]:
    <k>
      #loadAll(Module(
        FuncDef("correct_bracketing", Params("brackets"),
          Expr(
            Str("Return whether the angle brackets are correctly balanced."))
          Assign(Name("depth"), Int(0))
          Assign(Name("bracket"), Str(""))
          For(Name("bracket"), Name("brackets"),
            If(Compare(Name("bracket"), CmpOp("==", Str("<"))),
              AugAssign(Name("depth"), "-", Int(1)),
              AugAssign(Name("depth"), "-", Int(1)))
            If(Compare(Name("depth"), CmpOp("<", Int(0))),
              Return(Bool(false)),
              .Stmts))
          Return(Compare(Name("depth"), CmpOp("==", Int(0)))))))
      ~> Call(
          Name("correct_bracketing"),
          str(iCons(60, iCons(62, .IntSeq))))
    =>
      true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    =>
      0 |-> scope(
        "correct_bracketing" |->
          closureVal(("brackets", .ParamNames),
            Expr(
              Str("Return whether the angle brackets are correctly balanced."))
            Assign(Name("depth"), Int(0))
            Assign(Name("bracket"), Str(""))
            For(Name("bracket"), Name("brackets"),
              If(Compare(Name("bracket"), CmpOp("==", Str("<"))),
                AugAssign(Name("depth"), "-", Int(1)),
                AugAssign(Name("depth"), "-", Int(1)))
              If(Compare(Name("depth"), CmpOp("<", Int(0))),
                Return(Bool(false)),
                .Stmts))
            Return(Compare(Name("depth"), CmpOp("==", Int(0)))),
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
