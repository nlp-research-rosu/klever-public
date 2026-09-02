requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim [loop-zero]:
    <k>
      #loop(str(S:IntSeq), Name("bracket"),
        If(Compare(Name("bracket"), CmpOp("==", Str("<"))),
          AugAssign(Name("depth"), "+", Int(1)),
          AugAssign(Name("depth"), "-", Int(1)))
        If(Compare(Name("depth"), CmpOp("<", Int(0))),
          Return(Bool(false)),
          .Stmts))
      ~> (Return(Compare(Name("depth"), CmpOp("==", Int(0)))) .Stmts)
      ~> #endcall
    =>
      bracketResult(S, 0) ~> CONT
    </k>
    <env> L => CALLER </env>
    <scopes>
      (L |-> scope(
          "brackets" |-> str(INPUT:IntSeq)
          "depth" |-> 0
          "bracket" |-> OLD:Val,
          P:Parent)
       SC:Map)
    =>
      SC
    </scopes>
    <scopeLoc> _ => SAVED </scopeLoc>
    <stack>
      ListItem(frame(CONT:K, CALLER:Int, SAVED:Int)) REST:List => REST
    </stack>
    <ret> noRet </ret>
    requires notBool L in_keys(SC)

  claim [loop-positive]:
    <k>
      #loop(str(S:IntSeq), Name("bracket"),
        If(Compare(Name("bracket"), CmpOp("==", Str("<"))),
          AugAssign(Name("depth"), "+", Int(1)),
          AugAssign(Name("depth"), "-", Int(1)))
        If(Compare(Name("depth"), CmpOp("<", Int(0))),
          Return(Bool(false)),
          .Stmts))
      ~> (Return(Compare(Name("depth"), CmpOp("==", Int(0)))) .Stmts)
      ~> #endcall
    =>
      bracketResult(S, D) ~> CONT
    </k>
    <env> L => CALLER </env>
    <scopes>
      (L |-> scope(
          "brackets" |-> str(INPUT:IntSeq)
          "depth" |-> D
          "bracket" |-> OLD:Val,
          P:Parent)
       SC:Map)
    =>
      SC
    </scopes>
    <scopeLoc> _ => SAVED </scopeLoc>
    <stack>
      ListItem(frame(CONT:K, CALLER:Int, SAVED:Int)) REST:List => REST
    </stack>
    <ret> noRet </ret>
    requires D >Int 0
      andBool notBool L in_keys(SC)

  // Deliberately false for the satisfying input S=.IntSeq: the real result is
  // true, while this mutation requires false.
  claim [correct-bracketing-false]:
    <k>
      #loadAll(Module(
        FuncDef("correct_bracketing", Params("brackets"),
          Expr(
            Str("Return whether the angle brackets are correctly balanced."))
          Assign(Name("depth"), Int(0))
          Assign(Name("bracket"), Str(""))
          For(Name("bracket"), Name("brackets"),
            If(Compare(Name("bracket"), CmpOp("==", Str("<"))),
              AugAssign(Name("depth"), "+", Int(1)),
              AugAssign(Name("depth"), "-", Int(1)))
            If(Compare(Name("depth"), CmpOp("<", Int(0))),
              Return(Bool(false)),
              .Stmts))
          Return(Compare(Name("depth"), CmpOp("==", Int(0)))))))
      ~> Call(Name("correct_bracketing"), str(S:IntSeq))
    =>
      notBool bracketResult(S, 0)
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
                AugAssign(Name("depth"), "+", Int(1)),
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
