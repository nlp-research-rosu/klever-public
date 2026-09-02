// spec.k — smallest_change proof on the UNIFIED semantics (src/).
// Pass 1 builds rev = reverse(arr) by prepend; pass 2 zips arr with rev counting
// mismatches; palindrome edit distance = mismatches // 2.

requires "verification.k"

module SMALLEST-CHANGE-SPEC
  imports SMALLEST-CHANGE-VERIFICATION

  // ---- Loop invariant 1: build rev = reverse(arr) by prepend.
  // Over any ValSeq CS from rev=list(R) the loop leaves rev := list(revAcc(CS, R)).
  claim
    <k>
      #loop(list(CS:ValSeq), Name("x"),
        Assign(Name("rev"), BinOp("+", ListExpr(Name("x")), Name("rev"))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "arr" <- AV:Val ] [ "rev" <- ref(HN1_0:Int) ] [ "x" <- _:Val ] [ "cnt" <- CNT:Int ] [ "a" <- AA:Val ] [ "r" <- RR:Val ], P:Parent) =>
        scope(.Map [ "arr" <- AV ] [ "rev" <- ref(?HN1_0B:Int) ] [ "x" <- ?_:Val ] [ "cnt" <- CNT ] [ "a" <- AA ] [ "r" <- RR ], P)
      ) ...
    </scopes>
    <heap> (HN1_0 |-> list(R:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(revAcc(CS, R))) ?_:Map </heap>
    <heapLoc> HLC1:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
    [all-path]

  // ---- Loop invariant 2: zip arr with rev, counting mismatches.
  // Over two ValSeqs S1, S2 from cnt=CNT the loop leaves cnt := zipMismatch(S1, S2, CNT).
  claim
    <k>
      #loop(zipObj(S1:ValSeq, S2:ValSeq), TupleExpr(Name("a"), Name("r")),
        If(Compare(Name("a"), CmpOp("!=", Name("r"))),
           Assign(Name("cnt"), BinOp("+", Name("cnt"), Int(1))),
           .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "arr" <- AV:Val ] [ "rev" <- RV:Val ] [ "x" <- XV:Val ] [ "cnt" <- CNT:Int ] [ "a" <- _:Val ] [ "r" <- _:Val ], P:Parent) =>
        scope(.Map [ "arr" <- AV ] [ "rev" <- RV ] [ "x" <- XV ] [ "cnt" <- zipMismatch(S1, S2, CNT) ] [ "a" <- ?_:Val ] [ "r" <- ?_:Val ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(S1) andBool allInt(S2)
    [all-path]

  // ---- Entry claim — result = smallest_change(list(A)) == zipMismatch(A, rev(A), 0) // 2.
  claim
    <k>
      FuncDef("smallest_change", Params("arr"),
        Assign(Name("rev"), ListExpr(.Exprs))
        Assign(Name("x"), Int(0))
        Assign(Name("cnt"), Int(0))
        Assign(Name("a"), Int(0))
        Assign(Name("r"), Int(0))
        For(Name("x"), Name("arr"),
          Assign(Name("rev"), BinOp("+", ListExpr(Name("x")), Name("rev"))))
        For(TupleExpr(Name("a"), Name("r")), Call(Name("zip"), Name("arr"), Name("rev")),
          If(Compare(Name("a"), CmpOp("!=", Name("r"))),
             Assign(Name("cnt"), BinOp("+", Name("cnt"), Int(1))),
             .Stmts))
        Return(BinOp("//", Name("cnt"), Int(2))))
      Assign(Name("result"), Call(Name("smallest_change"), list(A:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "smallest_change" <- ?_:Val ]
                       [ "result" <- ( zipMismatch(A, revAcc(A, .ValSeq), 0)
                                       -Int pyMod(zipMismatch(A, revAcc(A, .ValSeq), 0), 2) ) /Int 2 ], parent(-1))
    </scopes>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(A)
    [all-path]
endmodule
