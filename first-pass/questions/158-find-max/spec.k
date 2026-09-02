// spec.k — find_max on the UNIFIED semantics (src/). List-of-strings argmax-FIRST reduce with a
// lex-smallest tie-break on distinct-char count. Elements are symbolic str Vals under allStr;
// len(set(w)) and w < best are the trusted opaque primitives (see verification.k). The body's
// `best = w if beats else best` IfExp case-splits on beats, aligning with findBest's guarded split.
//
//   kompile verification.k --backend haskell \
//     --main-module FIND-MAX-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module FIND-MAX-SPEC

requires "verification.k"

module FIND-MAX-SPEC
  imports FIND-MAX-VERIFICATION

  // ---- Loop invariant (circularity) — over VS from (best=BEST, best_d=BD) the loop leaves
  // best := findBest(VS, BEST, BD), best_d := finalD(VS, BEST, BD). Induction on VS; each body
  // step recomputes d = distinct(w), beats, and case-splits `best = w if beats else best`.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("w"),
        Assign(Name("d"), Call(Name("len"), Call(Name("set"), Name("w"))))
        Assign(Name("beats"),
          BoolOp("or",
            Compare(Name("d"), CmpOp(">", Name("best_d"))),
            BoolOp("and",
              Compare(Name("d"), CmpOp("==", Name("best_d"))),
              Compare(Name("w"), CmpOp("<", Name("best"))))))
        Assign(Name("best"),   IfExp(Name("beats"), Name("w"), Name("best")))
        Assign(Name("best_d"), IfExp(Name("beats"), Name("d"), Name("best_d"))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "find_max" <- FB0:Val ], parent(-1))  L |-> (
        scope(.Map [ "words" <- WV:Val ] [ "best" <- BEST:Val ] [ "best_d" <- BD:Int ]
                   [ "w" <- _:Val ] [ "d" <- _:Val ] [ "beats" <- _:Val ], parent(GLB:Int)) =>
        scope(.Map [ "words" <- WV ] [ "best" <- findBest(VS, BEST, BD) ] [ "best_d" <- finalD(VS, BEST, BD) ]
                   [ "w" <- ?_:Val ] [ "d" <- ?_:Val ] [ "beats" <- ?_:Val ], parent(GLB))
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(VS) andBool isStr(BEST)
    [all-path]

  // ---- Entry claim — result = find_max(list(vCons(str(XC0), REST))) == the word with the maximum
  // number of distinct characters, lex-smallest on ties. Seed best = words[0] = str(XC0),
  // best_d = distinct(str(XC0)). words is non-empty (the canonical reads words[0]).
  claim
    <k>
      FuncDef("find_max", Params("words"),
        Assign(Name("best"), Subscript(Name("words"), Int(0)))
        Assign(Name("best_d"), Call(Name("len"), Call(Name("set"), Subscript(Name("words"), Int(0)))))
        Assign(Name("w"), Str(""))
        Assign(Name("d"), Int(0))
        Assign(Name("beats"), Bool(false))
        For(Name("w"), Name("words"),
          Assign(Name("d"), Call(Name("len"), Call(Name("set"), Name("w"))))
          Assign(Name("beats"),
            BoolOp("or",
              Compare(Name("d"), CmpOp(">", Name("best_d"))),
              BoolOp("and",
                Compare(Name("d"), CmpOp("==", Name("best_d"))),
                Compare(Name("w"), CmpOp("<", Name("best"))))))
          Assign(Name("best"),   IfExp(Name("beats"), Name("w"), Name("best")))
          Assign(Name("best_d"), IfExp(Name("beats"), Name("d"), Name("best_d"))))
        Return(Name("best")))
      Assign(Name("result"), Call(Name("find_max"), list(vCons(str(XC0:IntSeq), REST:ValSeq))))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "find_max" <- ?_:Val ]
                       [ "result" <- findBest(vCons(str(XC0), REST), str(XC0), distinct(str(XC0))) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(REST)
    [all-path]
endmodule
