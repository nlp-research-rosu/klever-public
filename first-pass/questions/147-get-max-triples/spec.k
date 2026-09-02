// spec.k — get_max_triples on the UNIFIED semantics. TRIPLE nested COUNT: innermost k-invariant
// + middle j-invariant + outer i-invariant + entry. Index-based (aVal), no isInt echo. The If
// condition inlines A[i]+A[j]+A[k] as ((i+1)^2-(i+1)+1) + ((j+1)^2-(j+1)+1) + ((k+1)^2-(k+1)+1).
// See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module GET-MAX-TRIPLES-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module GET-MAX-TRIPLES-SPEC

requires "verification.k"

module GET-MAX-TRIPLES-SPEC
  imports GET-MAX-TRIPLES-VERIFICATION

  // The inlined A[x] = (x+1)*(x+1) - (x+1) + 1 for a Name x, as an Expr macro-by-hand.
  // (written out in each claim; kept identical to solution.mpy).

  // ---- INNERMOST k-loop invariant (i, j fixed) -------------------------------
  claim
    <k>
      #loop(rangeObj(K:Int, N:Int, 1), Name("k"),
        If(Compare(BinOp("%",
             BinOp("+",
               BinOp("+",
                 BinOp("+", BinOp("-", BinOp("*", BinOp("+", Name("i"), Int(1)), BinOp("+", Name("i"), Int(1))), BinOp("+", Name("i"), Int(1))), Int(1)),
                 BinOp("+", BinOp("-", BinOp("*", BinOp("+", Name("j"), Int(1)), BinOp("+", Name("j"), Int(1))), BinOp("+", Name("j"), Int(1))), Int(1))),
               BinOp("+", BinOp("-", BinOp("*", BinOp("+", Name("k"), Int(1)), BinOp("+", Name("k"), Int(1))), BinOp("+", Name("k"), Int(1))), Int(1))),
             Int(3)), CmpOp("==", Int(0))),
          Assign(Name("count"), BinOp("+", Name("count"), Int(1))),
          .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "n" <- N:Int ] [ "count" <- C:Int ] [ "i" <- I:Int ] [ "j" <- J:Int ] [ "k" <- _:Val ], PR:Parent)
               => scope(.Map [ "n" <- N ] [ "count" <- kFold(K, N, I, J, C) ] [ "i" <- I ] [ "j" <- J ] [ "k" <- ?_:Val ], PR) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0 andBool J >=Int 0 andBool K >=Int 0
    [all-path]

  // ---- MIDDLE j-loop invariant (i fixed; body contains the k-For) ------------
  claim
    <k>
      #loop(rangeObj(J:Int, N:Int, 1), Name("j"),
        For(Name("k"), Call(Name("range"), (BinOp("+", Name("j"), Int(1)), Name("n"))),
          If(Compare(BinOp("%",
               BinOp("+",
                 BinOp("+",
                   BinOp("+", BinOp("-", BinOp("*", BinOp("+", Name("i"), Int(1)), BinOp("+", Name("i"), Int(1))), BinOp("+", Name("i"), Int(1))), Int(1)),
                   BinOp("+", BinOp("-", BinOp("*", BinOp("+", Name("j"), Int(1)), BinOp("+", Name("j"), Int(1))), BinOp("+", Name("j"), Int(1))), Int(1))),
                 BinOp("+", BinOp("-", BinOp("*", BinOp("+", Name("k"), Int(1)), BinOp("+", Name("k"), Int(1))), BinOp("+", Name("k"), Int(1))), Int(1))),
               Int(3)), CmpOp("==", Int(0))),
            Assign(Name("count"), BinOp("+", Name("count"), Int(1))),
            .Stmts)))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "get_max_triples" <- FB0:Val ], parent(-1))  L |-> ( scope(.Map [ "n" <- N:Int ] [ "count" <- C:Int ] [ "i" <- I:Int ] [ "j" <- _:Val ] [ "k" <- _:Val ], parent(GLB:Int))
               => scope(.Map [ "n" <- N ] [ "count" <- jFold(J, N, I, C) ] [ "i" <- I ] [ "j" <- ?_:Val ] [ "k" <- ?_:Val ], parent(GLB)) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0 andBool J >=Int 0
    [all-path]

  // ---- OUTER i-loop invariant (body contains the j-For, which contains the k-For) ------------
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        For(Name("j"), Call(Name("range"), (BinOp("+", Name("i"), Int(1)), Name("n"))),
          For(Name("k"), Call(Name("range"), (BinOp("+", Name("j"), Int(1)), Name("n"))),
            If(Compare(BinOp("%",
                 BinOp("+",
                   BinOp("+",
                     BinOp("+", BinOp("-", BinOp("*", BinOp("+", Name("i"), Int(1)), BinOp("+", Name("i"), Int(1))), BinOp("+", Name("i"), Int(1))), Int(1)),
                     BinOp("+", BinOp("-", BinOp("*", BinOp("+", Name("j"), Int(1)), BinOp("+", Name("j"), Int(1))), BinOp("+", Name("j"), Int(1))), Int(1))),
                   BinOp("+", BinOp("-", BinOp("*", BinOp("+", Name("k"), Int(1)), BinOp("+", Name("k"), Int(1))), BinOp("+", Name("k"), Int(1))), Int(1))),
                 Int(3)), CmpOp("==", Int(0))),
              Assign(Name("count"), BinOp("+", Name("count"), Int(1))),
              .Stmts))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "get_max_triples" <- FB0:Val ], parent(-1))  L |-> ( scope(.Map [ "n" <- N:Int ] [ "count" <- C:Int ] [ "i" <- _:Val ] [ "j" <- _:Val ] [ "k" <- _:Val ], parent(GLB:Int))
               => scope(.Map [ "n" <- N ] [ "count" <- iFold(I, N, C) ] [ "i" <- ?_:Val ] [ "j" <- ?_:Val ] [ "k" <- ?_:Val ], parent(GLB)) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0
    [all-path]

  // ---- Entry claim -----------------------------------------------------------
  claim
    <k>
      FuncDef("get_max_triples", Params("n"),
        Assign(Name("count"), Int(0))
        Assign(Name("i"), Int(0))
        Assign(Name("j"), Int(0))
        Assign(Name("k"), Int(0))
        For(Name("i"), Call(Name("range"), (Int(0), Name("n"))),
          For(Name("j"), Call(Name("range"), (BinOp("+", Name("i"), Int(1)), Name("n"))),
            For(Name("k"), Call(Name("range"), (BinOp("+", Name("j"), Int(1)), Name("n"))),
              If(Compare(BinOp("%",
                   BinOp("+",
                     BinOp("+",
                       BinOp("+", BinOp("-", BinOp("*", BinOp("+", Name("i"), Int(1)), BinOp("+", Name("i"), Int(1))), BinOp("+", Name("i"), Int(1))), Int(1)),
                       BinOp("+", BinOp("-", BinOp("*", BinOp("+", Name("j"), Int(1)), BinOp("+", Name("j"), Int(1))), BinOp("+", Name("j"), Int(1))), Int(1))),
                     BinOp("+", BinOp("-", BinOp("*", BinOp("+", Name("k"), Int(1)), BinOp("+", Name("k"), Int(1))), BinOp("+", Name("k"), Int(1))), Int(1))),
                   Int(3)), CmpOp("==", Int(0))),
                Assign(Name("count"), BinOp("+", Name("count"), Int(1))),
                .Stmts))))
        Return(Name("count")))
      Assign(Name("result"), Call(Name("get_max_triples"), Int(N:Int)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "get_max_triples" <- ?_:Val ] [ "result" <- maxTriplesRes(N) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
    [all-path]
endmodule
