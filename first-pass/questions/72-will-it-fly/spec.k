// spec.k — will_it_fly proof on the UNIFIED semantics (src/).
// Compose two folds: total = sum(q), rev = reverse(q); return (total <= w) and (q == rev)
// (palindrome via list equality). The canonical indexes q[i]/q[j] at symbolic i,j.

requires "verification.k"

module WILL-IT-FLY-SPEC
  imports WILL-IT-FLY-VERIFICATION

  // ---- Loop invariant (circularity) — dual fold. From (total=T, rev=list(R)) the loop
  // leaves total := T +Int sumVS(VS) and rev := list(revVS(VS, R)). Induction on VS.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("x"),
        Assign(Name("total"), BinOp("+", Name("total"), Name("x")))
        Assign(Name("rev"), BinOp("+", ListExpr(Name("x")), Name("rev"))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "q" <- QV:Val ] [ "w" <- WV:Val ] [ "total" <- T:Int ] [ "rev" <- ref(HN1_0:Int) ] [ "x" <- _:Val ], P:Parent) =>
        scope(.Map [ "q" <- QV ] [ "w" <- WV ] [ "total" <- T +Int sumVS(VS) ] [ "rev" <- ref(?HN1_0B:Int) ] [ "x" <- ?_:Val ], P)
      ) ...
    </scopes>
    <heap> (HN1_0 |-> list(R:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(revVS(VS, R))) ?_:Map </heap>
    <heapLoc> HLC1:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
     andBool 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
    [all-path]

  // ---- Entry claim — result = will_it_fly(list(VS), W) ==
  //   (sumVS(VS) <=Int W) andBool (VS ==K revVS(VS, .ValSeq)).
  claim
    <k>
      FuncDef("will_it_fly", Params("q", "w"),
        Assign(Name("total"), Int(0))
        Assign(Name("rev"), ListExpr(.Exprs))
        Assign(Name("x"), Int(0))
        For(Name("x"), Name("q"),
          Assign(Name("total"), BinOp("+", Name("total"), Name("x")))
          Assign(Name("rev"), BinOp("+", ListExpr(Name("x")), Name("rev"))))
        Return(BoolOp("and",
          Compare(Name("total"), CmpOp("<=", Name("w"))),
          Compare(Name("q"), CmpOp("==", Name("rev"))))))
      Assign(Name("result"), Call(Name("will_it_fly"), list(VS:ValSeq) , W:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "will_it_fly" <- ?_:Val ]
                       [ "result" <- (sumVS(VS) <=Int W) andBool (VS ==K revVS(VS, .ValSeq)) ], parent(-1))
    </scopes>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]
endmodule
