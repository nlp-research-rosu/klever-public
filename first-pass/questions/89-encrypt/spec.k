// spec.k — encrypt proof on the UNIFIED semantics (src/).
// Rotate lowercase letters down 4 (a-z), else unchanged. The canonical uses d.index(c)
// + d[...] indexing into the alphabet; solution.py is the equivalent ord-arithmetic map.

requires "verification.k"

module ENCRYPT-SPEC
  imports ENCRYPT-VERIFICATION

  // ---- Loop invariant (circularity) — string char-map. From out=str(R) the loop appends
  // chr(encC(code)) per char, leaving out := str(seqConcat(R, encMap(CS))). Induction on CS.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("c"),
        Assign(Name("code"), Call(Name("ord"), Name("c")))
        Assign(Name("new"), Name("code"))
        If(BoolOp("and", Compare(Name("code"), CmpOp(">=", Int(97))), Compare(Name("code"), CmpOp("<=", Int(122)))),
          Assign(Name("new"), BinOp("+", BinOp("%", BinOp("+", BinOp("-", Name("code"), Int(97)), Int(4)), Int(26)), Int(97))),
          .Stmts)
        Assign(Name("out"), BinOp("+", Name("out"), Call(Name("chr"), Name("new")))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "encrypt" <- FB0:Val ], parent(-1))  L |-> (
        scope(.Map [ "s" <- SV:Val ] [ "out" <- str(R:IntSeq) ] [ "c" <- _:Val ] [ "code" <- _:Val ] [ "new" <- _:Val ], parent(GLB:Int)) =>
        scope(.Map [ "s" <- SV ] [ "out" <- str(seqConcat(R, encMap(CS))) ] [ "c" <- ?_:Val ] [ "code" <- ?_:Val ] [ "new" <- ?_:Val ], parent(GLB))
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — result = encrypt(str(CS)) == str(encMap(CS)).
  claim
    <k>
      FuncDef("encrypt", Params("s"),
        Assign(Name("out"), Str(""))
        Assign(Name("c"), Str(""))
        Assign(Name("code"), Int(0))
        Assign(Name("new"), Int(0))
        For(Name("c"), Name("s"),
          Assign(Name("code"), Call(Name("ord"), Name("c")))
          Assign(Name("new"), Name("code"))
          If(BoolOp("and", Compare(Name("code"), CmpOp(">=", Int(97))), Compare(Name("code"), CmpOp("<=", Int(122)))),
            Assign(Name("new"), BinOp("+", BinOp("%", BinOp("+", BinOp("-", Name("code"), Int(97)), Int(4)), Int(26)), Int(97))),
            .Stmts)
          Assign(Name("out"), BinOp("+", Name("out"), Call(Name("chr"), Name("new")))))
        Return(Name("out")))
      Assign(Name("result"), Call(Name("encrypt"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "encrypt" <- ?_:Val ] [ "result" <- str(encMap(CS)) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
