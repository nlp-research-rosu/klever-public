requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop]:
    <k>
      #loop(
        str(CS:IntSeq),
        Name("bracket"),
        If(
          Compare(Name("bracket"), CmpOp("==", Str("("))),
          AugAssign(Name("balance"), "+", Int(1)),
          AugAssign(Name("balance"), "-", Int(1)))
        If(
          Compare(Name("balance"), CmpOp("<", Int(0))),
          Assign(Name("valid"), Bool(false)),
          .Stmts))
      ~> (Return(
            BoolOp(
              "and",
              Name("valid"),
              Compare(Name("balance"), CmpOp("==", Int(0)))))
          .Stmts)
      ~> #endcall
      =>
      scanBrackets(CS, B:Int, V:Bool)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( -1 |-> BUILTINS:Scope
         0 |-> scope(MODULE:Map, parent(-1))
         1 |-> scope(
                "bracket" |-> _OLD:Val
                "brackets" |-> str(_INPUT:IntSeq)
                "balance" |-> B
                "valid" |-> V,
                parent(0)) )
      =>
      ( -1 |-> BUILTINS
         0 |-> scope(MODULE, parent(-1)) )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires bracketInput(CS)

  claim [correct-bracketing]:
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
      ~> Call(Name("correct_bracketing"), str(CS:IntSeq))
      =>
      scanBrackets(CS, 0, true)
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
    requires bracketInput(CS)
endmodule
