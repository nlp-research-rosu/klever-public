// spec.k — count_up_to, TRAP-FREE (P96). Inner trial-division invariant (the
// break exits within the loop — no pop; single uniform claim per frame shape),
// outer append invariant containing the inner For (nested-loop rung, Probe-B
// fixed ref), entry with the existential result ref.
//
//   kompile verification.k --backend haskell --main-module COUNT-UP-TO-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module COUNT-UP-TO-SPEC

requires "verification.k"

module COUNT-UP-TO-SPEC
  imports COUNT-UP-TO-VERIFICATION

  claim
    <k>
      #loop(rangeObj(J:Int, IHI:Int, 1), Name("j"),
        If(Compare(BinOp("%", Name("i"), Name("j")), CmpOp("==", Int(0))),
          Assign(Name("is_prime"), Bool(false))
          Break,
          .Stmts))
    => .K ... </k>
    <env> L0:Int </env>
    <scopes>
      ... L0 |-> ( scope(.Map [ "n" <- NV:Val ] [ "primes" <- PV:Val ] [ "i" <- I:Int ]
                              [ "is_prime" <- true ], PR:Parent)
               => scope((.Map [ "n" <- NV ] [ "primes" <- PV ] [ "i" <- I ]
                              [ "is_prime" <- primeAcc(I, J, IHI, true) ]) [ "j" <- ?_:Val ], PR) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires J >=Int 2 andBool J <Int IHI
    [all-path]

  claim
    <k>
      #loop(rangeObj(J:Int, IHI:Int, 1), Name("j"),
        If(Compare(BinOp("%", Name("i"), Name("j")), CmpOp("==", Int(0))),
          Assign(Name("is_prime"), Bool(false))
          Break,
          .Stmts))
    => .K ... </k>
    <env> L0:Int </env>
    <scopes>
      ... L0 |-> ( scope(.Map [ "n" <- NV:Val ] [ "primes" <- PV:Val ] [ "i" <- I:Int ]
                              [ "is_prime" <- true ] [ "j" <- _:Val ], PR:Parent)
               => scope((.Map [ "n" <- NV ] [ "primes" <- PV ] [ "i" <- I ]
                              [ "is_prime" <- primeAcc(I, J, IHI, true) ]) [ "j" <- ?_:Val ], PR) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires J >=Int 2
    [all-path]

  claim
    <k>
      #loop(rangeObj(I2:Int, HI:Int, 1), Name("i"),
        Assign(Name("is_prime"), Bool(true))
        For(Name("j"), Call(Name("range"), Int(2), Name("i")),
          If(Compare(BinOp("%", Name("i"), Name("j")), CmpOp("==", Int(0))),
            Assign(Name("is_prime"), Bool(false))
            Break,
            .Stmts))
        If(Name("is_prime"),
          Expr(Call(Attribute(Name("primes"), "append"), Name("i"))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "count_up_to" <- CUV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "n" <- NV:Val ] [ "primes" <- ref(LR:Int) ], parent(0))
           => scope((.Map [ "n" <- NV ] [ "primes" <- ref(LR) ]) ?_:Map, parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (LR |-> list(ACC:ValSeq)) HREST:Map
        => (LR |-> list(primesUpTo(I2, HI, ACC))) HREST </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I2 >=Int 2 andBool I2 <Int HI
    [all-path]

  claim
    <k>
      #loop(rangeObj(I2:Int, HI:Int, 1), Name("i"),
        Assign(Name("is_prime"), Bool(true))
        For(Name("j"), Call(Name("range"), Int(2), Name("i")),
          If(Compare(BinOp("%", Name("i"), Name("j")), CmpOp("==", Int(0))),
            Assign(Name("is_prime"), Bool(false))
            Break,
            .Stmts))
        If(Name("is_prime"),
          Expr(Call(Attribute(Name("primes"), "append"), Name("i"))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "count_up_to" <- CUV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "n" <- NV:Val ] [ "primes" <- ref(LR:Int) ] [ "i" <- _:Val ] [ "is_prime" <- _:Val ] [ "j" <- _:Val ], parent(0))
           => scope((.Map [ "n" <- NV ] [ "primes" <- ref(LR) ]) ?_:Map, parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (LR |-> list(ACC:ValSeq)) HREST:Map
        => (LR |-> list(primesUpTo(I2, HI, ACC))) HREST </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I2 >=Int 2
    [all-path]

  claim
    <k>
      #loop(rangeObj(I2:Int, HI:Int, 1), Name("i"),
        Assign(Name("is_prime"), Bool(true))
        For(Name("j"), Call(Name("range"), Int(2), Name("i")),
          If(Compare(BinOp("%", Name("i"), Name("j")), CmpOp("==", Int(0))),
            Assign(Name("is_prime"), Bool(false))
            Break,
            .Stmts))
        If(Name("is_prime"),
          Expr(Call(Attribute(Name("primes"), "append"), Name("i"))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "count_up_to" <- CUV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "n" <- NV:Val ] [ "primes" <- ref(LR:Int) ] [ "i" <- _:Val ] [ "is_prime" <- _:Val ], parent(0))
           => scope((.Map [ "n" <- NV ] [ "primes" <- ref(LR) ]) ?_:Map, parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (LR |-> list(ACC:ValSeq)) HREST:Map
        => (LR |-> list(primesUpTo(I2, HI, ACC))) HREST </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I2 >=Int 2
    [all-path]


  claim
    <k>
      FuncDef("count_up_to", Params("n"),
        Assign(Name("primes"), ListExpr(.Exprs))
        For(Name("i"), Call(Name("range"), Int(2), Name("n")),
          Assign(Name("is_prime"), Bool(true))
        For(Name("j"), Call(Name("range"), Int(2), Name("i")),
          If(Compare(BinOp("%", Name("i"), Name("j")), CmpOp("==", Int(0))),
            Assign(Name("is_prime"), Bool(false))
            Break,
            .Stmts))
        If(Name("is_prime"),
          Expr(Call(Attribute(Name("primes"), "append"), Name("i"))),
          .Stmts))
        Return(Name("primes")))
      Assign(Name("result"), Call(Name("count_up_to"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "count_up_to" <- ?_:Val ] [ "result" <- ref(?NO:Int) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => (?NO |-> list(primesUpTo(2, N, .ValSeq))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 3
    [all-path]
endmodule
