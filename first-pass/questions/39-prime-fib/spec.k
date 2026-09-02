// spec.k — prime_fib, TRAP-FREE (P39). The REAL is_prime runs per candidate:
// its while folds via the inner invariant, the call span folds onto isPrimeV
// via the callee-span claim (the closure verbatim), and the unbounded search
// folds via the co-inductive primeFibFold invariant.
//
//   kompile verification.k --backend haskell --main-module PRIME-FIB-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module PRIME-FIB-SPEC

requires "verification.k"

module PRIME-FIB-SPEC
  imports PRIME-FIB-VERIFICATION

  // ---- is_prime's trial-scan while invariant (env 2 = the is_prime frame) --
  claim
    <k>
      #while(Compare(BinOp("*", Name("k"), Name("k")), CmpOp("<=", Name("p"))),
        If(Compare(BinOp("%", Name("p"), Name("k")), CmpOp("==", Int(0))),
          Assign(Name("pr"), Bool(false)),
          .Stmts)
        Assign(Name("k"), BinOp("+", Name("k"), Int(1))))
    => .K ... </k>
    <env> 2 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "is_prime" <- IPV:Val ] [ "prime_fib" <- PFV:Val ], parent(-1))
       1 |-> scope(.Map [ "a" <- AV:Val ] [ "b" <- BV:Val ] [ "c" <- CV:Val ] [ "n" <- NV:Val ], parent(0))
       2 |-> (
        scope(.Map [ "p" <- P:Int ] [ "pr" <- PR:Bool ] [ "k" <- K:Int ], parent(0)) =>
        scope(.Map [ "p" <- P ] [ "pr" <- prAcc(P, K, PR) ] [ "k" <- ?_:Val ], parent(0))
      )
    </scopes>
    <scopeLoc> 3 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires K >=Int 2
    [all-path]

  // ---- the is_prime CALL SPAN — the real body (closure verbatim) computes
  // isPrimeV(C); heap untouched, frames restored, wind-back per the shared
  // deallocation discipline
  claim
    <k>
      #applyK(toCall(closureVal(("p", .ParamNames),
        If(Compare(Name("p"), CmpOp("<", Int(2))),
          Return(Bool(false)) .Stmts,
          .Stmts)
        Assign(Name("pr"), Bool(true))
        Assign(Name("k"), Int(2))
        While(Compare(BinOp("*", Name("k"), Name("k")), CmpOp("<=", Name("p"))),
          If(Compare(BinOp("%", Name("p"), Name("k")), CmpOp("==", Int(0))),
            Assign(Name("pr"), Bool(false)),
            .Stmts)
          Assign(Name("k"), BinOp("+", Name("k"), Int(1))))
        Return(Name("pr")) .Stmts, 0)), (C:Int, .Vals))
    => isPrimeV(C) ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "is_prime" <- IPV:Val ] [ "prime_fib" <- PFV:Val ], parent(-1))
       1 |-> scope(.Map [ "a" <- AV:Val ] [ "b" <- BV:Val ] [ "c" <- CV:Val ] [ "n" <- NV:Val ], parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> HP:Map </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- the fib search invariant (co-inductive) ------------------------------
  claim
    <k>
      #while(Compare(Name("n"), CmpOp(">", Int(0))),
        Assign(Name("c"), BinOp("+", Name("a"), Name("b")))
        Assign(Name("a"), Name("b"))
        Assign(Name("b"), Name("c"))
        If(Call(Name("is_prime"), Name("c")),
          Assign(Name("n"), BinOp("-", Name("n"), Int(1))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "is_prime" <-
               closureVal(("p", .ParamNames),
                 If(Compare(Name("p"), CmpOp("<", Int(2))),
                   Return(Bool(false)) .Stmts,
                   .Stmts)
                 Assign(Name("pr"), Bool(true))
                 Assign(Name("k"), Int(2))
                 While(Compare(BinOp("*", Name("k"), Name("k")), CmpOp("<=", Name("p"))),
                   If(Compare(BinOp("%", Name("p"), Name("k")), CmpOp("==", Int(0))),
                     Assign(Name("pr"), Bool(false)),
                     .Stmts)
                   Assign(Name("k"), BinOp("+", Name("k"), Int(1))))
                 Return(Name("pr")) .Stmts, 0) ]
             [ "prime_fib" <- PFV:Val ], parent(-1))
       1 |-> (
        scope(.Map [ "a" <- A:Int ] [ "b" <- B:Int ] [ "c" <- _:Val ] [ "n" <- N:Int ], parent(0)) =>
        scope(.Map [ "a" <- ?_:Val ] [ "b" <- primeFibFold(A, B, N) ] [ "c" <- ?_:Val ] [ "n" <- ?_:Val ], parent(0))
      )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
    [all-path]

  // ---- Entry — result = prime_fib(N), both defs verbatim ---------------------
  claim
    <k>
      FuncDef("is_prime", Params("p"),
        If(Compare(Name("p"), CmpOp("<", Int(2))),
          Return(Bool(false)) .Stmts,
          .Stmts)
        Assign(Name("pr"), Bool(true))
        Assign(Name("k"), Int(2))
        While(Compare(BinOp("*", Name("k"), Name("k")), CmpOp("<=", Name("p"))),
          If(Compare(BinOp("%", Name("p"), Name("k")), CmpOp("==", Int(0))),
            Assign(Name("pr"), Bool(false)),
            .Stmts)
          Assign(Name("k"), BinOp("+", Name("k"), Int(1))))
        Return(Name("pr")))
      FuncDef("prime_fib", Params("n"),
        Assign(Name("a"), Int(0))
        Assign(Name("b"), Int(1))
        Assign(Name("c"), Int(0))
        While(Compare(Name("n"), CmpOp(">", Int(0))),
          Assign(Name("c"), BinOp("+", Name("a"), Name("b")))
          Assign(Name("a"), Name("b"))
          Assign(Name("b"), Name("c"))
          If(Call(Name("is_prime"), Name("c")),
            Assign(Name("n"), BinOp("-", Name("n"), Int(1))),
            .Stmts))
        Return(Name("b")))
      Assign(Name("result"), Call(Name("prime_fib"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "is_prime" <- ?_:Val ] [ "prime_fib" <- ?_:Val ]
                       [ "result" <- primeFibRes(N) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 1
    [all-path]
endmodule
