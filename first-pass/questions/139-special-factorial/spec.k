// spec.k — special_factorial proof on the UNIFIED semantics (src/).
//
//   kompile verification.k --backend haskell \
//     --main-module SPECIAL-FACTORIAL-VERIFICATION --syntax-module SPECIAL-FACTORIAL-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module SPECIAL-FACTORIAL-SPEC

requires "verification.k"

module SPECIAL-FACTORIAL-SPEC
  imports SPECIAL-FACTORIAL-VERIFICATION

  // ---- Loop invariant (the circularity) — induction on the index range ------
  // Running `#rangeLoop(I, HI, i, body)` over symbolic (I, HI) updates BOTH coupled
  // accumulators in lockstep:  fact_i := facFold(I,HI,F)  and
  // special_fact := sfacFold(I,HI,F,S)  (the loop var `i` ends at some index → ?_).
  // kprove splits on I >=Int HI (base: scope unchanged, facFold/sfacFold = F/S) and
  // I <Int HI (step: bind i:=I, run body => fact_i=F*I, special_fact=S*(F*I), recurse
  // on (I+1, HI), whose IH closes the fold).
  claim
    <k>
      #loop(rangeObj(I:Int, HI:Int, 1), Name("i"),
        AugAssign(Name("fact_i"), "*", Name("i"))
        AugAssign(Name("special_fact"), "*", Name("fact_i")))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "n" <- NV:Int ]
                              [ "fact_i" <- F:Int ] [ "special_fact" <- S:Int ]
                              [ "i" <- _:Val ], PR:Parent)
               => scope(.Map [ "n" <- NV ]
                              [ "fact_i" <- facFold(I, HI, F) ]
                              [ "special_fact" <- sfacFold(I, HI, F, S) ]
                              [ "i" <- ?_:Val ], PR) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim -----------------------------------------------------------
  // After `result = special_factorial(N)`, the root scope's result is
  // sfacFold(1, N+1, 1, 1) = 1! * 2! * ... * N!  (the super/Brazilian factorial).
  // Domain: N >= 1 (the program's assumed domain, n > 0 per the docstring; the loop
  // `range(1, n+1)` then runs at least once so the loop var `i` is bound, matching the
  // invariant's scope shape).  For N >= 1 we have N+1 > 1 so I=1 < HI=N+1.
  claim
    <k>
      FuncDef("special_factorial", Params("n"),
        Assign(Name("fact_i"), Int(1))
        Assign(Name("special_fact"), Int(1))
        For(Name("i"), Call(Name("range"), (Int(1), BinOp("+", Name("n"), Int(1)))),
          AugAssign(Name("fact_i"), "*", Name("i"))
          AugAssign(Name("special_fact"), "*", Name("fact_i")))
        Return(Name("special_fact")))
      Assign(Name("result"), Call(Name("special_factorial"), Int(N:Int)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "special_factorial" <- ?_:Val ]
                       [ "result" <- sfacFold(1, N +Int 1, 1, 1) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 1
    [all-path]
endmodule
