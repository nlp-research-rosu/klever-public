requires "verification.k"

module MAX-ELEMENT-SPEC
  imports MAX-ELEMENT-VERIFICATION

  // ---- Loop invariant (circularity) — induction on VS; running max in the store's m.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("e"),
        If(Compare(Name("e"), CmpOp(">", Name("m"))), Assign(Name("m"), Name("e")), .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "l" <- LV:Val ] [ "m" <- MV:Val ] [ "e" <- _:Val ], P:Parent) =>
        scope(.Map [ "l" <- LV ] [ "m" <- ?MOut:Val ] [ "e" <- ?_:Val ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool isInt(MV)
    ensures ?MOut ==K maxFold(intListOf(VS), {MV}:>Int)
    [all-path]

  // ---- Entry claim — result = max_element(list(vCons(H, T))) == maxFold(intListOf(T), H).
  claim
    <k>
      FuncDef("max_element", Params("l"),
        Assign(Name("m"), Subscript(Name("l"), Int(0)))
        For(Name("e"), Name("l"),
          If(Compare(Name("e"), CmpOp(">", Name("m"))), Assign(Name("m"), Name("e")), .Stmts))
        Return(Name("m")))
      Assign(Name("result"), Call(Name("max_element"), list(vCons(H:Val, T:ValSeq))))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "max_element" <- ?_:Val ] [ "result" <- ?R:Val ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(vCons(H, T))
    ensures ?R ==K maxFold(intListOf(T), {H}:>Int)
    [all-path]
endmodule
