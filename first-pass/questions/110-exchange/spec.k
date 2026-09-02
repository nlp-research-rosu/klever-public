requires "verification.k"

module EXCHANGE-SPEC
  imports EXCHANGE-VERIFICATION

  // ---- Loop invariant 1: the odd-count loop over lst1. odd := OD +Int countOdd(VS).
  claim
    <k>
      #loop(list(VS:ValSeq), Name("i"),
        If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(1))),
           AugAssign(Name("odd"), "+", Int(1)),
           .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "lst1" <- L1V:Val ] [ "lst2" <- L2V:Val ]
                   [ "odd" <- OD:Int ] [ "even" <- EV:Int ] [ "i" <- _:Val ], P:Parent) =>
        scope(.Map [ "lst1" <- L1V ] [ "lst2" <- L2V ]
                   [ "odd" <- ?OD2:Int ] [ "even" <- EV ] [ "i" <- ?_:Val ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    ensures ?OD2 ==Int OD +Int countOdd(intListOf(VS))
    [all-path]

  // ---- Loop invariant 2: the even-count loop over lst2. even := EV +Int countEven(VS).
  claim
    <k>
      #loop(list(VS:ValSeq), Name("i"),
        If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
           AugAssign(Name("even"), "+", Int(1)),
           .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "lst1" <- L1V:Val ] [ "lst2" <- L2V:Val ]
                   [ "odd" <- OD:Int ] [ "even" <- EV:Int ] [ "i" <- _:Val ], P:Parent) =>
        scope(.Map [ "lst1" <- L1V ] [ "lst2" <- L2V ]
                   [ "odd" <- OD ] [ "even" <- ?EV2:Int ] [ "i" <- ?_:Val ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    ensures ?EV2 ==Int EV +Int countEven(intListOf(VS))
    [all-path]

  // ---- Entry claim — result = exchange(list(VS1), list(VS2)) = "YES" iff
  // countEven(VS2) >= countOdd(VS1), else "NO".
  claim
    <k>
      FuncDef("exchange", Params("lst1", "lst2"),
        Assign(Name("odd"), Int(0))
        Assign(Name("even"), Int(0))
        For(Name("i"), Name("lst1"),
          If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(1))),
             AugAssign(Name("odd"), "+", Int(1)),
             .Stmts))
        For(Name("i"), Name("lst2"),
          If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
             AugAssign(Name("even"), "+", Int(1)),
             .Stmts))
        If(Compare(Name("even"), CmpOp(">=", Name("odd"))),
           Return(Str("YES")),
           .Stmts)
        Return(Str("NO")))
      Assign(Name("result"), Call(Name("exchange"), list(VS1:ValSeq) , list(VS2:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "exchange" <- ?_:Val ] [ "result" <- ?R:Val ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS1) andBool allInt(VS2)
    ensures ?R ==K #if (countEven(intListOf(VS2)) >=Int countOdd(intListOf(VS1)))
             #then str(strToCodes("YES"))
             #else str(strToCodes("NO")) #fi
    [all-path]
endmodule
