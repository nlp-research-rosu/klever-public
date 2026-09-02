// spec.k — solve proof on the UNIFIED semantics (src/).
// 3 accumulators: swapcase-map (swapped), reverse (rev), any-letter flag (has_alpha).
// Return swapped if any letter, else the reversed string.

requires "verification.k"

module SOLVE-SPEC
  imports SOLVE-VERIFICATION

  // ---- Loop invariant (circularity) — from (swapped=str(SW), rev=str(RV),
  // has_alpha=HA) the loop leaves swapped := str(seqConcat(SW, sSwapMap(CS))),
  // rev := str(revPrep(CS, RV)), has_alpha := HA orBool sHasAlpha(CS). Induction on CS.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("c"),
        Assign(Name("code"), Call(Name("ord"), Name("c")))
        Assign(Name("new"), Name("code"))
        If(BoolOp("and", Compare(Name("code"), CmpOp(">=", Int(65))), Compare(Name("code"), CmpOp("<=", Int(90)))),
          Assign(Name("new"), BinOp("+", Name("code"), Int(32)))
          Assign(Name("has_alpha"), Bool(true)),
          If(BoolOp("and", Compare(Name("code"), CmpOp(">=", Int(97))), Compare(Name("code"), CmpOp("<=", Int(122)))),
            Assign(Name("new"), BinOp("-", Name("code"), Int(32)))
            Assign(Name("has_alpha"), Bool(true)),
            .Stmts))
        Assign(Name("swapped"), BinOp("+", Name("swapped"), Call(Name("chr"), Name("new"))))
        Assign(Name("rev"), BinOp("+", Name("c"), Name("rev"))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "solve" <- FB0:Val ], parent(-1))  L |-> (
        scope(.Map [ "s" <- SV:Val ] [ "has_alpha" <- HA:Bool ] [ "swapped" <- str(SW:IntSeq) ] [ "rev" <- str(RV:IntSeq) ] [ "c" <- _:Val ] [ "code" <- _:Val ] [ "new" <- _:Val ], parent(GLB:Int)) =>
        scope(.Map [ "s" <- SV ] [ "has_alpha" <- HA orBool sHasAlpha(CS) ] [ "swapped" <- str(seqConcat(SW, sSwapMap(CS))) ] [ "rev" <- str(revPrep(CS, RV)) ] [ "c" <- ?_:Val ] [ "code" <- ?_:Val ] [ "new" <- ?_:Val ], parent(GLB))
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — result = solve(str(CS)) ==
  //   #if sHasAlpha(CS) #then str(sSwapMap(CS)) #else str(revPrep(CS, .IntSeq)).
  claim
    <k>
      FuncDef("solve", Params("s"),
        Assign(Name("has_alpha"), Bool(false))
        Assign(Name("swapped"), Str(""))
        Assign(Name("rev"), Str(""))
        Assign(Name("c"), Str(""))
        Assign(Name("code"), Int(0))
        Assign(Name("new"), Int(0))
        For(Name("c"), Name("s"),
          Assign(Name("code"), Call(Name("ord"), Name("c")))
          Assign(Name("new"), Name("code"))
          If(BoolOp("and", Compare(Name("code"), CmpOp(">=", Int(65))), Compare(Name("code"), CmpOp("<=", Int(90)))),
            Assign(Name("new"), BinOp("+", Name("code"), Int(32)))
            Assign(Name("has_alpha"), Bool(true)),
            If(BoolOp("and", Compare(Name("code"), CmpOp(">=", Int(97))), Compare(Name("code"), CmpOp("<=", Int(122)))),
              Assign(Name("new"), BinOp("-", Name("code"), Int(32)))
              Assign(Name("has_alpha"), Bool(true)),
              .Stmts))
          Assign(Name("swapped"), BinOp("+", Name("swapped"), Call(Name("chr"), Name("new"))))
          Assign(Name("rev"), BinOp("+", Name("c"), Name("rev"))))
        Assign(Name("result"), Name("rev"))
        If(Name("has_alpha"),
           Assign(Name("result"), Name("swapped")),
           .Stmts)
        Return(Name("result")))
      Assign(Name("result"), Call(Name("solve"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "solve" <- ?_:Val ]
                       [ "result" <- #if sHasAlpha(CS) #then str(sSwapMap(CS)) #else str(revPrep(CS, .IntSeq)) #fi ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
