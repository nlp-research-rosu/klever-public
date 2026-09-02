// spec.k — pluck reachability claims on the UNIFIED semantics (src/).
// solution.py is a single indexed scan (the canonical filter/min/arr.index is not
// modelled). Four accumulators: found, bestVal, bestIdx, and a position counter i.
//
//   kompile verification.k --backend haskell \
//     --main-module PLUCK-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module PLUCK-SPEC

requires "verification.k"

module PLUCK-SPEC
  imports PLUCK-VERIFICATION

  // ---- Loop invariant (circularity) — running the scan over VS from (found=F, bestVal=BV,
  // bestIdx=BI, i=I) leaves found := pFound(VS,F,BV,BI,I), bestVal := pBest(VS,F,BV,BI,I),
  // bestIdx := pIdx(VS,F,BV,BI,I), i := I +Int vsLen(VS). Induction on VS; the body's nested
  // Ifs split on v%2==0, then (not found), then v<bestVal — the folds' branch predicates.
  // isInt(BV) so the v<bestVal / v%2 casts fire; allInt(VS) so each element projects.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("v"),
        If(Compare(BinOp("%", Name("v"), Int(2)), CmpOp("==", Int(0))),
          If(UnaryOp("not", Name("found")),
            Assign(Name("bestVal"), Name("v"))
            Assign(Name("bestIdx"), Name("i"))
            Assign(Name("found"), Bool(true)),
            If(Compare(Name("v"), CmpOp("<", Name("bestVal"))),
              Assign(Name("bestVal"), Name("v"))
              Assign(Name("bestIdx"), Name("i")),
              .Stmts)),
          .Stmts)
        Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "pluck" <- _:Val ], parent(-1))
       1 |-> (
        scope(.Map [ "arr" <- AV:Val ] [ "i" <- I:Int ] [ "found" <- F:Bool ]
                   [ "bestVal" <- BV:Val ] [ "bestIdx" <- BI:Int ] [ "v" <- _:Val ], parent(0)) =>
        scope(.Map [ "arr" <- AV ] [ "i" <- I +Int vsLen(VS) ] [ "found" <- pFound(VS, F, BV, BI, I) ]
                   [ "bestVal" <- pBest(VS, F, BV, BI, I) ] [ "bestIdx" <- pIdx(VS, F, BV, BI, I) ]
                   [ "v" <- ?_:Val ], parent(0))
      )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool isInt(BV)
    [all-path]

  // ---- Entry, found case: result = [min even, its first index] ------------
  claim
    <k>
      FuncDef("pluck", Params("arr"),
        Assign(Name("i"), Int(0))
        Assign(Name("found"), Bool(false))
        Assign(Name("bestVal"), Int(0))
        Assign(Name("bestIdx"), Int(0))
        Assign(Name("v"), Int(0))
        For(Name("v"), Name("arr"),
          If(Compare(BinOp("%", Name("v"), Int(2)), CmpOp("==", Int(0))),
            If(UnaryOp("not", Name("found")),
              Assign(Name("bestVal"), Name("v"))
              Assign(Name("bestIdx"), Name("i"))
              Assign(Name("found"), Bool(true)),
              If(Compare(Name("v"), CmpOp("<", Name("bestVal"))),
                Assign(Name("bestVal"), Name("v"))
                Assign(Name("bestIdx"), Name("i")),
                .Stmts)),
            .Stmts)
          Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
        If(Name("found"),
          Return(ListExpr(Name("bestVal"), Name("bestIdx"))),
          Return(ListExpr(.Exprs))))
      Assign(Name("result"), Call(Name("pluck"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "pluck" <- ?_:Val ] [ "result" <- ref(?RH:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?RH |-> list(vCons(pBest(VS, false, 0, 0, 0), vCons(pIdx(VS, false, 0, 0, 0), .ValSeq)))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool pFound(VS, false, 0, 0, 0)
    [all-path]

  // ---- Entry, no-even case: result = [] ------------------------------------
  claim
    <k>
      FuncDef("pluck", Params("arr"),
        Assign(Name("i"), Int(0))
        Assign(Name("found"), Bool(false))
        Assign(Name("bestVal"), Int(0))
        Assign(Name("bestIdx"), Int(0))
        Assign(Name("v"), Int(0))
        For(Name("v"), Name("arr"),
          If(Compare(BinOp("%", Name("v"), Int(2)), CmpOp("==", Int(0))),
            If(UnaryOp("not", Name("found")),
              Assign(Name("bestVal"), Name("v"))
              Assign(Name("bestIdx"), Name("i"))
              Assign(Name("found"), Bool(true)),
              If(Compare(Name("v"), CmpOp("<", Name("bestVal"))),
                Assign(Name("bestVal"), Name("v"))
                Assign(Name("bestIdx"), Name("i")),
                .Stmts)),
            .Stmts)
          Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
        If(Name("found"),
          Return(ListExpr(Name("bestVal"), Name("bestIdx"))),
          Return(ListExpr(.Exprs))))
      Assign(Name("result"), Call(Name("pluck"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "pluck" <- ?_:Val ] [ "result" <- ref(?RH:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?RH |-> list(.ValSeq)) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool notBool pFound(VS, false, 0, 0, 0)
    [all-path]
endmodule
