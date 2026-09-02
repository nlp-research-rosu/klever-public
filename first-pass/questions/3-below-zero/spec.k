requires "verification.k"

module BELOW-ZERO-SPEC
  imports BELOW-ZERO-VERIFICATION

  // ---- Loop invariant (circularity) — induction on the list VS; result staged in <ret>.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("op"),
        AugAssign(Name("balance"), "+", Name("op"))
        If(Compare(Name("balance"), CmpOp("<", Int(0))), Return(Bool(true)), .Stmts))
      ~> Return(Bool(false)) .Stmts ~> #endcall
    => #pop </k>
    <ret> noRet => retV(?R:Bool) </ret>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "operations" <- OV:Val ] [ "op" <- _:Val ] [ "balance" <- B:Int ], P:Parent) =>
        scope(.Map [ "operations" <- OV ] [ "op" <- ?_:Val ] [ "balance" <- ?_:Int ], P)
      ) ...
    </scopes>
    requires allInt(VS)
    ensures ?R ==Bool wentNeg(intListOf(VS), B)
    [all-path]

  // ---- Entry claim — result = below_zero(list(VS)) == wentNeg(intListOf(VS), 0).
  claim
    <k>
      FuncDef("below_zero", Params("operations"),
        Assign(Name("balance"), Int(0))
        For(Name("op"), Name("operations"),
          AugAssign(Name("balance"), "+", Name("op"))
          If(Compare(Name("balance"), CmpOp("<", Int(0))), Return(Bool(true)), .Stmts))
        Return(Bool(false)))
      Assign(Name("result"), Call(Name("below_zero"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "below_zero" <- ?_:Val ] [ "result" <- ?R:Bool ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    requires allInt(VS)
    ensures ?R ==Bool wentNeg(intListOf(VS), 0)
    [all-path]
endmodule
