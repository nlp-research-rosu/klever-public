// spec.k — triples_sum_to_zero on the UNIFIED semantics. TRIPLE nested Bool-existential fold:
// innermost k-invariant + middle j-invariant + outer i-invariant + entry. allInt(VS) lets the
// applyBin echoes reduce l[i]+l[j]+l[k]. See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module TRIPLES-SUM-TO-ZERO-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module TRIPLES-SUM-TO-ZERO-SPEC

requires "verification.k"

module TRIPLES-SUM-TO-ZERO-SPEC
  imports TRIPLES-SUM-TO-ZERO-VERIFICATION

  // ---- INNERMOST k-loop invariant (i, j fixed) -------------------------------
  claim
    <k>
      #loop(rangeObj(K:Int, N:Int, 1), Name("k"),
        If(Compare(BinOp("+", BinOp("+", Subscript(Name("l"), Name("i")), Subscript(Name("l"), Name("j"))), Subscript(Name("l"), Name("k"))),
             CmpOp("==", Int(0))),
          Assign(Name("found"), Bool(true)),
          .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "l" <- list(VS:ValSeq) ] [ "n" <- N:Int ] [ "found" <- F:Bool ]
                              [ "i" <- I:Int ] [ "j" <- J:Int ] [ "k" <- _:Val ], PR:Parent)
               => scope(.Map [ "l" <- list(VS) ] [ "n" <- N ] [ "found" <- kFold(K, N, I, J, VS, F) ]
                              [ "i" <- I ] [ "j" <- J ] [ "k" <- ?_:Val ], PR) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool I >=Int 0 andBool J >=Int 0 andBool K >=Int 0
    [all-path]

  // ---- MIDDLE j-loop invariant (i fixed; body contains the k-For) ------------
  claim
    <k>
      #loop(rangeObj(J:Int, N:Int, 1), Name("j"),
        For(Name("k"), Call(Name("range"), (BinOp("+", Name("j"), Int(1)), Name("n"))),
          If(Compare(BinOp("+", BinOp("+", Subscript(Name("l"), Name("i")), Subscript(Name("l"), Name("j"))), Subscript(Name("l"), Name("k"))),
               CmpOp("==", Int(0))),
            Assign(Name("found"), Bool(true)),
            .Stmts)))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "triples_sum_to_zero" <- FB0:Val ], parent(-1))  L |-> ( scope(.Map [ "l" <- list(VS:ValSeq) ] [ "n" <- N:Int ] [ "found" <- F:Bool ]
                              [ "i" <- I:Int ] [ "j" <- _:Val ] [ "k" <- _:Val ], parent(GLB:Int))
               => scope(.Map [ "l" <- list(VS) ] [ "n" <- N ] [ "found" <- jFold(J, N, I, VS, F) ]
                              [ "i" <- I ] [ "j" <- ?_:Val ] [ "k" <- ?_:Val ], parent(GLB)) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool I >=Int 0 andBool J >=Int 0
    [all-path]

  // ---- OUTER i-loop invariant (body contains the j-For, which contains the k-For) ------------
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        For(Name("j"), Call(Name("range"), (BinOp("+", Name("i"), Int(1)), Name("n"))),
          For(Name("k"), Call(Name("range"), (BinOp("+", Name("j"), Int(1)), Name("n"))),
            If(Compare(BinOp("+", BinOp("+", Subscript(Name("l"), Name("i")), Subscript(Name("l"), Name("j"))), Subscript(Name("l"), Name("k"))),
                 CmpOp("==", Int(0))),
              Assign(Name("found"), Bool(true)),
              .Stmts))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "triples_sum_to_zero" <- FB0:Val ], parent(-1))  L |-> ( scope(.Map [ "l" <- list(VS:ValSeq) ] [ "n" <- N:Int ] [ "found" <- F:Bool ]
                              [ "i" <- _:Val ] [ "j" <- _:Val ] [ "k" <- _:Val ], parent(GLB:Int))
               => scope(.Map [ "l" <- list(VS) ] [ "n" <- N ] [ "found" <- iFold(I, N, VS, F) ]
                              [ "i" <- ?_:Val ] [ "j" <- ?_:Val ] [ "k" <- ?_:Val ], parent(GLB)) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool I >=Int 0
    [all-path]

  // ---- Entry claim -----------------------------------------------------------
  claim
    <k>
      FuncDef("triples_sum_to_zero", Params("l"),
        Assign(Name("n"), Call(Name("len"), Name("l")))
        Assign(Name("found"), Bool(false))
        Assign(Name("i"), Int(0))
        Assign(Name("j"), Int(0))
        Assign(Name("k"), Int(0))
        For(Name("i"), Call(Name("range"), (Int(0), Name("n"))),
          For(Name("j"), Call(Name("range"), (BinOp("+", Name("i"), Int(1)), Name("n"))),
            For(Name("k"), Call(Name("range"), (BinOp("+", Name("j"), Int(1)), Name("n"))),
              If(Compare(BinOp("+", BinOp("+", Subscript(Name("l"), Name("i")), Subscript(Name("l"), Name("j"))), Subscript(Name("l"), Name("k"))),
                   CmpOp("==", Int(0))),
                Assign(Name("found"), Bool(true)),
                .Stmts))))
        Return(Name("found")))
      Assign(Name("result"), Call(Name("triples_sum_to_zero"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "triples_sum_to_zero" <- ?_:Val ] [ "result" <- triplesRes(VS) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]
endmodule
