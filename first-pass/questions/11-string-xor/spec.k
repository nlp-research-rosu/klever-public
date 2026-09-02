// spec.k — string_xor proof on the UNIFIED semantics (src/).
// Parallel zip over two strings (reference zipObjS): for x, y in zip(a, b):
// result += "0" if x==y else "1". The canonical uses a nested fn + ''.join (unmodeled).

requires "verification.k"

module STRING-XOR-SPEC
  imports STRING-XOR-VERIFICATION

  // ---- Loop invariant (circularity) — over two code-seqs CA, CB the zip-loop appends
  // "0"/"1" per aligned pair, leaving result := str(seqConcat(R, xorSeq(CA, CB))).
  // Induction on (CA, CB); x == y case-splits to A ==Int B.
  claim
    <k>
      #loop(zipObjS(CA:IntSeq, CB:IntSeq), TupleExpr(Name("x"), Name("y")),
        If(Compare(Name("x"), CmpOp("==", Name("y"))),
           Assign(Name("result"), BinOp("+", Name("result"), Str("0"))),
           Assign(Name("result"), BinOp("+", Name("result"), Str("1")))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "a" <- AV:Val ] [ "b" <- BV:Val ] [ "result" <- str(R:IntSeq) ]
                   [ "x" <- _:Val ] [ "y" <- _:Val ], P:Parent) =>
        scope(.Map [ "a" <- AV ] [ "b" <- BV ] [ "result" <- str(seqConcat(R, xorSeq(CA, CB))) ]
                   [ "x" <- ?_:Val ] [ "y" <- ?_:Val ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — result = string_xor(str(CA), str(CB)) == str(xorSeq(CA, CB)).
  claim
    <k>
      FuncDef("string_xor", Params("a", "b"),
        Assign(Name("result"), Str(""))
        Assign(Name("x"), Str(""))
        Assign(Name("y"), Str(""))
        For(TupleExpr(Name("x"), Name("y")), Call(Name("zip"), Name("a"), Name("b")),
          If(Compare(Name("x"), CmpOp("==", Name("y"))),
             Assign(Name("result"), BinOp("+", Name("result"), Str("0"))),
             Assign(Name("result"), BinOp("+", Name("result"), Str("1")))))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("string_xor"), str(CA:IntSeq) , str(CB:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "string_xor" <- ?_:Val ] [ "result" <- str(xorSeq(CA, CB)) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
