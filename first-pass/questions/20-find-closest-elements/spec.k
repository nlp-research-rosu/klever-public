// spec.k — find_closest_elements on the UNIFIED semantics. Nested min-scan: inner invariant
// (j-scan, skip j==i) + outer invariant (i-scan whose body contains the inner For) + entry.
// allInt(NUMS) lets the echoes reduce numbers[i]-numbers[j] and min/max(numbers[i],numbers[j]).
// See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module CLOSEST-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module CLOSEST-SPEC

requires "verification.k"

module CLOSEST-SPEC
  imports CLOSEST-VERIFICATION

  // ---- INNER loop invariant: j in [J, N), fixed outer index I; threads (dist, lo, hi). --------
  claim
    <k>
      #loop(rangeObj(J:Int, N:Int, 1), Name("j"),
        If(Compare(Name("i"), CmpOp("!=", Name("j"))),
          Assign(Name("d"),
            Call(Name("abs"), BinOp("-", Subscript(Name("numbers"), Name("i")), Subscript(Name("numbers"), Name("j")))))
          If(Compare(Name("d"), CmpOp("<", Name("dist"))),
            Assign(Name("dist"), Name("d"))
            Assign(Name("lo"), Call(Name("min"), Subscript(Name("numbers"), Name("i")), Subscript(Name("numbers"), Name("j"))))
            Assign(Name("hi"), Call(Name("max"), Subscript(Name("numbers"), Name("i")), Subscript(Name("numbers"), Name("j")))),
            .Stmts),
          .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "find_closest_elements" <- FB0:Val ], parent(-1))  L |-> ( scope(.Map [ "numbers" <- list(NUMS:ValSeq) ] [ "n" <- N:Int ] [ "i" <- I:Int ]
                          [ "dist" <- D:Int ] [ "lo" <- LO:Int ] [ "hi" <- HI:Int ]
                          [ "j" <- _:Val ] [ "d" <- _:Val ], parent(GLB:Int))
               => scope(.Map [ "numbers" <- list(NUMS) ] [ "n" <- N ] [ "i" <- I ]
                          [ "dist" <- accD(innerFold(J, N, I, NUMS, acc(D, LO, HI))) ]
                          [ "lo" <- accLo(innerFold(J, N, I, NUMS, acc(D, LO, HI))) ]
                          [ "hi" <- accHi(innerFold(J, N, I, NUMS, acc(D, LO, HI))) ]
                          [ "j" <- ?_:Val ] [ "d" <- ?_:Val ], parent(GLB)) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(NUMS) andBool I >=Int 0 andBool J >=Int 0
    [all-path]

  // ---- OUTER loop invariant: i in [I, N); each step runs the full inner loop. -----------------
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        For(Name("j"), Call(Name("range"), (Int(0), Name("n"))),
          If(Compare(Name("i"), CmpOp("!=", Name("j"))),
            Assign(Name("d"),
              Call(Name("abs"), BinOp("-", Subscript(Name("numbers"), Name("i")), Subscript(Name("numbers"), Name("j")))))
            If(Compare(Name("d"), CmpOp("<", Name("dist"))),
              Assign(Name("dist"), Name("d"))
              Assign(Name("lo"), Call(Name("min"), Subscript(Name("numbers"), Name("i")), Subscript(Name("numbers"), Name("j"))))
              Assign(Name("hi"), Call(Name("max"), Subscript(Name("numbers"), Name("i")), Subscript(Name("numbers"), Name("j")))),
              .Stmts),
            .Stmts)))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "find_closest_elements" <- FB0:Val ], parent(-1))  L |-> ( scope(.Map [ "numbers" <- list(NUMS:ValSeq) ] [ "n" <- N:Int ] [ "i" <- _:Val ]
                          [ "dist" <- D:Int ] [ "lo" <- LO:Int ] [ "hi" <- HI:Int ]
                          [ "j" <- _:Val ] [ "d" <- _:Val ], parent(GLB:Int))
               => scope(.Map [ "numbers" <- list(NUMS) ] [ "n" <- N ] [ "i" <- ?_:Val ]
                          [ "dist" <- accD(outerFold(I, N, NUMS, acc(D, LO, HI))) ]
                          [ "lo" <- accLo(outerFold(I, N, NUMS, acc(D, LO, HI))) ]
                          [ "hi" <- accHi(outerFold(I, N, NUMS, acc(D, LO, HI))) ]
                          [ "j" <- ?_:Val ] [ "d" <- ?_:Val ], parent(GLB)) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(NUMS) andBool I >=Int 0
    [all-path]

  // ---- Entry claim -----------------------------------------------------------
  claim
    <k>
      FuncDef("find_closest_elements", Params("numbers"),
        Assign(Name("n"), Call(Name("len"), Name("numbers")))
        Assign(Name("dist"), Call(Name("abs"), BinOp("-", Subscript(Name("numbers"), Int(0)), Subscript(Name("numbers"), Int(1)))))
        Assign(Name("lo"), Call(Name("min"), Subscript(Name("numbers"), Int(0)), Subscript(Name("numbers"), Int(1))))
        Assign(Name("hi"), Call(Name("max"), Subscript(Name("numbers"), Int(0)), Subscript(Name("numbers"), Int(1))))
        Assign(Name("i"), Int(0))
        Assign(Name("j"), Int(0))
        Assign(Name("d"), Int(0))
        For(Name("i"), Call(Name("range"), (Int(0), Name("n"))),
          For(Name("j"), Call(Name("range"), (Int(0), Name("n"))),
            If(Compare(Name("i"), CmpOp("!=", Name("j"))),
              Assign(Name("d"),
                Call(Name("abs"), BinOp("-", Subscript(Name("numbers"), Name("i")), Subscript(Name("numbers"), Name("j")))))
              If(Compare(Name("d"), CmpOp("<", Name("dist"))),
                Assign(Name("dist"), Name("d"))
                Assign(Name("lo"), Call(Name("min"), Subscript(Name("numbers"), Name("i")), Subscript(Name("numbers"), Name("j"))))
                Assign(Name("hi"), Call(Name("max"), Subscript(Name("numbers"), Name("i")), Subscript(Name("numbers"), Name("j")))),
                .Stmts),
              .Stmts)))
        Return(TupleExpr(Name("lo"), Name("hi"))))
      Assign(Name("result"), Call(Name("find_closest_elements"), list(NUMS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "find_closest_elements" <- ?_:Val ] [ "result" <- closestRes(NUMS, vsLen(NUMS)) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(NUMS) andBool vsLen(NUMS) >=Int 2
    [all-path]
endmodule
