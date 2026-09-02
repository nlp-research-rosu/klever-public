requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports VERIFICATION

  // Reviewer-authored false mutation. The satisfying input "()" returns true;
  // the deliberately false target below must remain unprovable.
  claim [pair-falsely-returns-false]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "correct_bracketing",
            Params("brackets"),
            Assign(Name("balance"), Int(0))
            Assign(Name("valid"), Bool(true))
            For(
              Name("bracket"),
              Name("brackets"),
              If(
                Compare(Name("bracket"), CmpOp("==", Str("("))),
                AugAssign(Name("balance"), "+", Int(1)),
                AugAssign(Name("balance"), "-", Int(1)))
              If(
                Compare(Name("balance"), CmpOp("<", Int(0))),
                Assign(Name("valid"), Bool(false)),
                .Stmts))
            Return(
              BoolOp(
                "and",
                Name("valid"),
                Compare(Name("balance"), CmpOp("==", Int(0))))))))
      ~> Call(
           Name("correct_bracketing"),
           str(iCons(40, iCons(41, .IntSeq))))
      =>
      false
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        .Map
        =>
        "correct_bracketing" |->
          closureVal(
            "brackets",
            Assign(Name("balance"), Int(0))
            Assign(Name("valid"), Bool(true))
            For(
              Name("bracket"),
              Name("brackets"),
              If(
                Compare(Name("bracket"), CmpOp("==", Str("("))),
                AugAssign(Name("balance"), "+", Int(1)),
                AugAssign(Name("balance"), "-", Int(1)))
              If(
                Compare(Name("balance"), CmpOp("<", Int(0))),
                Assign(Name("valid"), Bool(false)),
                .Stmts))
            Return(
              BoolOp(
                "and",
                Name("valid"),
                Compare(Name("balance"), CmpOp("==", Int(0))))),
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
endmodule
