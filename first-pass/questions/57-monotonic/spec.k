// spec.k — monotonic reachability claims on the UNIFIED semantics (src/).
// The canonical compares l against sorted(l)/sorted(l,reverse=True); solution.py is the
// equivalent adjacent-compare fold with `prev` (four accumulators: inc, dec, i, prev).
//
//   kompile verification.k --backend haskell \
//     --main-module MONOTONIC-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module MONOTONIC-SPEC

requires "verification.k"

module MONOTONIC-SPEC
  imports MONOTONIC-VERIFICATION

  // ---- Loop invariant (circularity) — from (inc=IF, dec=DF, i=IDX, prev=PV) the loop over
  // VS leaves inc := incFoldV(VS, IDX, PV, IF), dec := decFoldV(VS, IDX, PV, DF),
  // i := IDX +Int vsLen(VS), prev := lastOfV(VS, PV).  Induction on VS; the nested If splits
  // on i>=1 then the two sibling compares x<prev / x>prev (PRE-increment i, PRE-update prev).
  claim
    <k>
      #loop(list(VS:ValSeq), Name("x"),
        If(Compare(Name("i"), CmpOp(">=", Int(1))),
          If(Compare(Name("x"), CmpOp("<", Name("prev"))),
            Assign(Name("inc"), Bool(false)),
            .Stmts)
          If(Compare(Name("x"), CmpOp(">", Name("prev"))),
            Assign(Name("dec"), Bool(false)),
            .Stmts),
          .Stmts)
        Assign(Name("prev"), Name("x"))
        Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "l" <- LV:Val ] [ "inc" <- IF:Bool ] [ "dec" <- DF:Bool ]
                   [ "i" <- IDX:Int ] [ "prev" <- PV:Val ] [ "x" <- _:Val ], P:Parent) =>
        scope(.Map [ "l" <- LV ] [ "inc" <- incFoldV(VS, IDX, PV, IF) ]
                   [ "dec" <- decFoldV(VS, IDX, PV, DF) ]
                   [ "i" <- IDX +Int vsLen(VS) ] [ "prev" <- lastOfV(VS, PV) ]
                   [ "x" <- ?_:Val ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool isInt(PV)
    [all-path]

  // ---- Entry claim — after `result = monotonic(list(VS))` the root scope's result is
  // monotonicSpec(VS) = incFoldV(VS,0,0,true) orBool decFoldV(VS,0,0,true): VS is non-
  // decreasing OR non-increasing.  Holds for ANY symbolic ValSeq VS incl. the empty list
  // (no descent and no ascent => both flags stay True => True).  The loop invariant gives
  // inc/dec; `return inc or dec` evaluates STRICTLY to the orBool.
  claim
    <k>
      FuncDef("monotonic", Params("l"),
        Assign(Name("inc"), Bool(true))
        Assign(Name("dec"), Bool(true))
        Assign(Name("i"), Int(0))
        Assign(Name("prev"), Int(0))
        Assign(Name("x"), Int(0))
        For(Name("x"), Name("l"),
          If(Compare(Name("i"), CmpOp(">=", Int(1))),
            If(Compare(Name("x"), CmpOp("<", Name("prev"))),
              Assign(Name("inc"), Bool(false)),
              .Stmts)
            If(Compare(Name("x"), CmpOp(">", Name("prev"))),
              Assign(Name("dec"), Bool(false)),
              .Stmts),
            .Stmts)
          Assign(Name("prev"), Name("x"))
          Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
        Return(BoolOp("or", Name("inc"), Name("dec"))))
      Assign(Name("result"), Call(Name("monotonic"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "monotonic" <- ?_:Val ] [ "result" <- monotonicSpec(VS) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]
endmodule
