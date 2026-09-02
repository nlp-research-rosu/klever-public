// spec.k — parse_nested_parens on the UNIFIED semantics (src/). A single flat char-scan over
// `paren_string + ' '` with four accumulators (result/depth/curmax/has). Elements are single-char
// strings; `c == "("` decomposes to a code compare. See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module PARSE-NESTED-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module PARSE-NESTED-SPEC

requires "verification.k"

module PARSE-NESTED-SPEC
  imports PARSE-NESTED-VERIFICATION

  // ---- Loop invariant (circularity) — over the code sequence SS from
  //   (result=list(R), depth=D, curmax=M, has=HAS) the loop leaves
  //   result := list(parseRes(SS,R,D,M,HAS)), depth := parseDepth(SS,D,M,HAS),
  //   curmax := parseMax(SS,D,M,HAS), has := parseHas(SS,D,M,HAS). Induction on SS.
  claim
    <k>
      #loop(str(SS:IntSeq), Name("c"),
        If(Compare(Name("c"), CmpOp("==", Str("("))),
          Assign(Name("depth"), BinOp("+", Name("depth"), Int(1)))
          If(Compare(Name("depth"), CmpOp(">", Name("curmax"))),
            Assign(Name("curmax"), Name("depth")),
            .Stmts)
          Assign(Name("has"), Bool(true)),
          If(Compare(Name("c"), CmpOp("==", Str(" "))),
            If(Name("has"),
              Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Name("curmax"))))
              Assign(Name("depth"), Int(0))
              Assign(Name("curmax"), Int(0))
              Assign(Name("has"), Bool(false)),
              .Stmts),
            Assign(Name("depth"), BinOp("-", Name("depth"), Int(1)))
            Assign(Name("has"), Bool(true)))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "paren_string" <- PV:Val ] [ "result" <- ref(HN1_0:Int) ]
                   [ "depth" <- D:Int ] [ "curmax" <- M:Int ] [ "has" <- HAS:Bool ] [ "c" <- _:Val ], P:Parent) =>
        scope(.Map [ "paren_string" <- PV ] [ "result" <- ref(?HN1_0B:Int) ]
                   [ "depth" <- parseDepth(SS, D, M, HAS) ] [ "curmax" <- parseMax(SS, D, M, HAS) ]
                   [ "has" <- parseHas(SS, D, M, HAS) ] [ "c" <- ?_:Val ], P)
      ) ...
    </scopes>
    <heap> (HN1_0 |-> list(R:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(parseRes(SS, R, D, M, HAS))) ?_:Map </heap>
    <heapLoc> HLC1:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
    [all-path]

  // ---- Entry claim — result = parse_nested_parens(str(CS)) == the per-group max depths. The loop
  // scans str(CS) + " " = str(seqConcat(CS, iCons(32, .IntSeq))); the trailing space flushes.
  claim
    <k>
      FuncDef("parse_nested_parens", Params("paren_string"),
        Assign(Name("result"), ListExpr(.Exprs))
        Assign(Name("depth"), Int(0))
        Assign(Name("curmax"), Int(0))
        Assign(Name("has"), Bool(false))
        Assign(Name("c"), Str(""))
        For(Name("c"), BinOp("+", Name("paren_string"), Str(" ")),
          If(Compare(Name("c"), CmpOp("==", Str("("))),
            Assign(Name("depth"), BinOp("+", Name("depth"), Int(1)))
            If(Compare(Name("depth"), CmpOp(">", Name("curmax"))),
              Assign(Name("curmax"), Name("depth")),
              .Stmts)
            Assign(Name("has"), Bool(true)),
            If(Compare(Name("c"), CmpOp("==", Str(" "))),
              If(Name("has"),
                Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Name("curmax"))))
                Assign(Name("depth"), Int(0))
                Assign(Name("curmax"), Int(0))
                Assign(Name("has"), Bool(false)),
                .Stmts),
              Assign(Name("depth"), BinOp("-", Name("depth"), Int(1)))
              Assign(Name("has"), Bool(true)))))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("parse_nested_parens"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "parse_nested_parens" <- ?_:Val ]
                       [ "result" <- ref(?HN2_0:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?HN2_0 |-> list(parseRes(seqConcat(CS, iCons(32, .IntSeq)), .ValSeq, 0, 0, false))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
