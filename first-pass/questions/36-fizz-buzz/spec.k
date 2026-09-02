// spec.k — fizz_buzz, TRAP-FREE (P36). Filter-append invariant (Probe-B fixed
// ref), the opaque join/map composition in straight line, and the char-count
// invariant over the abstract joined codes; entry composes all three.
//
//   kompile verification.k --backend haskell --main-module FIZZ-BUZZ-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module FIZZ-BUZZ-SPEC

requires "verification.k"

module FIZZ-BUZZ-SPEC
  imports FIZZ-BUZZ-VERIFICATION

  claim
    <k>
      #loop(rangeObj(I:Int, HI:Int, 1), Name("i"),
        If(BoolOp("or",
            Compare(BinOp("%", Name("i"), Int(11)), CmpOp("==", Int(0))),
            Compare(BinOp("%", Name("i"), Int(13)), CmpOp("==", Int(0)))),
          Expr(Call(Attribute(Name("ns"), "append"), Name("i"))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "fizz_buzz" <- FBV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "n" <- NV:Val ] [ "ns" <- ref(LR:Int) ], parent(0))
           => scope(.Map [ "n" <- NV ] [ "ns" <- ref(LR) ] [ "i" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (LR |-> list(ACC:ValSeq)) HREST:Map
        => (LR |-> list(divList(I, HI, ACC))) HREST </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I <Int HI
    [all-path]

  claim
    <k>
      #loop(rangeObj(I:Int, HI:Int, 1), Name("i"),
        If(BoolOp("or",
            Compare(BinOp("%", Name("i"), Int(11)), CmpOp("==", Int(0))),
            Compare(BinOp("%", Name("i"), Int(13)), CmpOp("==", Int(0)))),
          Expr(Call(Attribute(Name("ns"), "append"), Name("i"))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "fizz_buzz" <- FBV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "n" <- NV:Val ] [ "ns" <- ref(LR:Int) ] [ "i" <- _:Val ], parent(0))
           => scope(.Map [ "n" <- NV ] [ "ns" <- ref(LR) ] [ "i" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (LR |-> list(ACC:ValSeq)) HREST:Map
        => (LR |-> list(divList(I, HI, ACC))) HREST </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  claim
    <k>
      #loop(str(IS:IntSeq), Name("c"),
        AugAssign(Name("ans"), "+", Compare(Name("c"), CmpOp("==", Str("7")))))
    => .K ... </k>
    <env> L0:Int </env>
    <scopes>
      ... L0 |-> ( scope(.Map [ "n" <- NV:Val ] [ "ns" <- NSV:Val ] [ "s" <- SV:Val ]
                              [ "ans" <- ACC:Int ] [ "i" <- IV:Val ], PR:Parent)
               => scope((.Map [ "n" <- NV ] [ "ns" <- NSV ] [ "s" <- SV ]
                              [ "ans" <- count7(IS, ACC) ] [ "i" <- IV ]) ?_:Map, PR) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  claim
    <k>
      #loop(str(IS:IntSeq), Name("c"),
        AugAssign(Name("ans"), "+", Compare(Name("c"), CmpOp("==", Str("7")))))
    => .K ... </k>
    <env> L0:Int </env>
    <scopes>
      ... L0 |-> ( scope(.Map [ "n" <- NV:Val ] [ "ns" <- NSV:Val ] [ "s" <- SV:Val ]
                              [ "ans" <- ACC:Int ] [ "i" <- IV:Val ] [ "c" <- _:Val ], PR:Parent)
               => scope((.Map [ "n" <- NV ] [ "ns" <- NSV ] [ "s" <- SV ]
                              [ "ans" <- count7(IS, ACC) ] [ "i" <- IV ]) [ "c" <- ?_:Val ], PR) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  claim
    <k>
      FuncDef("fizz_buzz", Params("n"),
        Assign(Name("ns"), ListExpr(.Exprs))
        For(Name("i"), Call(Name("range"), Name("n")),
          If(BoolOp("or",
            Compare(BinOp("%", Name("i"), Int(11)), CmpOp("==", Int(0))),
            Compare(BinOp("%", Name("i"), Int(13)), CmpOp("==", Int(0)))),
          Expr(Call(Attribute(Name("ns"), "append"), Name("i"))),
          .Stmts))
        Assign(Name("s"),
          Call(Attribute(Str(""), "join"),
            Call(Name("list"), Call(Name("map"), Name("str"), Name("ns")))))
        Assign(Name("ans"), Int(0))
        For(Name("c"), Name("s"),
          AugAssign(Name("ans"), "+", Compare(Name("c"), CmpOp("==", Str("7")))))
        Return(Name("ans")))
      Assign(Name("result"), Call(Name("fizz_buzz"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "fizz_buzz" <- ?_:Val ] [ "result" <- fbRes(N) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 1
    [all-path]
endmodule
