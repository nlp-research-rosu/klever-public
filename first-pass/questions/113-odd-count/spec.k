requires "verification.k"

module ODD-COUNT-SPEC
  imports ODD-COUNT-VERIFICATION

  // ---- Inner digit-count invariant, variant B (d bound; circularity).
  claim
    <k>
      #loop(str(CS:IntSeq), Name("d"),
        If(Compare(
          BinOp("%", Call(Name("int"), Name("d")), Int(2)),
          CmpOp("==", Int(1))),
          Assign(Name("n"), BinOp("+", Name("n"), Int(1))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "odd_count" <- _:Val ], parent(-1))
       1 |-> (
         scope(.Map [ "lst" <- LV:Val ] [ "res" <- ref(AR:Int) ] [ "arr" <- AV:Val ]
                    [ "n" <- N:Int ] [ "d" <- _:Val ], parent(0)) =>
         scope(.Map [ "lst" <- LV ] [ "res" <- ref(AR) ] [ "arr" <- AV ]
                    [ "n" <- oddCnt2(CS, N) ] [ "d" <- ?_:Val ], parent(0))
       )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allDigit(CS)
    [all-path]

  // ---- Inner variant A (d unbound: first outer iteration; the domain
  // premise makes every string nonempty, so d always binds).
  claim
    <k>
      #loop(str(CS:IntSeq), Name("d"),
        If(Compare(
          BinOp("%", Call(Name("int"), Name("d")), Int(2)),
          CmpOp("==", Int(1))),
          Assign(Name("n"), BinOp("+", Name("n"), Int(1))),
          .Stmts))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "odd_count" <- _:Val ], parent(-1))
       1 |-> (
         scope(.Map [ "lst" <- LV:Val ] [ "res" <- ref(AR:Int) ] [ "arr" <- AV:Val ]
                    [ "n" <- N:Int ], parent(0)) =>
         scope(.Map [ "lst" <- LV ] [ "res" <- ref(AR) ] [ "arr" <- AV ]
                    [ "n" <- oddCnt2(CS, N) ] [ "d" <- ?_:Val ], parent(0))
       )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allDigit(CS) andBool 0 <Int isLen(CS)
    [all-path]

  // ---- Outer append invariant, variant C (arr/n/d all bound).
  claim
    <k>
      #loop(list(VS:ValSeq), Name("arr"),
        Assign(Name("n"), Int(0))
        For(Name("d"), Name("arr"),
          If(Compare(
            BinOp("%", Call(Name("int"), Name("d")), Int(2)),
            CmpOp("==", Int(1))),
            Assign(Name("n"), BinOp("+", Name("n"), Int(1))),
            .Stmts))
        Expr(
          Call(
            Attribute(Name("res"), "append"),
            BinOp(
              "+",
              BinOp(
                "+",
                BinOp(
                  "+",
                  BinOp(
                    "+",
                    BinOp(
                      "+",
                      BinOp(
                        "+",
                        BinOp(
                          "+",
                          BinOp(
                            "+",
                            Str("the number of odd elements "),
                            Call(Name("str"), Name("n"))),
                          Str("n the str")),
                        Call(Name("str"), Name("n"))),
                      Str("ng ")),
                    Call(Name("str"), Name("n"))),
                  Str(" of the ")),
                Call(Name("str"), Name("n"))),
              Str("nput.")))))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "odd_count" <- _:Val ], parent(-1))
       1 |-> (
         scope(.Map [ "lst" <- LV:Val ] [ "res" <- ref(AR:Int) ] [ "arr" <- _:Val ]
                    [ "n" <- _:Val ] [ "d" <- _:Val ], parent(0)) =>
         scope(.Map [ "lst" <- LV ] [ "res" <- ref(AR) ]
                    [ "arr" <- ?_:Val ] [ "n" <- ?_:Val ] [ "d" <- ?_:Val ], parent(0))
       )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (AR |-> list(ACC:ValSeq)) HREST:Map
        => (AR |-> list(msgFold(VS, ACC))) HREST </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allDigS(VS)
    [all-path]

  // ---- Outer variant A (pre-first-iteration).
  claim
    <k>
      #loop(list(VS:ValSeq), Name("arr"),
        Assign(Name("n"), Int(0))
        For(Name("d"), Name("arr"),
          If(Compare(
            BinOp("%", Call(Name("int"), Name("d")), Int(2)),
            CmpOp("==", Int(1))),
            Assign(Name("n"), BinOp("+", Name("n"), Int(1))),
            .Stmts))
        Expr(
          Call(
            Attribute(Name("res"), "append"),
            BinOp(
              "+",
              BinOp(
                "+",
                BinOp(
                  "+",
                  BinOp(
                    "+",
                    BinOp(
                      "+",
                      BinOp(
                        "+",
                        BinOp(
                          "+",
                          BinOp(
                            "+",
                            Str("the number of odd elements "),
                            Call(Name("str"), Name("n"))),
                          Str("n the str")),
                        Call(Name("str"), Name("n"))),
                      Str("ng ")),
                    Call(Name("str"), Name("n"))),
                  Str(" of the ")),
                Call(Name("str"), Name("n"))),
              Str("nput.")))))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "odd_count" <- _:Val ], parent(-1))
       1 |-> (
         scope(.Map [ "lst" <- LV:Val ] [ "res" <- ref(AR:Int) ], parent(0)) =>
         scope(.Map [ "lst" <- LV ] [ "res" <- ref(AR) ]
                    [ "arr" <- ?_:Val ] [ "n" <- ?_:Val ] [ "d" <- ?_:Val ], parent(0))
       )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (AR |-> list(ACC:ValSeq)) HREST:Map
        => (AR |-> list(msgFold(VS, ACC))) HREST </heap>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allDigS(VS) andBool 0 <Int vsLen(VS)
    [all-path]

  // ---- Entry claim -- the REAL canonical-shape code, verbatim .mpy.
  claim
    <k>
      FuncDef("odd_count", Params("lst"),
        Assign(Name("res"), ListExpr(.Exprs))
        For(Name("arr"), Name("lst"),
          Assign(Name("n"), Int(0))
        For(Name("d"), Name("arr"),
          If(Compare(
            BinOp("%", Call(Name("int"), Name("d")), Int(2)),
            CmpOp("==", Int(1))),
            Assign(Name("n"), BinOp("+", Name("n"), Int(1))),
            .Stmts))
        Expr(
          Call(
            Attribute(Name("res"), "append"),
            BinOp(
              "+",
              BinOp(
                "+",
                BinOp(
                  "+",
                  BinOp(
                    "+",
                    BinOp(
                      "+",
                      BinOp(
                        "+",
                        BinOp(
                          "+",
                          BinOp(
                            "+",
                            Str("the number of odd elements "),
                            Call(Name("str"), Name("n"))),
                          Str("n the str")),
                        Call(Name("str"), Name("n"))),
                      Str("ng ")),
                    Call(Name("str"), Name("n"))),
                  Str(" of the ")),
                Call(Name("str"), Name("n"))),
              Str("nput.")))))
        Return(Name("res")))
      Assign(Name("result"), Call(Name("odd_count"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "odd_count" <- ?_:Val ]
                       [ "result" <- ref(?NO:Int) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => (?NO |-> list(msgFold(VS, .ValSeq))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allDigS(VS)
    [all-path]
endmodule
