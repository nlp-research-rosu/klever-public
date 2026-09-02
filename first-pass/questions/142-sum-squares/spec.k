requires "verification.k"

module SUM-SQUARES-SPEC
  imports SUM-SQUARES-VERIFICATION

  // ---- Loop invariant (circularity) — position-dependent dual fold. From
  // (result=R, i=I) the loop leaves result := R +Int sumSq(VS, I) and
  // i := I +Int vsLen(VS). Induction on VS; the nested If splits on i%3 / i%4.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("e"),
        If(Compare(BinOp("%", Name("i"), Int(3)), CmpOp("==", Int(0))),
          Assign(Name("result"), BinOp("+", Name("result"), BinOp("*", Name("e"), Name("e")))),
          If(Compare(BinOp("%", Name("i"), Int(4)), CmpOp("==", Int(0))),
            Assign(Name("result"), BinOp("+", Name("result"), BinOp("*", BinOp("*", Name("e"), Name("e")), Name("e")))),
            Assign(Name("result"), BinOp("+", Name("result"), Name("e")))))
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
    ensures ?R2 ==Int R +Int sumSq(intListOf(VS), I) andBool ?I2 ==Int I +Int vsLen(VS)
    [all-path]

  // ---- Entry claim — result = sum_squares(list(VS)) == sumSq(intListOf(VS), 0).
  claim
    <k>
      FuncDef("sum_squares", Params("lst"),
        Assign(Name("result"), Int(0))
        Assign(Name("i"), Int(0))
        Assign(Name("e"), Int(0))
        For(Name("e"), Name("lst"),
          If(Compare(BinOp("%", Name("i"), Int(3)), CmpOp("==", Int(0))),
            Assign(Name("result"), BinOp("+", Name("result"), BinOp("*", Name("e"), Name("e")))),
            If(Compare(BinOp("%", Name("i"), Int(4)), CmpOp("==", Int(0))),
              Assign(Name("result"), BinOp("+", Name("result"), BinOp("*", BinOp("*", Name("e"), Name("e")), Name("e")))),
              Assign(Name("result"), BinOp("+", Name("result"), Name("e")))))
          Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("sum_squares"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "sum_squares" <- ?_:Val ] [ "result" <- ?R:Int ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    ensures ?R ==Int sumSq(intListOf(VS), 0)
    [all-path]
endmodule
