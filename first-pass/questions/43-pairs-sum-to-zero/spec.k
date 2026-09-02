// spec.k — pairs_sum_to_zero on the UNIFIED semantics. Nested Bool-existential fold: inner
// invariant (j-scan) + outer invariant (i-scan whose body contains the inner For) + entry.
// The allInt(VS) precondition lets the applyBin echo reduce l[i]+l[j] on symbolic elements.
// See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module PAIRS-SUM-TO-ZERO-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module PAIRS-SUM-TO-ZERO-SPEC

requires "verification.k"

module PAIRS-SUM-TO-ZERO-SPEC
  imports PAIRS-SUM-TO-ZERO-VERIFICATION

  // ---- INNER loop invariant (j-scan, i fixed) --------------------------------
  // `for j in range(J, N): if l[i]+l[j]==0: found=True` leaves found := innerFold(J, N, I, VS, F).
  // l/n/i loop-constant; allInt(VS) so the echo reduces l[i]+l[j]; I,J >= 0 so normIdx collapses.
  claim
    <k>
      #loop(rangeObj(J:Int, N:Int, 1), Name("j"),
        If(Compare(BinOp("+", Subscript(Name("l"), Name("i")), Subscript(Name("l"), Name("j"))), CmpOp("==", Int(0))),
          Assign(Name("found"), Bool(true)),
          .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "l" <- list(VS:ValSeq) ] [ "n" <- N:Int ] [ "found" <- F:Bool ]
                              [ "i" <- I:Int ] [ "j" <- _:Val ], PR:Parent)
               => scope(.Map [ "l" <- list(VS) ] [ "n" <- N ] [ "found" <- innerFold(J, N, I, VS, F) ]
                              [ "i" <- I ] [ "j" <- ?_:Val ], PR) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool I >=Int 0 andBool J >=Int 0
    [all-path]

  // ---- OUTER loop invariant (i-scan; body contains the inner For) ------------
  // leaves found := outerFold(I, N, VS, F).  Per iteration the inner For (via the inner invariant)
  // makes found := innerFold(i+1, N, i, VS, found).
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        For(Name("j"), Call(Name("range"), (BinOp("+", Name("i"), Int(1)), Name("n"))),
          If(Compare(BinOp("+", Subscript(Name("l"), Name("i")), Subscript(Name("l"), Name("j"))), CmpOp("==", Int(0))),
            Assign(Name("found"), Bool(true)),
            .Stmts)))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "pairs_sum_to_zero" <- FB0:Val ], parent(-1))  L |-> ( scope(.Map [ "l" <- list(VS:ValSeq) ] [ "n" <- N:Int ] [ "found" <- F:Bool ]
                              [ "i" <- _:Val ] [ "j" <- _:Val ], parent(GLB:Int))
               => scope(.Map [ "l" <- list(VS) ] [ "n" <- N ] [ "found" <- outerFold(I, N, VS, F) ]
                              [ "i" <- ?_:Val ] [ "j" <- ?_:Val ], parent(GLB)) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool I >=Int 0 andBool N ==Int vsLen(VS)
    [all-path]

  // ---- Entry claim -----------------------------------------------------------
  // After `result = pairs_sum_to_zero(list(VS))`, result == pairsRes(VS) = outerFold(0, len, VS,
  // false).  i/j pre-bound to 0 so the outer invariant folds without a first-iteration unroll.
  // Domain allInt(VS) (the problem's "list of integers").
  claim
    <k>
      FuncDef("pairs_sum_to_zero", Params("l"),
        Assign(Name("n"), Call(Name("len"), Name("l")))
        Assign(Name("found"), Bool(false))
        Assign(Name("i"), Int(0))
        Assign(Name("j"), Int(0))
        For(Name("i"), Call(Name("range"), (Int(0), Name("n"))),
          For(Name("j"), Call(Name("range"), (BinOp("+", Name("i"), Int(1)), Name("n"))),
            If(Compare(BinOp("+", Subscript(Name("l"), Name("i")), Subscript(Name("l"), Name("j"))), CmpOp("==", Int(0))),
              Assign(Name("found"), Bool(true)),
              .Stmts)))
        Return(Name("found")))
      Assign(Name("result"), Call(Name("pairs_sum_to_zero"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "pairs_sum_to_zero" <- ?_:Val ] [ "result" <- pairsRes(VS) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]
endmodule
