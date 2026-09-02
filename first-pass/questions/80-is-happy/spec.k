// spec.k — is_happy proof on the UNIFIED semantics (src/).
// Width-2 window fold over the string's codes: happy iff length >= 3 and every 3
// consecutive letters are distinct. The canonical indexes s[i]/s[i+1]/s[i+2].

requires "verification.k"

module IS-HAPPY-SPEC
  imports IS-HAPPY-VERIFICATION

  // ---- Loop invariant (circularity) — 4 accumulators (happy, i, p1, p2). From
  // (happy=H, i=IDX, p1=P1, p2=P2) the loop leaves happy := happyFold(CS, IDX, P1, P2, H)
  // and i := IDX +Int isLen(CS) (p1/p2 existential). Induction on CS.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("c"),
        Assign(Name("code"), Call(Name("ord"), Name("c")))
        If(Compare(Name("i"), CmpOp(">=", Int(2))),
          If(BoolOp("or",
               Compare(Name("code"), CmpOp("==", Name("p1"))),
               Compare(Name("p1"), CmpOp("==", Name("p2"))),
               Compare(Name("code"), CmpOp("==", Name("p2")))),
            Assign(Name("happy"), Bool(false)),
            .Stmts),
          .Stmts)
        Assign(Name("p2"), Name("p1"))
        Assign(Name("p1"), Name("code"))
        Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "is_happy" <- FB0:Val ], parent(-1))  L |-> (
        scope(.Map [ "s" <- SV:Val ] [ "happy" <- H:Bool ] [ "i" <- IDX:Int ] [ "p1" <- P1:Int ] [ "p2" <- P2:Int ] [ "code" <- _:Val ] [ "c" <- _:Val ], parent(GLB:Int)) =>
        scope(.Map [ "s" <- SV ] [ "happy" <- happyFold(CS, IDX, P1, P2, H) ] [ "i" <- IDX +Int isLen(CS) ] [ "p1" <- ?_:Int ] [ "p2" <- ?_:Int ] [ "code" <- ?_:Val ] [ "c" <- ?_:Val ], parent(GLB))
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — result = is_happy(str(CS)) ==
  //   (isLen(CS) >=Int 3) andBool happyFold(CS, 0, 0, 0, true).
  claim
    <k>
      FuncDef("is_happy", Params("s"),
        Assign(Name("happy"), Bool(true))
        Assign(Name("i"), Int(0))
        Assign(Name("p1"), Int(0))
        Assign(Name("p2"), Int(0))
        Assign(Name("code"), Int(0))
        Assign(Name("c"), Str(""))
        For(Name("c"), Name("s"),
          Assign(Name("code"), Call(Name("ord"), Name("c")))
          If(Compare(Name("i"), CmpOp(">=", Int(2))),
            If(BoolOp("or",
                 Compare(Name("code"), CmpOp("==", Name("p1"))),
                 Compare(Name("p1"), CmpOp("==", Name("p2"))),
                 Compare(Name("code"), CmpOp("==", Name("p2")))),
              Assign(Name("happy"), Bool(false)),
              .Stmts),
            .Stmts)
          Assign(Name("p2"), Name("p1"))
          Assign(Name("p1"), Name("code"))
          Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
        Return(BoolOp("and", Compare(Name("i"), CmpOp(">=", Int(3))), Name("happy"))))
      Assign(Name("result"), Call(Name("is_happy"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "is_happy" <- ?_:Val ]
                       [ "result" <- (isLen(CS) >=Int 3) andBool happyFold(CS, 0, 0, 0, true) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
