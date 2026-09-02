// spec.k — can_arrange proof on the UNIFIED semantics (src/).
// The canonical indexes arr[i]/arr[i-1] at a symbolic i (intractable); solution.py is
// the equivalent adjacent-compare fold with a `prev` accumulator (triple: ind, prev, i).

requires "verification.k"

module CAN-ARRANGE-SPEC
  imports CAN-ARRANGE-VERIFICATION

  // ---- Loop invariant (circularity) — from (ind=ID, i=IDX, prev=PV) the loop leaves
  // ind := canArrFrom(VS, IDX, PV, ID), i := IDX +Int vsLen(VS), prev := lastOfV(VS, PV).
  // Induction on VS; the nested If splits on i>=1 then x<prev.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("x"),
        If(Compare(Name("i"), CmpOp(">=", Int(1))),
          If(Compare(Name("x"), CmpOp("<", Name("prev"))),
            Assign(Name("ind"), Name("i")),
            .Stmts),
          .Stmts)
        Assign(Name("prev"), Name("x"))
        Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "arr" <- AV:Val ] [ "ind" <- ID:Int ] [ "i" <- IDX:Int ] [ "prev" <- PV:Val ] [ "x" <- _:Val ], P:Parent) =>
        scope(.Map [ "arr" <- AV ] [ "ind" <- canArrFrom(VS, IDX, PV, ID) ] [ "i" <- IDX +Int vsLen(VS) ] [ "prev" <- lastOfV(VS, PV) ] [ "x" <- ?_:Val ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS) andBool isInt(PV)
    [all-path]

  // ---- Entry claim — result = can_arrange(list(VS)) == canArrFrom(VS, 0, 0, -1).
  claim
    <k>
      FuncDef("can_arrange", Params("arr"),
        Assign(Name("ind"), UnaryOp("-", Int(1)))
        Assign(Name("i"), Int(0))
        Assign(Name("prev"), Int(0))
        Assign(Name("x"), Int(0))
        For(Name("x"), Name("arr"),
          If(Compare(Name("i"), CmpOp(">=", Int(1))),
            If(Compare(Name("x"), CmpOp("<", Name("prev"))),
              Assign(Name("ind"), Name("i")),
              .Stmts),
            .Stmts)
          Assign(Name("prev"), Name("x"))
          Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
        Return(Name("ind")))
      Assign(Name("result"), Call(Name("can_arrange"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "can_arrange" <- ?_:Val ] [ "result" <- canArrFrom(VS, 0, 0, -1) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]
endmodule
