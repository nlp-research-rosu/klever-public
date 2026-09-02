// spec.k — largest_smallest_integers on the UNIFIED semantics (src/). One pass, four accumulators
// a/b/hn/hp; the negative/positive sides fold via maxNeg/minPos (+ hasNeg/hasPos flags). Elements
// are symbolic Vals under allInt; a/b carry isInt so `x>a` / `x<b` reduce via the cast bridge. The
// result maps the flags to None. See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module LARGEST-SMALLEST-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module LARGEST-SMALLEST-SPEC

requires "verification.k"

module LARGEST-SMALLEST-SPEC
  imports LARGEST-SMALLEST-VERIFICATION

  // ---- Loop invariant (circularity) — over CS from (a=A, b=B, hn=HN, hp=HP) the loop leaves
  //   a := maxNeg(CS, A, HN)   b := minPos(CS, B, HP)   hn := HN orBool hasNeg(CS)   hp := HP orBool hasPos(CS)
  claim
    <k>
      #loop(list(CS:ValSeq), Name("x"),
        If(Compare(Name("x"), CmpOp("<", Int(0))),
           If(Compare(Name("hn"), CmpOp("==", Bool(false))),
              Assign(Name("a"), Name("x")) Assign(Name("hn"), Bool(true)),
              If(Compare(Name("x"), CmpOp(">", Name("a"))),
                 Assign(Name("a"), Name("x")),
                 .Stmts)),
           If(Compare(Name("x"), CmpOp(">", Int(0))),
              If(Compare(Name("hp"), CmpOp("==", Bool(false))),
                 Assign(Name("b"), Name("x")) Assign(Name("hp"), Bool(true)),
                 If(Compare(Name("x"), CmpOp("<", Name("b"))),
                    Assign(Name("b"), Name("x")),
                    .Stmts)),
              .Stmts)))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "lst" <- LV:Val ] [ "a" <- A:Val ] [ "b" <- B:Val ]
                   [ "hn" <- HN:Bool ] [ "hp" <- HP:Bool ] [ "x" <- _:Val ], P:Parent) =>
        scope(.Map [ "lst" <- LV ] [ "a" <- maxNeg(CS, A, HN) ] [ "b" <- minPos(CS, B, HP) ]
                   [ "hn" <- HN orBool hasNeg(CS) ] [ "hp" <- HP orBool hasPos(CS) ] [ "x" <- ?_:Val ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(CS) andBool isInt(A) andBool isInt(B)
    [all-path]

  // ---- Entry claim — result = (largest negative or None, smallest positive or None).
  claim
    <k>
      FuncDef("largest_smallest_integers", Params("lst"),
        Assign(Name("a"), Int(0))
        Assign(Name("b"), Int(0))
        Assign(Name("hn"), Bool(false))
        Assign(Name("hp"), Bool(false))
        Assign(Name("x"), Int(0))
        For(Name("x"), Name("lst"),
          If(Compare(Name("x"), CmpOp("<", Int(0))),
             If(Compare(Name("hn"), CmpOp("==", Bool(false))),
                Assign(Name("a"), Name("x")) Assign(Name("hn"), Bool(true)),
                If(Compare(Name("x"), CmpOp(">", Name("a"))),
                   Assign(Name("a"), Name("x")),
                   .Stmts)),
             If(Compare(Name("x"), CmpOp(">", Int(0))),
                If(Compare(Name("hp"), CmpOp("==", Bool(false))),
                   Assign(Name("b"), Name("x")) Assign(Name("hp"), Bool(true)),
                   If(Compare(Name("x"), CmpOp("<", Name("b"))),
                      Assign(Name("b"), Name("x")),
                      .Stmts)),
                .Stmts)))
        Assign(Name("ra"), NoneVal)
        If(Name("hn"), Assign(Name("ra"), Name("a")), .Stmts)
        Assign(Name("rb"), NoneVal)
        If(Name("hp"), Assign(Name("rb"), Name("b")), .Stmts)
        Return(TupleExpr(Name("ra"), Name("rb"))))
      Assign(Name("result"), Call(Name("largest_smallest_integers"), list(CS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "largest_smallest_integers" <- ?_:Val ]
                       [ "result" <- tuple(vCons(#if hasNeg(CS) #then maxNeg(CS, 0, false) #else noneV #fi,
                                            vCons(#if hasPos(CS) #then minPos(CS, 0, false) #else noneV #fi, .ValSeq))) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(CS)
    [all-path]
endmodule
