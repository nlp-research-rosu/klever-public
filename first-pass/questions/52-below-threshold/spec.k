requires "verification.k"

module BELOW-THRESHOLD-SPEC
  imports BELOW-THRESHOLD-VERIFICATION

  // ---- Loop invariant (circularity) — induction on the list VS; result staged in <ret>.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("e"),
        If(Compare(Name("e"), CmpOp(">=", Name("t"))), Return(Bool(false)), .Stmts))
      ~> Return(Bool(true)) .Stmts ~> #endcall
    => #pop </k>
    <ret> noRet => retV(?R:Bool) </ret>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "l" <- LV:Val ] [ "e" <- _:Val ] [ "t" <- T:Int ], P:Parent) =>
        scope(.Map [ "l" <- LV ] [ "e" <- ?_:Val ] [ "t" <- T ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    ensures ?R ==Bool allBelow(intListOf(VS), T)
    [all-path]

  // ---- Entry claim — result = below_threshold(list(VS), T) == allBelow(intListOf(VS), T).
  claim
    <k>
      FuncDef("below_threshold", Params("l", "t"),
        For(Name("e"), Name("l"),
          If(Compare(Name("e"), CmpOp(">=", Name("t"))), Return(Bool(false)), .Stmts))
        Return(Bool(true)))
      Assign(Name("result"), Call(Name("below_threshold"), list(VS:ValSeq), T:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "below_threshold" <- ?_:Val ] [ "result" <- ?R:Bool ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    ensures ?R ==Bool allBelow(intListOf(VS), T)
    [all-path]
endmodule
