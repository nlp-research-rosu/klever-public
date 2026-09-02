requires "verification.k"

module CORRECT-BRACKETING-SPEC
  imports CORRECT-BRACKETING-VERIFICATION

  // ---- Loop invariant (circularity) — like below_zero: the loop plus the trailing
  // `return depth == 0` returns correctFrom(CS, D). The early `return False` (depth<0)
  // realizes the everNeg disjunct; otherwise the IH handles the tail; the empty tail
  // returns (depthOf(CS,D) == 0). Result staged in <ret>. Induction on CS.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("b"),
        If(Compare(Name("b"), CmpOp("==", Str("("))),
           AugAssign(Name("depth"), "+", Int(1)),
           AugAssign(Name("depth"), "-", Int(1)))
        If(Compare(Name("depth"), CmpOp("<", Int(0))),
           Return(Bool(false)),
           .Stmts))
      ~> Return(Compare(Name("depth"), CmpOp("==", Int(0)))) .Stmts ~> #endcall
    => #pop </k>
    <ret> noRet => retV(?R:Bool) </ret>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "brackets" <- BR:Val ] [ "depth" <- D:Int ] [ "b" <- _:Val ], P:Parent) =>
        scope(.Map [ "brackets" <- BR ] [ "depth" <- ?_:Int ] [ "b" <- ?_:Val ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Bool correctFrom(CS, D)
    [all-path]

  // ---- Entry claim — result = correct_bracketing(str(CS)) == correctFrom(CS, 0).
  claim
    <k>
      FuncDef("correct_bracketing", Params("brackets"),
        Assign(Name("depth"), Int(0))
        For(Name("b"), Name("brackets"),
          If(Compare(Name("b"), CmpOp("==", Str("("))),
             AugAssign(Name("depth"), "+", Int(1)),
             AugAssign(Name("depth"), "-", Int(1)))
          If(Compare(Name("depth"), CmpOp("<", Int(0))),
             Return(Bool(false)),
             .Stmts))
        Return(Compare(Name("depth"), CmpOp("==", Int(0)))))
      Assign(Name("result"), Call(Name("correct_bracketing"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "correct_bracketing" <- ?_:Val ] [ "result" <- ?R:Bool ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Bool correctFrom(CS, 0)
    [all-path]
endmodule
