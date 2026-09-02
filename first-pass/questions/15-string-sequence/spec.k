// spec.k — string_sequence on the UNIFIED semantics (src/). Range-loop string-build invariant + entry.
// See ./PROOF.md.
//
//   kompile verification.k --backend haskell --main-module STRING-SEQUENCE-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module STRING-SEQUENCE-SPEC

requires "verification.k"

module STRING-SEQUENCE-SPEC
  imports STRING-SEQUENCE-VERIFICATION

  // ---- Loop invariant (circularity) — over rangeObj(K, HI, 1) from result = str(RC) the loop appends
  // " " + str(x) each step, leaving result := str(seqFold(K, HI, RC)). `str(x)` reduces to str(digitCodes(x))
  // (x >= K >= 1 >= 0); `str(RC) + " " + str(digitCodes(x))` concatenates via str-+ (seqConcat). `x` bound.
  claim
    <k>
      #loop(rangeObj(K:Int, HI:Int, 1), Name("x"),
        Assign(Name("result"),
          BinOp("+", BinOp("+", Name("result"), Str(" ")), Call(Name("str"), Name("x")))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "string_sequence" <- FB0:Val ], parent(-1))  L |-> ( scope(.Map [ "n" <- NV:Val ] [ "result" <- str(RC:IntSeq) ] [ "x" <- _:Val ], parent(GLB:Int))
               => scope(.Map [ "n" <- NV ] [ "result" <- str(?SC:IntSeq) ] [ "x" <- ?_:Val ], parent(GLB)) ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires K >=Int 1
    ensures ?SC ==K seqFold(K, HI, RC)
    [all-path]

  // ---- Entry — result = string_sequence(N) == strSeqRes(N) = "0 1 2 ... N". result starts str(0) =
  // str([48]); the loop over range(1, N+1) leaves result := str(seqFold(1, N+1, [48])). Domain N >= 0.
  claim
    <k>
      FuncDef("string_sequence", Params("n"),
        Assign(Name("result"), Call(Name("str"), Int(0)))
        Assign(Name("x"), Int(0))
        For(Name("x"), Call(Name("range"), Int(1), BinOp("+", Name("n"), Int(1))),
          Assign(Name("result"),
            BinOp("+", BinOp("+", Name("result"), Str(" ")), Call(Name("str"), Name("x")))))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("string_sequence"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "string_sequence" <- ?_:Val ] [ "result" <- strSeqRes(N) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
    [all-path]
endmodule
