// spec.k — by_length on the UNIFIED semantics (src/). One build-loop invariant (descending read of
// the trusted sorted list + filter 1..9 + word map) + entry. See ./PROOF.md.
//
//   kompile verification.k --backend haskell --main-module BYLEN-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module BYLEN-SPEC

requires "verification.k"

module BYLEN-SPEC
  imports BYLEN-VERIFICATION

  // ---- BUILD loop invariant — `for i in range(0,n): v = s[n-1-i]; if v>=1: if v<=9: result += [word(v)]`
  // leaves result := list(buildFold(I, N, SS, RACC)). s = list(SS) FRESH (only indexed); arr/n/s
  // loop-constant. I>=0 (with I<N in the step) so the descending index normIdx collapses.
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        Assign(Name("v"), Subscript(Name("s"), BinOp("-", BinOp("-", Name("n"), Int(1)), Name("i"))))
        If(Compare(Name("v"), CmpOp(">=", Int(1))),
          If(Compare(Name("v"), CmpOp("<=", Int(9))),
            Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Call(Name("word"), Name("v"))))),
            .Stmts),
          .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "arr" <- AV:Val ] [ "n" <- N:Int ] [ "s" <- list(SS:ValSeq) ]
                              [ "result" <- list(RACC:ValSeq) ] [ "i" <- _:Val ] [ "v" <- _:Val ], PR:Parent)
               => scope(.Map [ "arr" <- AV ] [ "n" <- N ] [ "s" <- list(SS) ]
                              [ "result" <- list(buildFold(I, N, SS, RACC)) ] [ "i" <- ?_:Val ] [ "v" <- ?_:Val ], PR) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0 andBool allInt(SS)
    [all-path]

  // ---- Entry claim — result = by_length(list(VS)) == list(buildFold(0, len, sortVS(VS), .ValSeq)).
  // s := sorted = list(sortVS(VS)); the descending filter+word-map loop folds. `word` is intercepted
  // (opaque wordV), so no word FuncDef in the claim; it runs for real in krun.
  claim
    <k>
      FuncDef("by_length", Params("arr"),
        Assign(Name("n"), Call(Name("len"), Name("arr")))
        Assign(Name("s"), Call(Name("sorted"), Name("arr")))
        Assign(Name("result"), ListExpr(.Exprs))
        Assign(Name("i"), Int(0))
        Assign(Name("v"), Int(0))
        For(Name("i"), Call(Name("range"), (Int(0), Name("n"))),
          Assign(Name("v"), Subscript(Name("s"), BinOp("-", BinOp("-", Name("n"), Int(1)), Name("i"))))
          If(Compare(Name("v"), CmpOp(">=", Int(1))),
            If(Compare(Name("v"), CmpOp("<=", Int(9))),
              Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Call(Name("word"), Name("v"))))),
              .Stmts),
            .Stmts))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("by_length"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "by_length" <- ?_:Val ]
                       [ "result" <- list(buildFold(0, vsLen(VS), sortVS(VS), .ValSeq)) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]
endmodule
