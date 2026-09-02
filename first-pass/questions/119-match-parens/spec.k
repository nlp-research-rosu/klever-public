// spec.k — match_parens proof on the UNIFIED semantics (src/).
// Two sequential balance-fold loops (val + sticky ok) over s1=lst[0]+lst[1] and
// s2=lst[1]+lst[0]; "Yes" iff either order is balanceable.

requires "verification.k"

module MATCH-PARENS-SPEC
  imports MATCH-PARENS-VERIFICATION

  // ---- Loop invariant (circularity) — the balance fold over one string CS: from
  // (val=V, ok=OK) the loop leaves val := balVal(CS,V), ok := balOk(CS,V,OK). By induction
  // on CS. ONE generic claim covers BOTH of the program's two loops (over s1 and s2).
  claim
    <k>
      #loop(str(CS:IntSeq), Name("c"),
        If(Compare(Name("c"), CmpOp("==", Str("("))),
           Assign(Name("val"), BinOp("+", Name("val"), Int(1))),
           Assign(Name("val"), BinOp("-", Name("val"), Int(1))))
        If(Compare(Name("val"), CmpOp("<", Int(0))),
           Assign(Name("ok"), Bool(false)),
           .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "lst" <- LV:Val ] [ "s1" <- S1V:Val ] [ "s2" <- S2V:Val ] [ "val" <- V:Int ] [ "ok" <- OK:Bool ] [ "c" <- _:Val ] [ "r1" <- R1:Bool ] [ "r2" <- R2:Bool ], P:Parent) =>
        scope(.Map [ "lst" <- LV ] [ "s1" <- S1V ] [ "s2" <- S2V ] [ "val" <- balVal(CS, V) ] [ "ok" <- balOk(CS, V, OK) ] [ "c" <- ?_:Val ] [ "r1" <- R1 ] [ "r2" <- R2 ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — for a 2-element list of strings (codes A, B), result is "Yes" iff
  // some concatenation order is balanceable, else "No".
  claim
    <k>
      FuncDef("match_parens", Params("lst"),
        Assign(Name("s1"), BinOp("+", Subscript(Name("lst"), Int(0)), Subscript(Name("lst"), Int(1))))
        Assign(Name("s2"), BinOp("+", Subscript(Name("lst"), Int(1)), Subscript(Name("lst"), Int(0))))
        Assign(Name("val"), Int(0))
        Assign(Name("ok"), Bool(true))
        Assign(Name("c"), Str(""))
        Assign(Name("r1"), Bool(false))
        Assign(Name("r2"), Bool(false))
        For(Name("c"), Name("s1"),
          If(Compare(Name("c"), CmpOp("==", Str("("))),
             Assign(Name("val"), BinOp("+", Name("val"), Int(1))),
             Assign(Name("val"), BinOp("-", Name("val"), Int(1))))
          If(Compare(Name("val"), CmpOp("<", Int(0))),
             Assign(Name("ok"), Bool(false)),
             .Stmts))
        Assign(Name("r1"), BoolOp("and", Name("ok"), Compare(Name("val"), CmpOp("==", Int(0)))))
        Assign(Name("val"), Int(0))
        Assign(Name("ok"), Bool(true))
        For(Name("c"), Name("s2"),
          If(Compare(Name("c"), CmpOp("==", Str("("))),
             Assign(Name("val"), BinOp("+", Name("val"), Int(1))),
             Assign(Name("val"), BinOp("-", Name("val"), Int(1))))
          If(Compare(Name("val"), CmpOp("<", Int(0))),
             Assign(Name("ok"), Bool(false)),
             .Stmts))
        Assign(Name("r2"), BoolOp("and", Name("ok"), Compare(Name("val"), CmpOp("==", Int(0)))))
        Return(IfExp(BoolOp("or", Name("r1"), Name("r2")), Str("Yes"), Str("No"))))
      Assign(Name("result"),
        Call(Name("match_parens"), list(vCons(str(A:IntSeq), vCons(str(B:IntSeq), .ValSeq)))))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "match_parens" <- ?_:Val ]
                       [ "result" <- #if ( checkBalance(seqConcat(A, B)) orBool checkBalance(seqConcat(B, A)) )
                                     #then str(strToCodes("Yes")) #else str(strToCodes("No")) #fi ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
