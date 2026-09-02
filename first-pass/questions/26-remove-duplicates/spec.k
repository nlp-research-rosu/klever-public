// spec.k — remove_duplicates on the UNIFIED semantics (src/). Index-based nested double loop: inner
// invariant (j-scan counts numbers[j]==numbers[i]) + outer invariant (i-scan whose body contains the
// inner For, the c-reset, and the count==1 append) + entry. allInt(VS) lets the applyCmp echo reduce
// numbers[j]==numbers[i] on symbolic elements. See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module REMOVE-DUPLICATES-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module REMOVE-DUPLICATES-SPEC

requires "verification.k"

module REMOVE-DUPLICATES-SPEC
  imports REMOVE-DUPLICATES-VERIFICATION

  // ---- INNER loop invariant (j-scan, i fixed) --------------------------------
  // `for j in range(0, m): if numbers[j]==numbers[i]: c += 1` leaves c := countEq(J, N, I, VS, C).
  // numbers/m/i/result loop-constant; allInt(VS) so the echo reduces numbers[j]==numbers[i];
  // I,J >= 0 so normIdx collapses to valSeqAt(VS, ·).
  claim
    <k>
      #loop(rangeObj(J:Int, N:Int, 1), Name("j"),
        If(Compare(Subscript(Name("numbers"), Name("j")), CmpOp("==", Subscript(Name("numbers"), Name("i")))),
          Assign(Name("c"), BinOp("+", Name("c"), Int(1))),
          .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "numbers" <- list(VS:ValSeq) ] [ "m" <- N:Int ] [ "result" <- RESV:Val ]
                              [ "i" <- I:Int ] [ "j" <- _:Val ] [ "c" <- C:Int ], PR:Parent)
               => scope(.Map [ "numbers" <- list(VS) ] [ "m" <- N ] [ "result" <- RESV ]
                              [ "i" <- I ] [ "j" <- ?_:Val ] [ "c" <- countEq(J, N, I, VS, C) ], PR) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool I >=Int 0 andBool J >=Int 0
    [all-path]

  // ---- OUTER loop invariant (i-scan; body = c-reset + inner For + count==1 append) -----------
  // leaves result := list(dupFilter(I, N, VS, R)). Per iteration the inner For (via the inner
  // invariant) sets c := countEq(0, N, i, VS, 0); the `if c==1` append is dupFilter's guard.
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        Assign(Name("c"), Int(0))
        For(Name("j"), Call(Name("range"), (Int(0), Name("m"))),
          If(Compare(Subscript(Name("numbers"), Name("j")), CmpOp("==", Subscript(Name("numbers"), Name("i")))),
            Assign(Name("c"), BinOp("+", Name("c"), Int(1))),
            .Stmts))
        If(Compare(Name("c"), CmpOp("==", Int(1))),
          Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Subscript(Name("numbers"), Name("i"))))),
          .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "remove_duplicates" <- FB0:Val ], parent(-1))  L |-> ( scope(.Map [ "numbers" <- list(VS:ValSeq) ] [ "m" <- N:Int ] [ "result" <- ref(HN2_0:Int) ]
                              [ "i" <- _:Val ] [ "j" <- _:Val ] [ "c" <- _:Val ], parent(GLB:Int))
               => scope(.Map [ "numbers" <- list(VS) ] [ "m" <- N ] [ "result" <- ref(?HN2_0B:Int) ]
                              [ "i" <- ?_:Val ] [ "j" <- ?_:Val ] [ "c" <- ?_:Val ], parent(GLB)) ) ...
    </scopes>
    <heap> (HN2_0 |-> list(R:ValSeq)) HRST2:Map
        => (?HN2_0B |-> list(dupFilter(I, N, VS, R))) ?_:Map </heap>
    <heapLoc> HLC2:Int => ?_:Int </heapLoc>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool I >=Int 0 andBool N ==Int vsLen(VS)
     andBool 0 <=Int HN2_0 andBool HN2_0 <Int HLC2 andBool keysBelow(HRST2, HLC2)
    [all-path]

  // ---- Entry claim -----------------------------------------------------------
  // After `result = remove_duplicates(list(VS))`, result == list(dupFilter(0, len, VS, .ValSeq)):
  // the sublist of VS keeping each element that occurs exactly once, order preserved. i/j/c pre-bound
  // to 0 so the outer invariant folds without a first-iteration unroll. Domain allInt(VS).
  claim
    <k>
      FuncDef("remove_duplicates", Params("numbers"),
        Assign(Name("result"), ListExpr(.Exprs))
        Assign(Name("m"), Call(Name("len"), Name("numbers")))
        Assign(Name("i"), Int(0))
        Assign(Name("j"), Int(0))
        Assign(Name("c"), Int(0))
        For(Name("i"), Call(Name("range"), (Int(0), Name("m"))),
          Assign(Name("c"), Int(0))
          For(Name("j"), Call(Name("range"), (Int(0), Name("m"))),
            If(Compare(Subscript(Name("numbers"), Name("j")), CmpOp("==", Subscript(Name("numbers"), Name("i")))),
              Assign(Name("c"), BinOp("+", Name("c"), Int(1))),
              .Stmts))
          If(Compare(Name("c"), CmpOp("==", Int(1))),
            Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Subscript(Name("numbers"), Name("i"))))),
            .Stmts))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("remove_duplicates"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "remove_duplicates" <- ?_:Val ] [ "result" <- ref(?HN3_0:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?HN3_0 |-> list(dupFilter(0, vsLen(VS), VS, .ValSeq))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]
endmodule
