// spec.k — move_one_ball reachability claims on the UNIFIED semantics (src/).
// solution.py is a cyclic-descent count (the canonical sorted(arr)+rotation compare is not
// modelled). Five accumulators: descents, i, prev, first, and the loop var x.
//
//   kompile verification.k --backend haskell \
//     --main-module MOVE-ONE-BALL-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module MOVE-ONE-BALL-SPEC

requires "verification.k"

module MOVE-ONE-BALL-SPEC
  imports MOVE-ONE-BALL-VERIFICATION

  // ---- Loop invariant (circularity) — from (descents=D, i=I, prev=P, first=F) the loop
  // over VS leaves descents := descCount(VS,I,P,D), i := I +Int vsLen(VS),
  // prev := lastOfV(VS,P), first := firstFold(VS,I,F). Induction on VS; the nested Ifs
  // (i==0 => first=x; i>=1 then x<prev => descents+1) line up with the summaries' branches.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("x"),
        If(Compare(Name("i"), CmpOp("==", Int(0))),
           Assign(Name("first"), Name("x")),
           .Stmts)
        If(Compare(Name("i"), CmpOp(">=", Int(1))),
           If(Compare(Name("x"), CmpOp("<", Name("prev"))),
              Assign(Name("descents"), BinOp("+", Name("descents"), Int(1))),
              .Stmts),
           .Stmts)
        Assign(Name("prev"), Name("x"))
        Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "move_one_ball" <- _:Val ], parent(-1))
       1 |-> (
        scope(.Map [ "arr" <- AV:Val ] [ "descents" <- D:Int ] [ "i" <- I:Int ]
                   [ "prev" <- P:Val ] [ "first" <- F:Val ] [ "x" <- _:Val ], parent(0)) =>
        scope(.Map [ "arr" <- AV ] [ "descents" <- descCount(VS, I, P, D) ]
                   [ "i" <- I +Int vsLen(VS) ] [ "prev" <- lastOfV(VS, P) ]
                   [ "first" <- firstFold(VS, I, F) ] [ "x" <- ?_:Val ], parent(0))
      )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool knownIntM(P) andBool knownIntM(F)
    [all-path]

  // ---- Entry claim — after `result = move_one_ball(list(VS))` the root scope's result is
  //   (descCount(VS,0,0,0) + (1 if lastOfV(VS,0) > firstFold(VS,0,0) else 0)) <= 1
  // i.e. True iff the cyclic-descent count (internal + the wrap last>first) is <= 1. Holds
  // for any symbolic VS under allInt, incl. the empty list (0 descents, 0>0 false => True).
  claim
    <k>
      FuncDef("move_one_ball", Params("arr"),
        Assign(Name("descents"), Int(0))
        Assign(Name("i"), Int(0))
        Assign(Name("prev"), Int(0))
        Assign(Name("first"), Int(0))
        Assign(Name("x"), Int(0))
        For(Name("x"), Name("arr"),
          If(Compare(Name("i"), CmpOp("==", Int(0))),
             Assign(Name("first"), Name("x")),
             .Stmts)
          If(Compare(Name("i"), CmpOp(">=", Int(1))),
             If(Compare(Name("x"), CmpOp("<", Name("prev"))),
                Assign(Name("descents"), BinOp("+", Name("descents"), Int(1))),
                .Stmts),
             .Stmts)
          Assign(Name("prev"), Name("x"))
          Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
        If(Compare(Name("prev"), CmpOp(">", Name("first"))),
           Assign(Name("descents"), BinOp("+", Name("descents"), Int(1))),
           .Stmts)
        Return(Compare(Name("descents"), CmpOp("<=", Int(1)))))
      Assign(Name("result"), Call(Name("move_one_ball"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "move_one_ball" <- ?_:Val ]
                       [ "result" <- ( descCount(VS, 0, 0, 0)
                                       +Int #if projectIntTotal(lastOfV(VS, 0)) >Int projectIntTotal(firstFold(VS, 0, 0))
                                              #then 1 #else 0 #fi ) <=Int 1 ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]
endmodule
