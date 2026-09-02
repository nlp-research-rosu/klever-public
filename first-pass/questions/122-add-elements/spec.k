// spec.k — add_elements proof on the UNIFIED semantics (src/).
// Index-bounded value-predicate sum: sum the <=2-digit elements (-9..99) among the first
// k. The canonical is sum(elem for elem in arr[:k] if len(str(elem)) <= 2).

requires "verification.k"

module ADD-ELEMENTS-SPEC
  imports ADD-ELEMENTS-VERIFICATION

  // ---- Loop invariant (circularity) — from (total=T, i=IDX) the loop leaves
  // total := T +Int addEl(VS, IDX, K) and i := IDX +Int vsLen(VS). Induction on VS;
  // the nested If splits on i<k then -9<=x<=99.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("x"),
        If(Compare(Name("i"), CmpOp("<", Name("k"))),
          If(BoolOp("and", Compare(Name("x"), CmpOp(">=", UnaryOp("-", Int(9)))), Compare(Name("x"), CmpOp("<=", Int(99)))),
            Assign(Name("total"), BinOp("+", Name("total"), Name("x"))),
            .Stmts),
          .Stmts)
        Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "arr" <- AV:Val ] [ "k" <- K:Int ] [ "total" <- T:Int ] [ "i" <- IDX:Int ] [ "x" <- _:Val ], P:Parent) =>
        scope(.Map [ "arr" <- AV ] [ "k" <- K ] [ "total" <- T +Int addEl(VS, IDX, K) ] [ "i" <- IDX +Int vsLen(VS) ] [ "x" <- ?_:Val ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]

  // ---- Entry claim — result = add_elements(list(VS), K) == addEl(VS, 0, K).
  claim
    <k>
      FuncDef("add_elements", Params("arr", "k"),
        Assign(Name("total"), Int(0))
        Assign(Name("i"), Int(0))
        Assign(Name("x"), Int(0))
        For(Name("x"), Name("arr"),
          If(Compare(Name("i"), CmpOp("<", Name("k"))),
            If(BoolOp("and", Compare(Name("x"), CmpOp(">=", UnaryOp("-", Int(9)))), Compare(Name("x"), CmpOp("<=", Int(99)))),
              Assign(Name("total"), BinOp("+", Name("total"), Name("x"))),
              .Stmts),
            .Stmts)
          Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
        Return(Name("total")))
      Assign(Name("result"), Call(Name("add_elements"), list(VS:ValSeq) , K:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "add_elements" <- ?_:Val ] [ "result" <- addEl(VS, 0, K) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]
endmodule
