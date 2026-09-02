// spec.k — search on the UNIFIED semantics. Nested COUNT + MAX: inner count invariant + outer
// search invariant (body contains the inner For) + entry. allInt(VS) lets the mixed echo reduce
// lst[j]==v. See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module SEARCH-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module SEARCH-SPEC

requires "verification.k"

module SEARCH-SPEC
  imports SEARCH-VERIFICATION

  // ---- INNER count invariant (v fixed): cnt := countFold(J, N, V, VS, C). ----------------------
  claim
    <k>
      #loop(rangeObj(J:Int, N:Int, 1), Name("j"),
        If(Compare(Subscript(Name("lst"), Name("j")), CmpOp("==", Name("v"))),
          Assign(Name("cnt"), BinOp("+", Name("cnt"), Int(1))),
          .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "lst" <- list(VS:ValSeq) ] [ "n" <- N:Int ] [ "ans" <- A:Int ]
                              [ "v" <- V:Int ] [ "cnt" <- C:Int ] [ "j" <- _:Val ], PR:Parent)
               => scope(.Map [ "lst" <- list(VS) ] [ "n" <- N ] [ "ans" <- A ]
                              [ "v" <- V ] [ "cnt" <- countFold(J, N, V, VS, C) ] [ "j" <- ?_:Val ], PR) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool J >=Int 0
    [all-path]

  // ---- OUTER search invariant (body contains the count For): ans := searchFold(V, HI, VS, N, A). --
  claim
    <k>
      #loop(rangeObj(V:Int, HI:Int, 1), Name("v"),
        Assign(Name("cnt"), Int(0))
        For(Name("j"), Call(Name("range"), (Int(0), Name("n"))),
          If(Compare(Subscript(Name("lst"), Name("j")), CmpOp("==", Name("v"))),
            Assign(Name("cnt"), BinOp("+", Name("cnt"), Int(1))),
            .Stmts))
        If(Compare(Name("cnt"), CmpOp(">=", Name("v"))),
          Assign(Name("ans"), Name("v")),
          .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "search" <- FB0:Val ], parent(-1))  L |-> ( scope(.Map [ "lst" <- list(VS:ValSeq) ] [ "n" <- N:Int ] [ "ans" <- A:Int ]
                              [ "v" <- _:Val ] [ "cnt" <- _:Val ] [ "j" <- _:Val ], parent(GLB:Int))
               => scope(.Map [ "lst" <- list(VS) ] [ "n" <- N ] [ "ans" <- searchFold(V, HI, VS, N, A) ]
                              [ "v" <- ?_:Val ] [ "cnt" <- ?_:Val ] [ "j" <- ?_:Val ], parent(GLB)) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]

  // ---- Entry claim -----------------------------------------------------------
  claim
    <k>
      FuncDef("search", Params("lst"),
        Assign(Name("n"), Call(Name("len"), Name("lst")))
        Assign(Name("ans"), UnaryOp("-", Int(1)))
        Assign(Name("v"), Int(0))
        Assign(Name("j"), Int(0))
        Assign(Name("cnt"), Int(0))
        For(Name("v"), Call(Name("range"), (Int(1), BinOp("+", Name("n"), Int(1)))),
          Assign(Name("cnt"), Int(0))
          For(Name("j"), Call(Name("range"), (Int(0), Name("n"))),
            If(Compare(Subscript(Name("lst"), Name("j")), CmpOp("==", Name("v"))),
              Assign(Name("cnt"), BinOp("+", Name("cnt"), Int(1))),
              .Stmts))
          If(Compare(Name("cnt"), CmpOp(">=", Name("v"))),
            Assign(Name("ans"), Name("v")),
            .Stmts))
        Return(Name("ans")))
      Assign(Name("result"), Call(Name("search"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "search" <- ?_:Val ] [ "result" <- searchRes(VS) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool vsLen(VS) >=Int 1
    [all-path]
endmodule
