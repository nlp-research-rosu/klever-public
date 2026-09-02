requires "verification.k"

module ODD-AT-EVEN-SPEC
  imports ODD-AT-EVEN-VERIFICATION

  // ---- Loop invariant (circularity) — position-dependent fold. From (result=R, i=I)
  // the loop leaves result := R +Int sumOE(VS, I) and i := I +Int vsLen(VS).
  // Induction on VS; the nested If splits on i%2 then e%2.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("e"),
        If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
          If(Compare(BinOp("%", Name("e"), Int(2)), CmpOp("==", Int(1))),
            Assign(Name("result"), BinOp("+", Name("result"), Name("e"))),
            .Stmts),
          .Stmts)
        Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "lst" <- LV:Val ] [ "result" <- R:Int ] [ "i" <- I:Int ] [ "e" <- _:Val ], P:Parent) =>
        scope(.Map [ "lst" <- LV ] [ "result" <- ?R2:Int ]
                   [ "i" <- ?I2:Int ] [ "e" <- ?_:Val ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    ensures ?R2 ==Int R +Int sumOE(intListOf(VS), I) andBool ?I2 ==Int I +Int vsLen(VS)
    [all-path]

  // ---- Entry claim — result = solution(list(VS)) == sumOE(intListOf(VS), 0).
  claim
    <k>
      FuncDef("solution", Params("lst"),
        Assign(Name("result"), Int(0))
        Assign(Name("i"), Int(0))
        Assign(Name("e"), Int(0))
        For(Name("e"), Name("lst"),
          If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
            If(Compare(BinOp("%", Name("e"), Int(2)), CmpOp("==", Int(1))),
              Assign(Name("result"), BinOp("+", Name("result"), Name("e"))),
              .Stmts),
            .Stmts)
          Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("solution"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "solution" <- ?_:Val ] [ "result" <- ?R:Int ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    ensures ?R ==Int sumOE(intListOf(VS), 0)
    [all-path]
endmodule
