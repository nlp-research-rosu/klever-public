// spec.k — hex_key proof on the UNIFIED semantics (src/).
// String char-code value-predicate fold: count the prime hex digits (a simpler 64).

requires "verification.k"

module HEX-KEY-SPEC
  imports HEX-KEY-VERIFICATION

  // ---- Loop invariant (circularity) — count := CNT +Int countPH(CS). Induction on CS.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("c"),
        Assign(Name("code"), Call(Name("ord"), Name("c")))
        If(BoolOp("or",
             Compare(Name("code"), CmpOp("==", Int(50))),
             Compare(Name("code"), CmpOp("==", Int(51))),
             Compare(Name("code"), CmpOp("==", Int(53))),
             Compare(Name("code"), CmpOp("==", Int(55))),
             Compare(Name("code"), CmpOp("==", Int(66))),
             Compare(Name("code"), CmpOp("==", Int(68)))),
           Assign(Name("count"), BinOp("+", Name("count"), Int(1))),
           .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "hex_key" <- FB0:Val ], parent(-1))  L |-> (
        scope(.Map [ "num" <- NV:Val ] [ "count" <- CNT:Int ] [ "c" <- _:Val ] [ "code" <- _:Val ], parent(GLB:Int)) =>
        scope(.Map [ "num" <- NV ] [ "count" <- CNT +Int countPH(CS) ] [ "c" <- ?_:Val ] [ "code" <- ?_:Val ], parent(GLB))
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — result = hex_key(str(CS)) == countPH(CS).
  claim
    <k>
      FuncDef("hex_key", Params("num"),
        Assign(Name("count"), Int(0))
        Assign(Name("c"), Str(""))
        Assign(Name("code"), Int(0))
        For(Name("c"), Name("num"),
          Assign(Name("code"), Call(Name("ord"), Name("c")))
          If(BoolOp("or",
               Compare(Name("code"), CmpOp("==", Int(50))),
               Compare(Name("code"), CmpOp("==", Int(51))),
               Compare(Name("code"), CmpOp("==", Int(53))),
               Compare(Name("code"), CmpOp("==", Int(55))),
               Compare(Name("code"), CmpOp("==", Int(66))),
               Compare(Name("code"), CmpOp("==", Int(68)))),
             Assign(Name("count"), BinOp("+", Name("count"), Int(1))),
             .Stmts))
        Return(Name("count")))
      Assign(Name("result"), Call(Name("hex_key"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "hex_key" <- ?_:Val ] [ "result" <- countPH(CS) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
