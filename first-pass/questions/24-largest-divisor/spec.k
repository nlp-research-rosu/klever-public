// spec.k — largest_divisor proof on the UNIFIED semantics (src/).
//
//   kompile verification.k --backend haskell \
//     --main-module LARGEST-DIVISOR-VERIFICATION --syntax-module LARGEST-DIVISOR-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module LARGEST-DIVISOR-SPEC

requires "verification.k"

module LARGEST-DIVISOR-SPEC
  imports LARGEST-DIVISOR-VERIFICATION

  // ---- Loop invariant (the circularity) — induction on the gap (HI - I) -------
  // Running the ASCENDING sticky scan `#rangeLoop(I, HI, i, BODY)` over symbolic
  // bounds leaves result := lastDiv(N, I, HI, R) (n constant; i ends bound to some
  // index -> ?_).  kprove splits I into >=Int HI (base: empty range, scope
  // unchanged, lastDiv = R) and <Int HI (step: bind i:=I, run the If; the
  // `n % i == 0` sub-split either updates result := I and recurses, or leaves
  // result and recurses — exactly lastDiv's two recursive rules).  The body has NO
  // return, so the loop runs to completion and result lands in <scopes>; the <k>
  // ends in `.K`.  Proven by induction on (HI - I) via the I<HI / I>=HI split
  // (cf. 49-modp / 31-is-prime / 35-max-element).
  claim
    <k>
      #loop(rangeObj(I:Int, HI:Int, 1), Name("i"),
        If(Compare(BinOp("%", Name("n"), Name("i")), CmpOp("==", Int(0))),
           Assign(Name("result"), Name("i")),
           .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "n" <- N:Int ] [ "result" <- R:Int ] [ "i" <- _:Val ], P:Parent)
               => scope(.Map [ "n" <- N ] [ "result" <- lastDiv(N, I, HI, R) ] [ "i" <- ?_:Val ], P) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim -----------------------------------------------------------
  // After `result = largest_divisor(N)`, the root scope's result is bound to
  // lastDiv(N, 1, N, 1) — the LARGEST i in [1, N) with N % i == 0 (the largest
  // proper divisor of N), with floor 1 (handles N prime).  Domain: N >= 2 (the
  // program's assumed domain; canonical reversed(range(n)) reaches i = 0 / n % 0
  // for n < 2, a ZeroDivisionError, which is out of domain).  For N >= 2 the loop
  // body's `range(1, N)` is non-empty, so result is set to at least 1.
  claim
    <k>
      FuncDef("largest_divisor", Params("n"),
        Assign(Name("result"), Int(1))
        For(Name("i"), Call(Name("range"), (Int(1), Name("n"))),
          If(Compare(BinOp("%", Name("n"), Name("i")), CmpOp("==", Int(0))),
             Assign(Name("result"), Name("i")),
             .Stmts))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("largest_divisor"), Int(N:Int)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "largest_divisor" <- ?_:Val ]
                       [ "result" <- lastDiv(N, 1, N, 1) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 2
    [all-path]
endmodule
