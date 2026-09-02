// spec.k — is_sorted on the UNIFIED semantics. Two SEQUENTIAL loop invariants (non-decreasing
// scan + no-3-consecutive scan) + entry. allInt(VS) lets the applyCmp echo reduce the element
// comparisons. See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module IS-SORTED-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module IS-SORTED-SPEC

requires "verification.k"

module IS-SORTED-SPEC
  imports IS-SORTED-VERIFICATION

  // ---- LOOP 1 invariant: non-decreasing scan (nondec threaded; no3 constant). ---------------
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        If(Compare(Subscript(Name("lst"), BinOp("-", Name("i"), Int(1))), CmpOp(">", Subscript(Name("lst"), Name("i")))),
          Assign(Name("nondec"), Bool(false)),
          .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "lst" <- list(VS:ValSeq) ] [ "n" <- N:Int ] [ "nondec" <- ND:Bool ] [ "no3" <- N3:Bool ] [ "i" <- _:Val ], PR:Parent)
               => scope(.Map [ "lst" <- list(VS) ] [ "n" <- N ] [ "nondec" <- nondecFold(I, N, VS, ND) ] [ "no3" <- N3 ] [ "i" <- ?_:Val ], PR) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool I >=Int 1
    [all-path]

  // ---- LOOP 2 invariant: no-3-consecutive-equal scan (no3 threaded; nondec constant). -------
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        If(Compare(Subscript(Name("lst"), BinOp("-", Name("i"), Int(2))), CmpOp("==", Subscript(Name("lst"), BinOp("-", Name("i"), Int(1))))),
          If(Compare(Subscript(Name("lst"), BinOp("-", Name("i"), Int(1))), CmpOp("==", Subscript(Name("lst"), Name("i")))),
            Assign(Name("no3"), Bool(false)),
            .Stmts),
          .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "lst" <- list(VS:ValSeq) ] [ "n" <- N:Int ] [ "nondec" <- ND:Bool ] [ "no3" <- N3:Bool ] [ "i" <- _:Val ], PR:Parent)
               => scope(.Map [ "lst" <- list(VS) ] [ "n" <- N ] [ "nondec" <- ND ] [ "no3" <- no3Fold(I, N, VS, N3) ] [ "i" <- ?_:Val ], PR) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool I >=Int 2
    [all-path]

  // ---- Entry claim -----------------------------------------------------------
  // result == isSortedRes(VS) = nondecFold(1, len, VS, true) andBool no3Fold(2, len, VS, true).
  claim
    <k>
      FuncDef("is_sorted", Params("lst"),
        Assign(Name("n"), Call(Name("len"), Name("lst")))
        Assign(Name("nondec"), Bool(true))
        Assign(Name("no3"), Bool(true))
        Assign(Name("i"), Int(0))
        For(Name("i"), Call(Name("range"), (Int(1), Name("n"))),
          If(Compare(Subscript(Name("lst"), BinOp("-", Name("i"), Int(1))), CmpOp(">", Subscript(Name("lst"), Name("i")))),
            Assign(Name("nondec"), Bool(false)),
            .Stmts))
        For(Name("i"), Call(Name("range"), (Int(2), Name("n"))),
          If(Compare(Subscript(Name("lst"), BinOp("-", Name("i"), Int(2))), CmpOp("==", Subscript(Name("lst"), BinOp("-", Name("i"), Int(1))))),
            If(Compare(Subscript(Name("lst"), BinOp("-", Name("i"), Int(1))), CmpOp("==", Subscript(Name("lst"), Name("i")))),
              Assign(Name("no3"), Bool(false)),
              .Stmts),
            .Stmts))
        Return(BoolOp("and", Name("nondec"), Name("no3"))))
      Assign(Name("result"), Call(Name("is_sorted"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "is_sorted" <- ?_:Val ] [ "result" <- isSortedRes(VS) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]
endmodule
