// spec.k — count_upper proof on the UNIFIED semantics (src/).
// Position-dependent value-predicate count: uppercase vowels at even indices. Parity is
// derived from a manual index i (i % 2 == 0), NOT a flipping Bool flag.

requires "verification.k"

module COUNT-UPPER-SPEC
  imports COUNT-UPPER-VERIFICATION

  // ---- Loop invariant (circularity) — from (count=CNT, i=IDX) the loop leaves
  // count := CNT +Int countUE(CS, IDX) and i := IDX +Int isLen(CS). Induction on CS.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("c"),
        Assign(Name("code"), Call(Name("ord"), Name("c")))
        If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
          If(BoolOp("or",
               Compare(Name("code"), CmpOp("==", Int(65))),
               Compare(Name("code"), CmpOp("==", Int(69))),
               Compare(Name("code"), CmpOp("==", Int(73))),
               Compare(Name("code"), CmpOp("==", Int(79))),
               Compare(Name("code"), CmpOp("==", Int(85)))),
            Assign(Name("count"), BinOp("+", Name("count"), Int(1))),
            .Stmts),
          .Stmts)
        Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "count_upper" <- FB0:Val ], parent(-1))  L |-> (
        scope(.Map [ "s" <- SV:Val ] [ "count" <- CNT:Int ] [ "i" <- IDX:Int ] [ "c" <- _:Val ] [ "code" <- _:Val ], parent(GLB:Int)) =>
        scope(.Map [ "s" <- SV ] [ "count" <- CNT +Int countUE(CS, IDX) ] [ "i" <- IDX +Int isLen(CS) ] [ "c" <- ?_:Val ] [ "code" <- ?_:Val ], parent(GLB))
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — result = count_upper(str(CS)) == countUE(CS, 0).
  claim
    <k>
      FuncDef("count_upper", Params("s"),
        Assign(Name("count"), Int(0))
        Assign(Name("i"), Int(0))
        Assign(Name("c"), Str(""))
        Assign(Name("code"), Int(0))
        For(Name("c"), Name("s"),
          Assign(Name("code"), Call(Name("ord"), Name("c")))
          If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
            If(BoolOp("or",
                 Compare(Name("code"), CmpOp("==", Int(65))),
                 Compare(Name("code"), CmpOp("==", Int(69))),
                 Compare(Name("code"), CmpOp("==", Int(73))),
                 Compare(Name("code"), CmpOp("==", Int(79))),
                 Compare(Name("code"), CmpOp("==", Int(85)))),
              Assign(Name("count"), BinOp("+", Name("count"), Int(1))),
              .Stmts),
            .Stmts)
          Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
        Return(Name("count")))
      Assign(Name("result"), Call(Name("count_upper"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "count_upper" <- ?_:Val ] [ "result" <- countUE(CS, 0) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
