requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-invariant]:
    <k>
      #loop(
        str(IS:IntSeq),
        Name("ch"),
        Assign(Name("code"), Call(Name("ord"), Name("ch")))
        If(
          BoolOp(
            "and",
            Compare(Name("i"), CmpOp(">=", Int(2))),
            BoolOp(
              "or",
              Compare(Name("code"), CmpOp("==", Name("previous1"))),
              Compare(Name("code"), CmpOp("==", Name("previous2"))),
              Compare(Name("previous1"), CmpOp("==", Name("previous2"))))),
          Assign(Name("happy"), Bool(false)),
          .Stmts)
        Assign(Name("previous2"), Name("previous1"))
        Assign(Name("previous1"), Name("code"))
        Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope("is_happy" |-> _:Val, parent(-1))
       1 |-> scope(
              "s"         |-> str(_:IntSeq)
              "happy"     |-> (H:Bool => H andBool scanHappy(IS, I, P2, P1))
              "previous2" |-> (P2:Int => ?FINALP2:Int)
              "previous1" |-> (P1:Int => ?FINALP1:Int)
              "i"         |-> (I:Int => I +Int isLen(IS))
              "ch"        |-> (_:Val => ?FINALCH:Val)
              "code"      |-> (_:Int => ?FINALCODE:Int),
              parent(0))
    </scopes>
    requires I >=Int 2

  claim [is-happy]:
    <k>
      Call(Name("is_happy"), str(IS:IntSeq))
      => ?R:Bool
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
              "is_happy" |->
                closureVal(
                  ("s", .ParamNames),
                  Assign(Name("happy"), Bool(false))
                  Assign(Name("previous2"), UnaryOp("-", Int(1)))
                  Assign(Name("previous1"), UnaryOp("-", Int(1)))
                  Assign(Name("i"), Int(0))
                  Assign(Name("ch"), Str(""))
                  Assign(Name("code"), Int(0))
                  For(
                    Name("ch"),
                    Name("s"),
                    Assign(Name("code"), Call(Name("ord"), Name("ch")))
                    If(
                      BoolOp(
                        "and",
                        Compare(Name("i"), CmpOp(">=", Int(2))),
                        BoolOp(
                          "or",
                          Compare(
                            Name("code"),
                            CmpOp("==", Name("previous1"))),
                          Compare(
                            Name("code"),
                            CmpOp("==", Name("previous2"))),
                          Compare(
                            Name("previous1"),
                            CmpOp("==", Name("previous2"))))),
                      Assign(Name("happy"), Bool(false)),
                      .Stmts)
                    Assign(Name("previous2"), Name("previous1"))
                    Assign(Name("previous1"), Name("code"))
                    Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
                  Return(
                    BoolOp(
                      "and",
                      Compare(Name("i"), CmpOp(">=", Int(3))),
                      Name("happy"))),
                  0),
              parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    ensures ?R ==Bool
      ((isLen(IS) >=Int 3) andBool scanHappy(IS, 0, -1, -1))
endmodule
