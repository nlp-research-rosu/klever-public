// spec.k — is_bored on the UNIFIED semantics, TRAP-FREE (P91). Canonical 1-fn
// shape: the single-pass scan lives in is_bored's own frame; while-invariant
// claim + entry over the ONE FuncDef.
//
//   kompile verification.k --backend haskell \
//     --main-module IS-BORED-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module IS-BORED-SPEC

requires "verification.k"

module IS-BORED-SPEC
  imports IS-BORED-VERIFICATION

  // ---- WHILE invariant — the scan leaves (count, phase, cand) := projections of
  // boredFold(CS, I, N, bstate(CT, PH, CD)). Each iteration's elif dispatch case-splits on the
  // intSeqAt(CS, I) class atoms and folds via exactly one boredFold rule.
  claim
    <k>
      #while(Compare(Name("i"), CmpOp("<", Name("n"))),
        If(BoolOp(
          "and",
          Compare(Name("phase"), CmpOp("==", Int(3))),
          BoolOp(
            "or",
            Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(46))),
            Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(63))),
            Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(33))),
            BoolOp(
              "and",
              Compare(Int(9), CmpOp("<=", Call(Name("ord"), Subscript(Name("S"), Name("i"))))),
              Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("<=", Int(13)))),
            BoolOp(
              "and",
              Compare(Int(28), CmpOp("<=", Call(Name("ord"), Subscript(Name("S"), Name("i"))))),
              Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("<=", Int(32)))))),
          Assign(Name("phase"), Int(3)),
          If(BoolOp(
            "or",
            Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(46))),
            Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(63))),
            Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(33)))),
            If(Compare(Name("cand"), CmpOp("==", Int(2))),
              Assign(Name("count"), BinOp("+", Name("count"), Int(1))),
              .Stmts)
            Assign(Name("cand"), Int(0))
            Assign(Name("phase"), Int(3)),
            If(BoolOp(
              "or",
              Compare(Name("phase"), CmpOp("==", Int(3))),
              Compare(Name("phase"), CmpOp("==", Int(0)))),
              Assign(
                Name("cand"),
                IfExp(
                  Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(73))),
                  Int(1),
                  Int(0)))
              Assign(Name("phase"), Int(1)),
              If(Compare(Name("phase"), CmpOp("==", Int(1))),
                Assign(
                  Name("cand"),
                  IfExp(
                    BoolOp(
                      "and",
                      Compare(Name("cand"), CmpOp("==", Int(1))),
                      Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(32)))),
                    Int(2),
                    Int(0)))
                Assign(Name("phase"), Int(2)),
                .Stmts))))
        Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      ... -1 |-> builtinsScope
      0 |-> scope(.Map [ "is_bored" <- _FB0:Val ], parent(-1))
      1 |-> ( scope(.Map [ "S" <- str(CS:IntSeq) ] [ "count" <- CT:Int ] [ "phase" <- PH:Int ]
                              [ "cand" <- CD:Int ] [ "i" <- I:Int ] [ "n" <- N:Int ], parent(0))
               => scope(.Map [ "S" <- str(CS) ]
                              [ "count" <- bCt(boredFold(CS, I, N, bstate(CT, PH, CD))) ]
                              [ "phase" <- bPh(boredFold(CS, I, N, bstate(CT, PH, CD))) ]
                              [ "cand" <- bCd(boredFold(CS, I, N, bstate(CT, PH, CD))) ]
                              [ "i" <- ?_:Val ] [ "n" <- N ], parent(0)) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0 andBool N ==Int isLen(CS)
    [all-path]

  // ---- Entry claim — result = is_bored(str(CS)) == boredRes(CS), with BOTH FuncDefs executing
  // for real: the while folds via the invariant claim inside is_bored's own frame.
  // invariant above; the post-loop `if cand == 2` splits on the bCd atom and boredRes matches
  // both branches.
  claim
    <k>
      FuncDef("is_bored", Params("S"),
        Assign(Name("count"), Int(0))
        Assign(Name("phase"), Int(0))
        Assign(Name("cand"), Int(0))
        Assign(Name("i"), Int(0))
        Assign(Name("n"), Call(Name("len"), Name("S")))
        While(Compare(Name("i"), CmpOp("<", Name("n"))),
          If(BoolOp(
            "and",
            Compare(Name("phase"), CmpOp("==", Int(3))),
            BoolOp(
              "or",
              Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(46))),
              Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(63))),
              Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(33))),
              BoolOp(
                "and",
                Compare(Int(9), CmpOp("<=", Call(Name("ord"), Subscript(Name("S"), Name("i"))))),
                Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("<=", Int(13)))),
              BoolOp(
                "and",
                Compare(Int(28), CmpOp("<=", Call(Name("ord"), Subscript(Name("S"), Name("i"))))),
                Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("<=", Int(32)))))),
            Assign(Name("phase"), Int(3)),
            If(BoolOp(
              "or",
              Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(46))),
              Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(63))),
              Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(33)))),
              If(Compare(Name("cand"), CmpOp("==", Int(2))),
                Assign(Name("count"), BinOp("+", Name("count"), Int(1))),
                .Stmts)
              Assign(Name("cand"), Int(0))
              Assign(Name("phase"), Int(3)),
              If(BoolOp(
                "or",
                Compare(Name("phase"), CmpOp("==", Int(3))),
                Compare(Name("phase"), CmpOp("==", Int(0)))),
                Assign(
                  Name("cand"),
                  IfExp(
                    Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(73))),
                    Int(1),
                    Int(0)))
                Assign(Name("phase"), Int(1)),
                If(Compare(Name("phase"), CmpOp("==", Int(1))),
                  Assign(
                    Name("cand"),
                    IfExp(
                      BoolOp(
                        "and",
                        Compare(Name("cand"), CmpOp("==", Int(1))),
                        Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(32)))),
                      Int(2),
                      Int(0)))
                  Assign(Name("phase"), Int(2)),
                  .Stmts))))
          Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
        If(Compare(Name("cand"), CmpOp("==", Int(2))),
          Assign(Name("count"), BinOp("+", Name("count"), Int(1))),
          .Stmts)
        Return(Name("count")))
      Assign(Name("result"), Call(Name("is_bored"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "is_bored" <- ?_:Val ] [ "result" <- bCt(boredState(CS)) +Int 1 ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires bCd(boredState(CS)) ==Int 2
    [all-path]

  claim
    <k>
      FuncDef("is_bored", Params("S"),
        Assign(Name("count"), Int(0))
        Assign(Name("phase"), Int(0))
        Assign(Name("cand"), Int(0))
        Assign(Name("i"), Int(0))
        Assign(Name("n"), Call(Name("len"), Name("S")))
        While(Compare(Name("i"), CmpOp("<", Name("n"))),
          If(BoolOp(
            "and",
            Compare(Name("phase"), CmpOp("==", Int(3))),
            BoolOp(
              "or",
              Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(46))),
              Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(63))),
              Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(33))),
              BoolOp(
                "and",
                Compare(Int(9), CmpOp("<=", Call(Name("ord"), Subscript(Name("S"), Name("i"))))),
                Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("<=", Int(13)))),
              BoolOp(
                "and",
                Compare(Int(28), CmpOp("<=", Call(Name("ord"), Subscript(Name("S"), Name("i"))))),
                Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("<=", Int(32)))))),
            Assign(Name("phase"), Int(3)),
            If(BoolOp(
              "or",
              Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(46))),
              Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(63))),
              Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(33)))),
              If(Compare(Name("cand"), CmpOp("==", Int(2))),
                Assign(Name("count"), BinOp("+", Name("count"), Int(1))),
                .Stmts)
              Assign(Name("cand"), Int(0))
              Assign(Name("phase"), Int(3)),
              If(BoolOp(
                "or",
                Compare(Name("phase"), CmpOp("==", Int(3))),
                Compare(Name("phase"), CmpOp("==", Int(0)))),
                Assign(
                  Name("cand"),
                  IfExp(
                    Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(73))),
                    Int(1),
                    Int(0)))
                Assign(Name("phase"), Int(1)),
                If(Compare(Name("phase"), CmpOp("==", Int(1))),
                  Assign(
                    Name("cand"),
                    IfExp(
                      BoolOp(
                        "and",
                        Compare(Name("cand"), CmpOp("==", Int(1))),
                        Compare(Call(Name("ord"), Subscript(Name("S"), Name("i"))), CmpOp("==", Int(32)))),
                      Int(2),
                      Int(0)))
                  Assign(Name("phase"), Int(2)),
                  .Stmts))))
          Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
        If(Compare(Name("cand"), CmpOp("==", Int(2))),
          Assign(Name("count"), BinOp("+", Name("count"), Int(1))),
          .Stmts)
        Return(Name("count")))
      Assign(Name("result"), Call(Name("is_bored"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "is_bored" <- ?_:Val ] [ "result" <- bCt(boredState(CS)) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool (bCd(boredState(CS)) ==Int 2)
    [all-path]
endmodule
