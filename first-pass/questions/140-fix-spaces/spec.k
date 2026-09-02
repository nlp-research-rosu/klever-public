// spec.k — fix_spaces proof on the UNIFIED semantics (src/).
//
//   kompile verification.k --backend haskell \
//     --main-module FIX-SPACES-VERIFICATION --syntax-module FIX-SPACES-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module FIX-SPACES-SPEC

requires "verification.k"

module FIX-SPACES-SPEC
  imports FIX-SPACES-VERIFICATION

  // ---- Loop invariant (the circularity) — see ../3-below-zero/PROOF.md -------
  // Two accumulators (result, rl) over CS.  From (result=str(RESULT), rl=RL) the loop leaves
  //   result := str(fixRes(CS, RESULT, RL))   rl := fixRl(CS, RL)
  // By induction on CS; the nested If (' ' / NUL sentinel / other, then rl ranges) lines up
  // with each summary's branch-split rules.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("ch"),
        If(Compare(Name("ch"), CmpOp("==", Str(" "))),
           Assign(Name("rl"), BinOp("+", Name("rl"), Int(1))),
           If(Compare(Name("ch"), CmpOp("==", Call(Name("chr"), Int(0)))),
              If(Compare(Name("rl"), CmpOp(">", Int(2))),
                 Assign(Name("result"), BinOp("+", Name("result"), Str("-"))),
                 If(Compare(Name("rl"), CmpOp(">", Int(0))),
                    Assign(Name("result"), BinOp("+", Name("result"), Str("_"))),
                    .Stmts))
              Assign(Name("rl"), Int(0)),
              If(Compare(Name("rl"), CmpOp(">", Int(2))),
                 Assign(Name("result"), BinOp("+", Name("result"), Str("-"))),
                 If(Compare(Name("rl"), CmpOp("==", Int(2))),
                    Assign(Name("result"), BinOp("+", Name("result"), Str("__"))),
                    If(Compare(Name("rl"), CmpOp("==", Int(1))),
                       Assign(Name("result"), BinOp("+", Name("result"), Str("_"))),
                       .Stmts)))
              Assign(Name("result"), BinOp("+", Name("result"), Name("ch")))
              Assign(Name("rl"), Int(0))))
        )
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "fix_spaces" <- FB0:Val ], parent(-1))  L |-> ( scope(.Map [ "text" <- TV:Val ] [ "result" <- str(RESULT:IntSeq) ] [ "rl" <- RL:Int ]
                              [ "ch" <- _:Val ], parent(GLB:Int))
               => scope(.Map [ "text" <- TV ] [ "result" <- str(fixRes(CS, RESULT, RL)) ]
                              [ "rl" <- fixRl(CS, RL) ] [ "ch" <- ?_:Val ], parent(GLB)) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — see ../3-below-zero/PROOF.md ----------------------------
  // After `result = fix_spaces(str(CS))`, the root scope's result is fixRes over CS with a
  // trailing NUL sentinel (which flushes the last run): for symbolic CS.
  claim
    <k>
      FuncDef("fix_spaces", Params("text"),
        Assign(Name("result"), Str(""))
        Assign(Name("rl"), Int(0))
        Assign(Name("ch"), Str(""))
        For(Name("ch"), BinOp("+", Name("text"), Call(Name("chr"), Int(0))),
          If(Compare(Name("ch"), CmpOp("==", Str(" "))),
             Assign(Name("rl"), BinOp("+", Name("rl"), Int(1))),
             If(Compare(Name("ch"), CmpOp("==", Call(Name("chr"), Int(0)))),
                If(Compare(Name("rl"), CmpOp(">", Int(2))),
                   Assign(Name("result"), BinOp("+", Name("result"), Str("-"))),
                   If(Compare(Name("rl"), CmpOp(">", Int(0))),
                      Assign(Name("result"), BinOp("+", Name("result"), Str("_"))),
                      .Stmts))
                Assign(Name("rl"), Int(0)),
                If(Compare(Name("rl"), CmpOp(">", Int(2))),
                   Assign(Name("result"), BinOp("+", Name("result"), Str("-"))),
                   If(Compare(Name("rl"), CmpOp("==", Int(2))),
                      Assign(Name("result"), BinOp("+", Name("result"), Str("__"))),
                      If(Compare(Name("rl"), CmpOp("==", Int(1))),
                         Assign(Name("result"), BinOp("+", Name("result"), Str("_"))),
                         .Stmts)))
                Assign(Name("result"), BinOp("+", Name("result"), Name("ch")))
                Assign(Name("rl"), Int(0)))))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("fix_spaces"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "fix_spaces" <- ?_:Val ]
                       [ "result" <- str(fixRes(seqConcat(CS, iCons(0, .IntSeq)), .IntSeq, 0)) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
