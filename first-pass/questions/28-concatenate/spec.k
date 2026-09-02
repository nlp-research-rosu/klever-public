requires "verification.k"

module CONCATENATE-SPEC
  imports CONCATENATE-VERIFICATION

  // ---- Loop invariant (circularity) — over a list of strings VS, the loop appends
  // each string, leaving result := str(seqConcat(R, concatVS(VS))). Induction on VS.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("s"),
        Assign(Name("result"), BinOp("+", Name("result"), Name("s"))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "strings" <- SV:Val ] [ "result" <- str(R:IntSeq) ] [ "s" <- _:Val ], P:Parent) =>
        scope(.Map [ "strings" <- SV ] [ "result" <- ?RV:Val ] [ "s" <- ?_:Val ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(VS)
    ensures ?RV ==K str(seqConcat(R, concatVS(strListOf(VS))))
    [all-path]

  // ---- Entry claim — result = concatenate(list(VS)) == str(concatVS(strListOf(VS))).
  claim
    <k>
      FuncDef("concatenate", Params("strings"),
        Assign(Name("result"), Str(""))
        Assign(Name("s"), Str(""))
        For(Name("s"), Name("strings"),
          Assign(Name("result"), BinOp("+", Name("result"), Name("s"))))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("concatenate"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "concatenate" <- ?_:Val ] [ "result" <- ?R:Val ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(VS)
    ensures ?R ==K str(concatVS(strListOf(VS)))
    [all-path]
endmodule
