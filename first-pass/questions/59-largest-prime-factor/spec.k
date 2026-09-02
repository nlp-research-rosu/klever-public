// spec.k — largest_prime_factor, TRAP-FREE (P59). Claim 1 = the CALLEE-SPAN
// claim: from is_prime's real loop (early Return inside) down through #pop to
// the result in the CALLER (deallocation restores env/scopeLoc/stack; the
// callee frame is deleted). Claim 2 = the outer invariant with the REAL call
// (Probe A fixed shape; the nested closure lives in frame 1). Claim 3 = entry.
//
//   kompile verification.k --backend haskell --main-module LARGEST-PRIME-FACTOR-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module LARGEST-PRIME-FACTOR-SPEC

requires "verification.k"

module LARGEST-PRIME-FACTOR-SPEC
  imports LARGEST-PRIME-FACTOR-VERIFICATION

  // ---- Claim 1a/1b: callee span — the real loop (early Return inside) folds
  // to primeAcc and the frame pops. Two CLOSED frame shapes: before the first
  // iteration (no i yet) and steady state (i bound) — closed maps keep every
  // bind/lookup natively reducible.
  claim
    <k> #loop(rangeObj(I:Int, HI2:Int, 1), Name("i"),
          If(Compare(BinOp("%", Name("k"), Name("i")), CmpOp("==", Int(0))),
            Return(Bool(false)),
            .Stmts))
        ~> (Return(Bool(true)) .Stmts):Stmts ~> #endcall
     => primeAcc(K, I, HI2, true) ~> CONT </k>
    <env> 2 => 1 </env>
    <scopes> (2 |-> scope((.Map [ "k" <- K:Int ] [ "$cells" <- cellsMark(.ParamNames) ]), parent(0))) SREST:Map
          => SREST </scopes>
    <scopeLoc> _:Int => 2 </scopeLoc>
    <stack> ListItem(frame(CONT:K, 1, 2)) STK:List => STK </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 2 andBool K >=Int 2 andBool notBool 2 in_keys(SREST)
    [all-path]

  claim
    <k> #loop(rangeObj(I:Int, HI2:Int, 1), Name("i"),
          If(Compare(BinOp("%", Name("k"), Name("i")), CmpOp("==", Int(0))),
            Return(Bool(false)),
            .Stmts))
        ~> (Return(Bool(true)) .Stmts):Stmts ~> #endcall
     => primeAcc(K, I, HI2, true) ~> CONT </k>
    <env> 2 => 1 </env>
    <scopes> (2 |-> scope((.Map [ "k" <- K:Int ] [ "$cells" <- cellsMark(.ParamNames) ] [ "i" <- _:Val ]), parent(0))) SREST:Map
          => SREST </scopes>
    <scopeLoc> _:Int => 2 </scopeLoc>
    <stack> ListItem(frame(CONT:K, 1, 2)) STK:List => STK </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 2 andBool K >=Int 2 andBool notBool 2 in_keys(SREST)
    [all-path]

  // ---- Claim 2a/2b: the outer j-loop with the REAL call (fixed shape; closed
  // LHS frames — j absent / bound — with an existential RHS tail)
  claim
    <k>
      #loop(rangeObj(J:Int, HI:Int, 1), Name("j"),
        If(BoolOp("and",
            Compare(BinOp("%", Name("n"), Name("j")), CmpOp("==", Int(0))),
            Call(Name("is_prime"), Name("j"))),
          Assign(Name("largest"), Call(Name("max"), Name("largest"), Name("j"))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "largest_prime_factor" <- LPFV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "n" <- N:Int ] [ "largest" <- ACC:Int ]
                [ "is_prime" <- closureValC("k", .ParamNames,
              If(Compare(Name("k"), CmpOp("<", Int(2))),
                Return(Bool(false)),
                .Stmts)
              For(Name("i"), Call(Name("range"), Int(2), BinOp("-", Name("k"), Int(1))),
                If(Compare(BinOp("%", Name("k"), Name("i")), CmpOp("==", Int(0))),
                  Return(Bool(false)),
                  .Stmts))
              Return(Bool(true)) .Stmts, .Map) ], parent(0))
           => scope((.Map [ "n" <- N ] [ "largest" <- lpfAcc(J, HI, N, ACC) ]
                [ "is_prime" <- ?_:Val ]) ?_:Map, parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires J >=Int 2
    [all-path]

  claim
    <k>
      #loop(rangeObj(J:Int, HI:Int, 1), Name("j"),
        If(BoolOp("and",
            Compare(BinOp("%", Name("n"), Name("j")), CmpOp("==", Int(0))),
            Call(Name("is_prime"), Name("j"))),
          Assign(Name("largest"), Call(Name("max"), Name("largest"), Name("j"))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "largest_prime_factor" <- LPFV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "n" <- N:Int ] [ "largest" <- ACC:Int ]
                [ "is_prime" <- closureValC("k", .ParamNames,
              If(Compare(Name("k"), CmpOp("<", Int(2))),
                Return(Bool(false)),
                .Stmts)
              For(Name("i"), Call(Name("range"), Int(2), BinOp("-", Name("k"), Int(1))),
                If(Compare(BinOp("%", Name("k"), Name("i")), CmpOp("==", Int(0))),
                  Return(Bool(false)),
                  .Stmts))
              Return(Bool(true)) .Stmts, .Map) ] [ "j" <- _:Val ], parent(0))
           => scope((.Map [ "n" <- N ] [ "largest" <- lpfAcc(J, HI, N, ACC) ]
                [ "is_prime" <- ?_:Val ]) ?_:Map, parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires J >=Int 2
    [all-path]

  // ---- Claim 3: entry — result == lpfAcc(2, N+1, N, 1); domain n >= 2
  claim
    <k>
      FuncDef("largest_prime_factor", Params("n"),
        FuncDef("is_prime", Params("k"), CellVars(.ParamNames), FreeVars(.ParamNames),
          If(Compare(Name("k"), CmpOp("<", Int(2))),
          Return(Bool(false)),
          .Stmts)
        For(Name("i"), Call(Name("range"), Int(2), BinOp("-", Name("k"), Int(1))),
          If(Compare(BinOp("%", Name("k"), Name("i")), CmpOp("==", Int(0))),
            Return(Bool(false)),
            .Stmts))
        Return(Bool(true)))
        Assign(Name("largest"), Int(1))
        For(Name("j"), Call(Name("range"), Int(2), BinOp("+", Name("n"), Int(1))),
          If(BoolOp("and",
            Compare(BinOp("%", Name("n"), Name("j")), CmpOp("==", Int(0))),
            Call(Name("is_prime"), Name("j"))),
          Assign(Name("largest"), Call(Name("max"), Name("largest"), Name("j"))),
          .Stmts))
        Return(Name("largest")))
      Assign(Name("result"), Call(Name("largest_prime_factor"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "largest_prime_factor" <- ?_:Val ] [ "result" <- lpfAcc(2, N +Int 1, N, 1) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 2
    [all-path]
endmodule
