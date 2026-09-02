// spec.k — iscube reachability claims on the UNIFIED semantics (src/). A bounded scan (the
// is_prime idiom) over range(0, abs(a)+1) with a sticky Bool `found`. See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module ISCUBE-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module ISCUBE-SPEC

requires "verification.k"

module ISCUBE-SPEC
  imports ISCUBE-VERIFICATION

  // ---- Loop invariant (circularity) — over rangeObj(I, HI, 1) from found = F the scan
  // leaves found := cubeAcc(I, HI, AV, F). `r` pre-bound for a stable scope.
  claim
    <k>
      #loop(rangeObj(I:Int, HI:Int, 1), Name("r"),
        If(Compare(BinOp("*", BinOp("*", Name("r"), Name("r")), Name("r")), CmpOp("==", Name("a"))),
           Assign(Name("found"), Bool(true)),
           .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "a" <- AV:Int ] [ "found" <- F:Bool ] [ "r" <- _:Val ], PR:Parent)
               => scope(.Map [ "a" <- AV ] [ "found" <- cubeAcc(I, HI, AV, F) ] [ "r" <- ?_:Val ], PR) ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — after `result = iscube(A)`, result == cubeAcc(0, absInt(A)+1,
  // absInt(A), false): some non-negative r <= |A| has r^3 == |A|. abs(A) => absInt(A).
  claim
    <k>
      FuncDef("iscube", Params("a"),
        Assign(Name("a"), Call(Name("abs"), Name("a")))
        Assign(Name("found"), Bool(false))
        Assign(Name("r"), Int(0))
        For(Name("r"), Call(Name("range"), (Int(0), BinOp("+", Name("a"), Int(1)))),
          If(Compare(BinOp("*", BinOp("*", Name("r"), Name("r")), Name("r")), CmpOp("==", Name("a"))),
             Assign(Name("found"), Bool(true)),
             .Stmts))
        Return(Name("found")))
      Assign(Name("result"), Call(Name("iscube"), Int(A:Int)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "iscube" <- ?_:Val ] [ "result" <- cubeAcc(0, absInt(A) +Int 1, absInt(A), false) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
