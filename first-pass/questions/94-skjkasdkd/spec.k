requires "verification.k"

module SKJKASDKD-SPEC
  imports SKJKASDKD-VERIFICATION

  // ---- Callee-span 1a: the REAL isPrime loop + Return + #pop (i unbound).
  claim
    <k> #loop(rangeObj(I:Int, HI2:Int, 1), Name("i"),
          If(Compare(BinOp("%", Name("n"), Name("i")), CmpOp("==", Int(0))),
            Assign(Name("p"), Bool(false)),
            .Stmts))
        ~> (Return(Name("p")) .Stmts):Stmts ~> #endcall
     => (primeI(projectIntTotal(NV), I, HI2, P) ==Int 1) ~> CONT </k>
    <env> 2 => 1 </env>
    <scopes> (2 |-> scope((.Map [ "n" <- NV:Val ] [ "$cells" <- cellsMark(.ParamNames) ]
                               [ "p" <- P:Bool ]), parent(0))) SREST:Map
          => SREST </scopes>
    <scopeLoc> _:Int => 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(CONT:K, 1, 2)) STK:List => STK </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 2 andBool okV(NV) andBool notBool 2 in_keys(SREST)
    [all-path]

  // ---- Callee-span 1b: steady state (i bound; circularity).
  claim
    <k> #loop(rangeObj(I:Int, HI2:Int, 1), Name("i"),
          If(Compare(BinOp("%", Name("n"), Name("i")), CmpOp("==", Int(0))),
            Assign(Name("p"), Bool(false)),
            .Stmts))
        ~> (Return(Name("p")) .Stmts):Stmts ~> #endcall
     => (primeI(projectIntTotal(NV), I, HI2, P) ==Int 1) ~> CONT </k>
    <env> 2 => 1 </env>
    <scopes> (2 |-> scope((.Map [ "n" <- NV:Val ] [ "$cells" <- cellsMark(.ParamNames) ]
                               [ "p" <- P:Bool ] [ "i" <- _:Val ]), parent(0))) SREST:Map
          => SREST </scopes>
    <scopeLoc> _:Int => 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(CONT:K, 1, 2)) STK:List => STK </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 2 andBool okV(NV) andBool notBool 2 in_keys(SREST)
    [all-path]

  // ---- The while invariant with the REAL call (fixed shape, frame 1 pins
  // the closure verbatim; each call allocates frame 2 and winds back).
  claim
    <k>
      #while(Compare(Name("i"), CmpOp("<", Call(Name("len"), Name("lst")))),
        If(BoolOp(
                "and",
                Compare(
                  Subscript(Name("lst"), Name("i")),
                  CmpOp(">", Name("maxx"))),
                Call(Name("isPrime"), Subscript(Name("lst"), Name("i")))),
                Assign(Name("maxx"), Subscript(Name("lst"), Name("i"))),
                .Stmts)
              AugAssign(Name("i"), "+", Int(1)))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "skjkasdkd" <- _:Val ], parent(-1))
       1 |-> (
         scope(.Map [ "lst" <- list(VS:ValSeq) ]
                    [ "isPrime" <- closureValC("n", .ParamNames,
              Assign(Name("p"), Bool(true))
                    For(Name("i"), Call(
                      Name("range"),
                      Int(2),
                      BinOp(
                        "+",
                        Call(Name("int"), BinOp("**", Name("n"), Float(0.5))),
                        Int(1))),
                      If(Compare(BinOp("%", Name("n"), Name("i")), CmpOp("==", Int(0))),
                        Assign(Name("p"), Bool(false)),
                        .Stmts))
                    Return(Name("p")), .Map) ]
                    [ "maxx" <- MV:Val ] [ "i" <- I:Int ], parent(0)) =>
         scope(.Map [ "lst" <- list(VS) ] [ "isPrime" <- ?_:Val ]
                    [ "maxx" <- maxSel(VS, I, MV) ] [ "i" <- ?_:Val ], parent(0))
       )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool 0 <=Int I andBool okV(MV)
     andBool 0 <=Int projectIntTotal(MV)
    [all-path]

  // ---- Digit-sum loop, variant A (digit unbound; str(maxx) is nonempty).
  claim
    <k>
      #loop(str(CS:IntSeq), Name("digit"),
        Assign(
          Name("result"),
          BinOp("+", Name("result"), Call(Name("int"), Name("digit")))))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "skjkasdkd" <- _:Val ], parent(-1))
       1 |-> (
         scope(.Map [ "lst" <- LV:Val ] [ "isPrime" <- IPV:Val ] [ "maxx" <- MXV:Val ]
                    [ "i" <- IV:Val ] [ "result" <- R:Int ], parent(0)) =>
         scope(.Map [ "lst" <- LV ] [ "isPrime" <- IPV ] [ "maxx" <- MXV ]
                    [ "i" <- IV ] [ "result" <- sumDig(CS, R) ] [ "digit" <- ?_:Val ], parent(0))
       )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allDigit(CS) andBool 0 <Int isLen(CS)
    [all-path]

  // ---- Digit-sum loop, variant B (digit bound; circularity).
  claim
    <k>
      #loop(str(CS:IntSeq), Name("digit"),
        Assign(
          Name("result"),
          BinOp("+", Name("result"), Call(Name("int"), Name("digit")))))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "skjkasdkd" <- _:Val ], parent(-1))
       1 |-> (
         scope(.Map [ "lst" <- LV:Val ] [ "isPrime" <- IPV:Val ] [ "maxx" <- MXV:Val ]
                    [ "i" <- IV:Val ] [ "result" <- R:Int ] [ "digit" <- _:Val ], parent(0)) =>
         scope(.Map [ "lst" <- LV ] [ "isPrime" <- IPV ] [ "maxx" <- MXV ]
                    [ "i" <- IV ] [ "result" <- sumDig(CS, R) ] [ "digit" <- ?_:Val ], parent(0))
       )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allDigit(CS)
    [all-path]

  // ---- Entry — the REAL canonical-shape code, verbatim .mpy.
  claim
    <k>
      FuncDef("skjkasdkd", Params("lst"),
          FuncDef("isPrime", Params("n"), CellVars(.ParamNames), FreeVars(.ParamNames),
            Assign(Name("p"), Bool(true))
            For(Name("i"), Call(
              Name("range"),
              Int(2),
              BinOp(
                "+",
                Call(Name("int"), BinOp("**", Name("n"), Float(0.5))),
                Int(1))),
              If(Compare(BinOp("%", Name("n"), Name("i")), CmpOp("==", Int(0))),
                Assign(Name("p"), Bool(false)),
                .Stmts))
            Return(Name("p")))
          Assign(Name("maxx"), Int(0))
          Assign(Name("i"), Int(0))
          While(Compare(Name("i"), CmpOp("<", Call(Name("len"), Name("lst")))),
            If(BoolOp(
              "and",
              Compare(
                Subscript(Name("lst"), Name("i")),
                CmpOp(">", Name("maxx"))),
              Call(Name("isPrime"), Subscript(Name("lst"), Name("i")))),
              Assign(Name("maxx"), Subscript(Name("lst"), Name("i"))),
              .Stmts)
            AugAssign(Name("i"), "+", Int(1)))
          Assign(Name("result"), Int(0))
          For(Name("digit"), Call(Name("str"), Name("maxx")),
            Assign(
              Name("result"),
              BinOp("+", Name("result"), Call(Name("int"), Name("digit")))))
          Return(Name("result")))
      Assign(Name("result"), Call(Name("skjkasdkd"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "skjkasdkd" <- ?_:Val ]
                       [ "result" <- sumDig(strToCodes(Int2String(projectIntTotal(maxSel(VS, 0, 0)))), 0) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => .Map </heap>
    <heapLoc> 0 => 0 </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]
endmodule
