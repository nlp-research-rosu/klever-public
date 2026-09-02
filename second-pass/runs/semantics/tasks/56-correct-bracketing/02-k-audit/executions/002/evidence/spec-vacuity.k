requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Inductive loop invariant at depth zero.  Returning also pops the function
  // frame, so this claim describes that complete transition.
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

  // The positive-depth half of the invariant.  Splitting zero from positive
  // depth makes the final integer equality decidable on every proof branch.
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

  // The translated implementation, from module loading through its returned
  // value, agrees with the mathematical bracket predicate for every string.
  claim [correct-bracketing]:
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
