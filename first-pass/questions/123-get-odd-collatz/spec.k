// spec.k — get_odd_collatz on the UNIFIED semantics (src/). Collatz while invariant + entry. See
// ./PROOF.md.
//
//   kompile verification.k --backend haskell --main-module GET-ODD-COLLATZ-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module GET-ODD-COLLATZ-SPEC

requires "verification.k"

module GET-ODD-COLLATZ-SPEC
  imports GET-ODD-COLLATZ-VERIFICATION

  // ---- Loop invariant — Collatz odd-collection. From (odd_collatz=list(ACC), n=NV) the loop leaves
  // odd_collatz := list(collatzFold(NV, ACC)); n havoc'd. The body's first If splits on `n%2==0`
  // (n//2 vs n*3+1), the second on the NEW n's parity (collect) — matching collatzFold's rules (the odd
  // branch's collect is infeasible: n*3+1 is even). Scope: {n, odd_collatz}.
  claim
    <k>
      #while(Compare(Name("n"), CmpOp(">", Int(1))),
        If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(0))),
          Assign(Name("n"), BinOp("//", Name("n"), Int(2))),
          Assign(Name("n"), BinOp("+", BinOp("*", Name("n"), Int(3)), Int(1))))
        If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(1))),
          Assign(Name("odd_collatz"), BinOp("+", Name("odd_collatz"), ListExpr(Name("n")))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "get_odd_collatz" <- _:Val ], parent(-1))
       1 |-> (
        scope(.Map [ "n" <- NV:Int ] [ "odd_collatz" <- ref(HN1_0:Int) ], parent(0)) =>
        scope(.Map [ "n" <- ?_:Val ] [ "odd_collatz" <- ref(?HN1_0B:Int) ], parent(0))
      )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <heap> (HN1_0 |-> list(ACC:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(collatzFold(NV, ACC))) ?FRESH1:Map HRST1 </heap>
    <heapLoc> HLC1:Int => ?HLC2:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires NV >=Int 1
     andBool 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
    ensures 0 <=Int ?HN1_0B andBool ?HN1_0B <Int ?HLC2 andBool HLC1 <=Int ?HLC2
     andBool keysBelow(?FRESH1, ?HLC2)
     andBool notBool (?HN1_0B in_keys(?FRESH1))
     andBool notBool (?HN1_0B in_keys(HRST1))
    [all-path]

  // ---- Entry — result = get_odd_collatz(N) == getOddCollatzRes(N) = sorted list of odd Collatz numbers.
  // The initial `if n%2==1` splits the seed (odd_collatz = [N] vs []), matching getOddCollatzRes's two
  // rules. Domain N >= 1 (positive integer).
  claim
    <k>
      FuncDef("get_odd_collatz", Params("n"),
        Assign(Name("odd_collatz"), ListExpr(.Exprs))
        If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(1))),
          Assign(Name("odd_collatz"), ListExpr(Name("n"))),
          .Stmts)
        While(Compare(Name("n"), CmpOp(">", Int(1))),
          If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(0))),
            Assign(Name("n"), BinOp("//", Name("n"), Int(2))),
            Assign(Name("n"), BinOp("+", BinOp("*", Name("n"), Int(3)), Int(1))))
          If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(1))),
            Assign(Name("odd_collatz"), BinOp("+", Name("odd_collatz"), ListExpr(Name("n")))),
            .Stmts))
        Return(Call(Name("sorted"), Name("odd_collatz"))))
      Assign(Name("result"), Call(Name("get_odd_collatz"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "get_odd_collatz" <- ?_:Val ] [ "result" <- ref(?RH:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?RH |-> list(sortVS(collatzFold(N, vCons(N, .ValSeq))))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 1 andBool pyMod(N, 2) ==Int 1
    [all-path]
  // ---- Entry (even seed) — result = get_odd_collatz(N) == getOddCollatzRes(N) = sorted list of odd Collatz numbers.
  // The initial `if n%2==1` splits the seed (odd_collatz = [N] vs []), matching getOddCollatzRes's two
  // rules. Domain N >= 1 (positive integer).
  claim
    <k>
      FuncDef("get_odd_collatz", Params("n"),
        Assign(Name("odd_collatz"), ListExpr(.Exprs))
        If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(1))),
          Assign(Name("odd_collatz"), ListExpr(Name("n"))),
          .Stmts)
        While(Compare(Name("n"), CmpOp(">", Int(1))),
          If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(0))),
            Assign(Name("n"), BinOp("//", Name("n"), Int(2))),
            Assign(Name("n"), BinOp("+", BinOp("*", Name("n"), Int(3)), Int(1))))
          If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(1))),
            Assign(Name("odd_collatz"), BinOp("+", Name("odd_collatz"), ListExpr(Name("n")))),
            .Stmts))
        Return(Call(Name("sorted"), Name("odd_collatz"))))
      Assign(Name("result"), Call(Name("get_odd_collatz"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "get_odd_collatz" <- ?_:Val ] [ "result" <- ref(?RH:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?RH |-> list(sortVS(collatzFold(N, .ValSeq)))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 1 andBool pyMod(N, 2) ==Int 0
    [all-path]
endmodule
