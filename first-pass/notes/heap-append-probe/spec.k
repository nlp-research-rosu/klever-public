// spec.k — Probe B: heap-list builders. Claim 1 = append-loop invariant (fixed ref,
// heap rest LITERALLY unchanged — no allocation in the body). Claim 2 = plus-builder
// invariant (two allocations per iteration; the accumulator ref MOVES; garbage absorbed
// by the abstract heap rest + keysBelow premises). Claims 3/4 = entries with an
// existential result ref.
//
//   kompile verification.k --backend haskell \
//     --main-module HEAP-APPEND-PROBE-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module HEAP-APPEND-PROBE-SPEC

requires "verification.k"

module HEAP-APPEND-PROBE-SPEC
  imports HEAP-APPEND-PROBE-VERIFICATION

  // ---- Claim 1: append-loop invariant. result's heap entry folds in place; the
  // body never allocates, so the heap rest and heapLoc are untouched (both pinned).
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        Expr(Call(Attribute(Name("result"), "append"), BinOp("*", Name("i"), Name("i")))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "n" <- NV:Val ] [ "result" <- ref(RN:Int) ] [ "i" <- _:Val ], PR:Parent)
               => scope(.Map [ "n" <- NV ] [ "result" <- ref(RN) ] [ "i" <- ?_:Val ], PR) ) ...
    </scopes>
    <heap> (RN |-> list(ACC:ValSeq)) HREST:Map
        => (RN |-> list(sqFold(I, N, ACC))) HREST </heap>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Claim 2: plus-builder invariant. Each iteration allocates the [i] literal
  // and the concatenation result; `out` rebinds to the fresh ref. keysBelow lets the
  // allocator's freshness guard discharge against the abstract rest.
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        Assign(Name("out"), BinOp("+", Name("out"), ListExpr(Name("i")))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "n" <- NV:Val ] [ "out" <- ref(ON:Int) ] [ "i" <- _:Val ], PR:Parent)
               => scope(.Map [ "n" <- NV ] [ "out" <- ref(?ON2:Int) ] [ "i" <- ?_:Val ], PR) ) ...
    </scopes>
    <heap> (ON |-> list(ACC:ValSeq)) HREST:Map
        => (?ON2 |-> list(plusFold(I, N, ACC))) ?_:Map </heap>
    <heapLoc> HL:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int ON andBool ON <Int HL andBool keysBelow(HREST, HL)
    [all-path]

  // ---- Claim 3: entry (append builder) — res = build_squares(N), an existential
  // result ref whose heap entry holds the fold.
  claim
    <k>
      FuncDef("build_squares", Params("n"),
        Assign(Name("result"), ListExpr(.Exprs))
        Assign(Name("i"), Int(0))
        For(Name("i"), Call(Name("range"), Name("n")),
          Expr(Call(Attribute(Name("result"), "append"), BinOp("*", Name("i"), Name("i")))))
        Return(Name("result")))
      Assign(Name("res"), Call(Name("build_squares"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "build_squares" <- ?_:Val ] [ "res" <- ref(?NO:Int) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => (?NO |-> list(sqFold(0, N, .ValSeq))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Claim 4: entry (plus builder) — the final heap carries garbage; the result
  // entry is found by unification.
  claim
    <k>
      FuncDef("build_plus", Params("n"),
        Assign(Name("out"), ListExpr(.Exprs))
        Assign(Name("i"), Int(0))
        For(Name("i"), Call(Name("range"), Name("n")),
          Assign(Name("out"), BinOp("+", Name("out"), ListExpr(Name("i")))))
        Return(Name("out")))
      Assign(Name("res"), Call(Name("build_plus"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "build_plus" <- ?_:Val ] [ "res" <- ref(?NO:Int) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => (?NO |-> list(plusFold(0, N, .ValSeq))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
