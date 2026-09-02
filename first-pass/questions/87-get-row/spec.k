// spec.k — get_row on the UNIFIED semantics (src/). General jagged 2D scan via LOOP INVARIANTS:
// inner (column scan, reverse j=k-1-jj) + outer (row scan, body = k=len(lst[i]) + inner For) + entry.
// Domain allList(VS) (a list of lists). See ./PROOF.md.
//
//   kompile verification.k --backend haskell --main-module GETROW-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module GETROW-SPEC

requires "verification.k"

module GETROW-SPEC
  imports GETROW-VERIFICATION

  // ---- INNER loop invariant (column scan jj in [JJ, K), fixed row i=I) — leaves
  // coords := list(innerFold(JJ, K, I, rowProj(valSeqAt(VS,I)), X, TS)). lst/x/m/i/k loop-constant;
  // allIntGrid(VS) + 0<=I<len bridge lst[i][j] to valSeqAt(rowProj(valSeqAt(VS,I)), j); the cell==x
  // is the REAL Int equality on the cast cell (shared subscript lemma); j = k-1-jj descending.
  claim
    <k>
      #loop(rangeObj(JJ:Int, K:Int, 1), Name("jj"),
        Assign(Name("j"), BinOp("-", BinOp("-", Name("k"), Int(1)), Name("jj")))
        If(Compare(Subscript(Subscript(Name("lst"), Name("i")), Name("j")), CmpOp("==", Name("x"))),
          Assign(Name("coords"), BinOp("+", Name("coords"), ListExpr(TupleExpr(Name("i"), Name("j"))))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "get_row" <- _:Val ], parent(-1))
       1 |-> ( scope(.Map [ "lst" <- list(VS:ValSeq) ] [ "x" <- X:Int ] [ "m" <- M:Int ]
                              [ "coords" <- ref(CN:Int) ] [ "i" <- I:Int ] [ "k" <- K:Int ]
                              [ "jj" <- _:Val ] [ "j" <- _:Val ], parent(0))
               => scope(.Map [ "lst" <- list(VS) ] [ "x" <- X ] [ "m" <- M ]
                              [ "coords" <- ref(?CN2:Int) ] [ "i" <- I ] [ "k" <- K ]
                              [ "jj" <- ?_:Val ] [ "j" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <heap> (CN |-> list(TS:ValSeq)) HREST:Map
        => (?CN2 |-> list(innerFold(JJ, K, I, rowProj(valSeqAt(VS, I)), X, TS))) ?FRESH:Map HREST </heap>
    <heapLoc> HLM:Int => ?HL2:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allIntGrid(VS) andBool 0 <=Int I andBool I <Int vsLen(VS) andBool JJ >=Int 0
     andBool 0 <=Int CN andBool CN <Int HLM andBool keysBelow(HREST, HLM)
    ensures 0 <=Int ?CN2 andBool ?CN2 <Int ?HL2 andBool HLM <=Int ?HL2
     andBool keysBelow(?FRESH, ?HL2)
     andBool notBool (?CN2 in_keys(?FRESH)) andBool notBool (?CN2 in_keys(HREST))
    [all-path]

  // ---- OUTER loop invariant (row scan i in [I, M); body = k=len(lst[i]) + inner For) — leaves
  // coords := list(outerFold(I, M, VS, X, TS)). Each outer step: k := vsLen(rowProj(valSeqAt(VS,i)))
  // (the seqLen bridge), then the inner For folds (via the inner invariant) to innerFold(0,k,i,..).
  claim
    <k>
      #loop(rangeObj(I:Int, M:Int, 1), Name("i"),
        Assign(Name("k"), Call(Name("len"), Subscript(Name("lst"), Name("i"))))
        For(Name("jj"), Call(Name("range"), (Int(0), Name("k"))),
          Assign(Name("j"), BinOp("-", BinOp("-", Name("k"), Int(1)), Name("jj")))
          If(Compare(Subscript(Subscript(Name("lst"), Name("i")), Name("j")), CmpOp("==", Name("x"))),
            Assign(Name("coords"), BinOp("+", Name("coords"), ListExpr(TupleExpr(Name("i"), Name("j"))))),
            .Stmts)))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "get_row" <- _:Val ], parent(-1))
       1 |-> ( scope(.Map [ "lst" <- list(VS:ValSeq) ] [ "x" <- X:Int ] [ "m" <- M:Int ]
                              [ "coords" <- ref(CN:Int) ] [ "i" <- _:Val ] [ "k" <- _:Val ]
                              [ "jj" <- _:Val ] [ "j" <- _:Val ], parent(0))
               => scope(.Map [ "lst" <- list(VS) ] [ "x" <- X ] [ "m" <- M ]
                              [ "coords" <- ref(?CN2:Int) ] [ "i" <- ?_:Val ] [ "k" <- ?_:Val ]
                              [ "jj" <- ?_:Val ] [ "j" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <heap> (CN |-> list(TS:ValSeq)) HREST:Map
        => (?CN2 |-> list(outerFold(I, M, VS, X, TS))) ?FRESH:Map HREST </heap>
    <heapLoc> HLM:Int => ?HL2:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allIntGrid(VS) andBool 0 <=Int I andBool M ==Int vsLen(VS)
     andBool 0 <=Int CN andBool CN <Int HLM andBool keysBelow(HREST, HLM)
    ensures 0 <=Int ?CN2 andBool ?CN2 <Int ?HL2 andBool HLM <=Int ?HL2
     andBool keysBelow(?FRESH, ?HL2)
     andBool notBool (?CN2 in_keys(?FRESH)) andBool notBool (?CN2 in_keys(HREST))
    [all-path]

  // ---- Entry claim — result = get_row(list(VS), X) == list(outerFold(0, vsLen(VS), VS, X, .ValSeq)):
  // the (row asc, col desc) ordered coords of cells equal to x. i/jj/j/k pre-bound to 0. Domain
  // allList(VS).
  claim
    <k>
      FuncDef("get_row", Params("lst", "x"),
        Assign(Name("coords"), ListExpr(.Exprs))
        Assign(Name("m"), Call(Name("len"), Name("lst")))
        Assign(Name("i"), Int(0))
        Assign(Name("jj"), Int(0))
        Assign(Name("j"), Int(0))
        Assign(Name("k"), Int(0))
        For(Name("i"), Call(Name("range"), (Int(0), Name("m"))),
          Assign(Name("k"), Call(Name("len"), Subscript(Name("lst"), Name("i"))))
          For(Name("jj"), Call(Name("range"), (Int(0), Name("k"))),
            Assign(Name("j"), BinOp("-", BinOp("-", Name("k"), Int(1)), Name("jj")))
            If(Compare(Subscript(Subscript(Name("lst"), Name("i")), Name("j")), CmpOp("==", Name("x"))),
              Assign(Name("coords"), BinOp("+", Name("coords"), ListExpr(TupleExpr(Name("i"), Name("j"))))),
              .Stmts)))
        Return(Name("coords")))
      Assign(Name("result"), Call(Name("get_row"), (list(VS:ValSeq), X:Int)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "get_row" <- ?_:Val ]
                       [ "result" <- ref(?RH:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?RH |-> list(outerFold(0, vsLen(VS), VS, X, .ValSeq))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allIntGrid(VS)
    [all-path]
endmodule
