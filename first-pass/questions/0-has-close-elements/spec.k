// spec.k — has_close_elements on the UNIFIED semantics (src/). Nested-loop float existential (the Q43
// shape): inner invariant (idx2-scan) + outer invariant (idx-scan whose body contains the inner For)
// + entry. allFloat(VS) lets the echo reduce numbers[idx]-numbers[idx2]; the pairwise abs<t is the
// opaque closePair. See ./PROOF.md.
//
//   kompile verification.k --backend haskell --main-module HAS-CLOSE-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module HAS-CLOSE-SPEC

requires "verification.k"

module HAS-CLOSE-SPEC
  imports HAS-CLOSE-VERIFICATION

  // ---- INNER loop invariant (idx2-scan, idx fixed) — leaves found := innerFold(J, N, I, VS, T, F).
  claim
    <k>
      #loop(rangeObj(J:Int, N:Int, 1), Name("idx2"),
        If(Compare(Call(Name("abs"), BinOp("-", Subscript(Name("numbers"), Name("idx")), Subscript(Name("numbers"), Name("idx2")))),
             CmpOp("<", Name("threshold"))),
          Assign(Name("found"), Bool(true)),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "has_close_elements" <- _:Val ], parent(-1))
       1 |-> ( scope(.Map [ "numbers" <- list(VS:ValSeq) ] [ "threshold" <- T:Float ] [ "n" <- N:Int ]
                              [ "found" <- F:Bool ] [ "idx" <- I:Int ] [ "idx2" <- _:Val ], parent(0))
               => scope(.Map [ "numbers" <- list(VS) ] [ "threshold" <- T ] [ "n" <- N ]
                              [ "found" <- innerFold(J, N, I, VS, T, F) ] [ "idx" <- I ] [ "idx2" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allFloat(VS) andBool I >=Int 0 andBool J >=Int 0 andBool N ==Int vsLen(VS)
    [all-path]

  // ---- OUTER loop invariant (idx-scan; body = the inner For over idx2 in [idx+1, n)) — leaves
  // found := outerFold(I, N, VS, T, F).
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("idx"),
        For(Name("idx2"), Call(Name("range"), (BinOp("+", Name("idx"), Int(1)), Name("n"))),
          If(Compare(Call(Name("abs"), BinOp("-", Subscript(Name("numbers"), Name("idx")), Subscript(Name("numbers"), Name("idx2")))),
               CmpOp("<", Name("threshold"))),
            Assign(Name("found"), Bool(true)),
            .Stmts)))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "has_close_elements" <- _:Val ], parent(-1))
       1 |-> ( scope(.Map [ "numbers" <- list(VS:ValSeq) ] [ "threshold" <- T:Float ] [ "n" <- N:Int ]
                              [ "found" <- F:Bool ] [ "idx" <- _:Val ] [ "idx2" <- _:Val ], parent(0))
               => scope(.Map [ "numbers" <- list(VS) ] [ "threshold" <- T ] [ "n" <- N ]
                              [ "found" <- outerFold(I, N, VS, T, F) ] [ "idx" <- ?_:Val ] [ "idx2" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allFloat(VS) andBool I >=Int 0 andBool N ==Int vsLen(VS)
    [all-path]

  // ---- Entry claim — result = has_close_elements(list(VS), T) == hceRes(VS, T) =
  // outerFold(0, vsLen(VS), VS, T, false). idx/idx2 pre-bound to 0. Domain allFloat(VS).
  claim
    <k>
      FuncDef("has_close_elements", Params("numbers", "threshold"),
        Assign(Name("found"), Bool(false))
        Assign(Name("n"), Call(Name("len"), Name("numbers")))
        Assign(Name("idx"), Int(0))
        Assign(Name("idx2"), Int(0))
        For(Name("idx"), Call(Name("range"), (Int(0), Name("n"))),
          For(Name("idx2"), Call(Name("range"), (BinOp("+", Name("idx"), Int(1)), Name("n"))),
            If(Compare(Call(Name("abs"), BinOp("-", Subscript(Name("numbers"), Name("idx")), Subscript(Name("numbers"), Name("idx2")))),
                 CmpOp("<", Name("threshold"))),
              Assign(Name("found"), Bool(true)),
              .Stmts)))
        Return(Name("found")))
      Assign(Name("result"), Call(Name("has_close_elements"), (list(VS:ValSeq), T:Float)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "has_close_elements" <- ?_:Val ] [ "result" <- hceRes(VS, T) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allFloat(VS)
    [all-path]
endmodule
