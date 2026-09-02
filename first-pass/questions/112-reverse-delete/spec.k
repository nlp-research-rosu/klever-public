// spec.k — reverse_delete proof on the UNIFIED semantics (src/).
// Filter s's chars not in c, and check the filtered string is a palindrome; return
// (kept, kept == reverse). The canonical uses a comprehension + ''.join + [::-1] slice.

requires "verification.k"

module REVERSE-DELETE-SPEC
  imports REVERSE-DELETE-VERIFICATION

  // ---- Loop invariant (circularity) — from (kept=str(K), rev=str(R)) the loop leaves
  // kept := str(seqConcat(K, keptOf(CS, CC))), rev := str(revFilt(CS, CC, R)). Induction
  // on CS; `ch not in c` is the substring `in` on the (structural) char and the delete-set.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("ch"),
        If(Compare(Name("ch"), CmpOp("not in", Name("c"))),
          Assign(Name("kept"), BinOp("+", Name("kept"), Name("ch")))
          Assign(Name("rev"), BinOp("+", Name("ch"), Name("rev"))),
          .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "s" <- SV:Val ] [ "c" <- str(CC:IntSeq) ] [ "kept" <- str(K:IntSeq) ] [ "rev" <- str(R:IntSeq) ] [ "ch" <- _:Val ], P:Parent) =>
        scope(.Map [ "s" <- SV ] [ "c" <- str(CC) ] [ "kept" <- str(seqConcat(K, keptOf(CS, CC))) ] [ "rev" <- str(revFilt(CS, CC, R)) ] [ "ch" <- ?_:Val ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — result = reverse_delete(str(CS), str(CC)) ==
  //   tuple(str(keptOf(CS, CC)), keptOf(CS, CC) ==K revFilt(CS, CC, .IntSeq)).
  claim
    <k>
      FuncDef("reverse_delete", Params("s", "c"),
        Assign(Name("kept"), Str(""))
        Assign(Name("rev"), Str(""))
        Assign(Name("ch"), Str(""))
        For(Name("ch"), Name("s"),
          If(Compare(Name("ch"), CmpOp("not in", Name("c"))),
            Assign(Name("kept"), BinOp("+", Name("kept"), Name("ch")))
            Assign(Name("rev"), BinOp("+", Name("ch"), Name("rev"))),
            .Stmts))
        Return(TupleExpr(Name("kept"), Compare(Name("kept"), CmpOp("==", Name("rev"))))))
      Assign(Name("result"), Call(Name("reverse_delete"), str(CS:IntSeq) , str(CC:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "reverse_delete" <- ?_:Val ]
                       [ "result" <- tuple(vCons(str(keptOf(CS, CC)), vCons(keptOf(CS, CC) ==K revFilt(CS, CC, .IntSeq), .ValSeq))) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
