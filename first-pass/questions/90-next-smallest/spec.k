// spec.k — next_smallest on the UNIFIED semantics (src/). Two-pass min / 2nd-smallest-distinct.
// Elements are symbolic Vals under allInt; the reference operator cast bridge reduces x<min1 etc.
// via projectIntTotal. min1 = minFold(T,H) is an opaque Val summary fed into pass 2 — the pass-2
// invariant requires definedProjectInt(min1) (dischargeable for minFold, unlike isInt). See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module NEXT-SMALLEST-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module NEXT-SMALLEST-SPEC

requires "verification.k"

module NEXT-SMALLEST-SPEC
  imports NEXT-SMALLEST-VERIFICATION

  // ---- PASS 1 loop invariant — running pass 1 over VS from min1 = MV leaves min1 := minFold(VS, MV).
  claim
    <k>
      #loop(list(VS:ValSeq), Name("x"),
        If(Compare(Name("x"), CmpOp("<", Name("min1"))), Assign(Name("min1"), Name("x")), .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "next_smallest" <- _:Val ], parent(-1))
       1 |-> (
        scope(.Map [ "lst" <- LV:Val ] [ "min1" <- MV:Val ] [ "x" <- _:Val ], parent(0)) =>
        scope(.Map [ "lst" <- LV ] [ "min1" <- ?MOut:Val ] [ "x" <- ?_:Val ], parent(0))
      )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool isInt(MV)
    ensures ?MOut ==K minFold(VS, MV)
    [all-path]

  // ---- PASS 2 loop invariant — over VS with min1 = MIN1 (constant) and (found, m2) leaves
  // found := foundFold(VS, MIN1, F) and m2 := m2Fold(VS, MIN1, F, M2). definedProjectInt(MIN1)
  // (= isInt) lets the x>min1 / x<m2 compares reduce via the cast bridge.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("x"),
        If(Compare(Name("x"), CmpOp(">", Name("min1"))),
           If(Name("found"),
              If(Compare(Name("x"), CmpOp("<", Name("m2"))), Assign(Name("m2"), Name("x")), .Stmts),
              Assign(Name("m2"), Name("x"))
              Assign(Name("found"), Bool(true))),
           .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "next_smallest" <- _:Val ], parent(-1))
       1 |-> (
        scope(.Map [ "lst" <- LV:Val ] [ "min1" <- MIN1:Val ]
                   [ "found" <- F:Bool ] [ "m2" <- M2:Val ] [ "x" <- _:Val ], parent(0)) =>
        scope(.Map [ "lst" <- LV ] [ "min1" <- MIN1 ]
                   [ "found" <- ?FO:Bool ] [ "m2" <- ?M2O:Val ] [ "x" <- ?_:Val ], parent(0))
      )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool knownInt(MIN1) andBool knownInt(M2)
    ensures ?FO ==K foundFold(VS, MIN1, F) andBool ?M2O ==K m2Fold(VS, MIN1, F, M2)
    [all-path]

  // ---- Entry claim — for a NON-EMPTY list vCons(H, T): result = nextSmallest(H, T) (the
  // 2nd-smallest DISTINCT element, or None). The `if not lst` guard is the skipped false branch.
  claim
    <k>
      FuncDef("next_smallest", Params("lst"),
        If(UnaryOp("not", Name("lst")), Return(NoneVal), .Stmts)
        Assign(Name("min1"), Subscript(Name("lst"), Int(0)))
        For(Name("x"), Name("lst"),
          If(Compare(Name("x"), CmpOp("<", Name("min1"))), Assign(Name("min1"), Name("x")), .Stmts))
        Assign(Name("found"), Bool(false))
        Assign(Name("m2"), Int(0))
        For(Name("x"), Name("lst"),
          If(Compare(Name("x"), CmpOp(">", Name("min1"))),
             If(Name("found"),
                If(Compare(Name("x"), CmpOp("<", Name("m2"))), Assign(Name("m2"), Name("x")), .Stmts),
                Assign(Name("m2"), Name("x"))
                Assign(Name("found"), Bool(true))),
             .Stmts))
        Return(IfExp(Name("found"), Name("m2"), NoneVal)))
      Assign(Name("result"), Call(Name("next_smallest"), list(vCons(H:Val, T:ValSeq))))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "next_smallest" <- ?_:Val ] [ "result" <- nextSmallest(H, T) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(vCons(H, T))
    [all-path]
endmodule
