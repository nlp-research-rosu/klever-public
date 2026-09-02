requires "verification.k"

module DECODE-SHIFT-SPEC
  imports DECODE-SHIFT-VERIFICATION

  // ---- Loop invariant (circularity) — string char-map. From result=str(R) the loop
  // appends chr(dshift(code)) per char, leaving result := str(seqConcat(R, decShift(CS))).
  // Induction on CS; result + chr(...) is a concrete str concat (no projection needed).
  claim
    <k>
      #loop(str(CS:IntSeq), Name("ch"),
        Assign(Name("result"),
          BinOp("+", Name("result"),
            Call(Name("chr"),
              BinOp("+", BinOp("%", BinOp("-", BinOp("-", Call(Name("ord"), Name("ch")), Int(5)), Int(97)), Int(26)), Int(97))))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "decode_shift" <- FB0:Val ], parent(-1))  L |-> (
        scope(.Map [ "s" <- SV:Val ] [ "result" <- str(R:IntSeq) ] [ "ch" <- _:Val ], parent(GLB:Int)) =>
        scope(.Map [ "s" <- SV ] [ "result" <- ?RV:Val ] [ "ch" <- ?_:Val ], parent(GLB))
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?RV ==K str(seqConcat(R, decShift(CS)))
    [all-path]

  // ---- Entry claim — result = decode_shift(str(CS)) == str(decShift(CS)).
  claim
    <k>
      FuncDef("decode_shift", Params("s"),
        Assign(Name("result"), Str(""))
        Assign(Name("ch"), Str(""))
        For(Name("ch"), Name("s"),
          Assign(Name("result"),
            BinOp("+", Name("result"),
              Call(Name("chr"),
                BinOp("+", BinOp("%", BinOp("-", BinOp("-", Call(Name("ord"), Name("ch")), Int(5)), Int(97)), Int(26)), Int(97))))))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("decode_shift"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "decode_shift" <- ?_:Val ] [ "result" <- ?R:Val ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==K str(decShift(CS))
    [all-path]
endmodule
