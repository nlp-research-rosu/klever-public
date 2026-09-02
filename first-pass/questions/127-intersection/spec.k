// spec.k — intersection reachability claims on the UNIFIED semantics (src/). is_prime (reused
// from #31) of the interval-overlap length, formatted "YES"/"NO". See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module INTERSECTION-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module INTERSECTION-SPEC

requires "verification.k"

module INTERSECTION-SPEC
  imports INTERSECTION-VERIFICATION

  // ---- Loop invariant (circularity) — over rangeObj(I, HI, 1) from prime = P the divisor
  // scan on `length` leaves prime := primeAcc(LEN, I, HI, P). `i` pre-bound for a stable scope.
  claim
    <k>
      #loop(rangeObj(I:Int, HI:Int, 1), Name("i"),
        If(Compare(BinOp("%", Name("length"), Name("i")), CmpOp("==", Int(0))),
           Assign(Name("prime"), Bool(false)),
           .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "interval1" <- IV1:Val ] [ "interval2" <- IV2:Val ]
                            [ "l" <- LV:Int ] [ "r" <- RV:Int ]
                            [ "length" <- LEN:Int ] [ "prime" <- P:Bool ] [ "i" <- _:Val ], PR:Parent)
               => scope(.Map [ "interval1" <- IV1 ] [ "interval2" <- IV2 ]
                            [ "l" <- LV ] [ "r" <- RV ]
                            [ "length" <- LEN ] [ "prime" <- primeAcc(LEN, I, HI, P) ] [ "i" <- ?_:Val ], PR) ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — after `result = intersection((S1,E1), (S2,E2))`, result ==
  // ires(minInt(E1,E2) -Int maxInt(S1,S2)): "YES" iff the overlap length is > 0 and prime.
  // max(a,b) => maxInt(a,b), min(a,b) => minInt(a,b) via the unified builtins.
  claim
    <k>
      FuncDef("intersection", Params("interval1", "interval2"),
        Assign(Name("l"), Call(Name("max"), (Subscript(Name("interval1"), Int(0)), Subscript(Name("interval2"), Int(0)))))
        Assign(Name("r"), Call(Name("min"), (Subscript(Name("interval1"), Int(1)), Subscript(Name("interval2"), Int(1)))))
        Assign(Name("length"), BinOp("-", Name("r"), Name("l")))
        Assign(Name("prime"), Compare(Name("length"), CmpOp(">=", Int(2))))
        Assign(Name("i"), Int(0))
        For(Name("i"), Call(Name("range"), (Int(2), Name("length"))),
          If(Compare(BinOp("%", Name("length"), Name("i")), CmpOp("==", Int(0))),
             Assign(Name("prime"), Bool(false)),
             .Stmts))
        If(Compare(Name("length"), CmpOp(">", Int(0))),
          If(Name("prime"),
            Assign(Name("result"), Str("YES")),
            Assign(Name("result"), Str("NO"))),
          Assign(Name("result"), Str("NO")))
        Return(Name("result")))
      Assign(Name("result"),
        Call(Name("intersection"),
          (tuple(vCons(S1:Int, vCons(E1:Int, .ValSeq))),
           tuple(vCons(S2:Int, vCons(E2:Int, .ValSeq))))))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "intersection" <- ?_:Val ]
                       [ "result" <- ires(minInt(E1, E2) -Int maxInt(S1, S2)) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
