// spec.k — derivative proof on the UNIFIED semantics (src/).
// Position-dependent list-map: element i (>=1) becomes i * xs[i]. The canonical is
// [(i*x) for i,x in enumerate(xs)][1:] (enumerate + trailing slice).

requires "verification.k"

module DERIVATIVE-SPEC
  imports DERIVATIVE-VERIFICATION

  // ---- Loop invariant (circularity) — from (result=list(R), i=IDX) the loop leaves
  // result := list(valSeqConcat(R, derivFrom(VS, IDX))) and i := IDX +Int vsLen(VS).
  // Induction on VS; the If splits on i>=1.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("x"),
        If(Compare(Name("i"), CmpOp(">=", Int(1))),
          Assign(Name("result"), BinOp("+", Name("result"), ListExpr(BinOp("*", Name("i"), Name("x"))))),
          .Stmts)
        Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "xs" <- XV:Val ] [ "result" <- ref(HN1_0:Int) ] [ "i" <- IDX:Int ] [ "x" <- _:Val ], P:Parent) =>
        scope(.Map [ "xs" <- XV ] [ "result" <- ref(?HN1_0B:Int) ] [ "i" <- IDX +Int vsLen(VS) ] [ "x" <- ?_:Val ], P)
      ) ...
    </scopes>
    <heap> (HN1_0 |-> list(R:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(valSeqConcat(R, derivFrom(VS, IDX)))) ?_:Map </heap>
    <heapLoc> HLC1:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
     andBool 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
    [all-path]

  // ---- Entry claim — result = derivative(list(VS)) == derivFrom(VS, 0).
  claim
    <k>
      FuncDef("derivative", Params("xs"),
        Assign(Name("result"), ListExpr(.Exprs))
        Assign(Name("i"), Int(0))
        Assign(Name("x"), Int(0))
        For(Name("x"), Name("xs"),
          If(Compare(Name("i"), CmpOp(">=", Int(1))),
            Assign(Name("result"), BinOp("+", Name("result"), ListExpr(BinOp("*", Name("i"), Name("x"))))),
            .Stmts)
          Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("derivative"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "derivative" <- ?_:Val ] [ "result" <- ref(?HN2_0:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?HN2_0 |-> list(derivFrom(VS, 0))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]
endmodule
