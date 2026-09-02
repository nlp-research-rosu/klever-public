// spec.k — separate_paren_groups proof on the UNIFIED semantics (src/).
// 3-accumulator scan (result list, current string, depth) emitting a list of groups.

requires "verification.k"

module SEPARATE-PAREN-GROUPS-SPEC
  imports SEPARATE-PAREN-GROUPS-VERIFICATION

  // ---- Loop invariant (circularity) — from (result=list(R), current=str(CUR), depth=D)
  // the loop leaves result := list(valSeqConcat(R, groupsOf(CS, D, CUR))),
  // current := str(curAfter(CS, D, CUR)), depth := depthAfter(CS, D). Induction on CS.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("c"),
        If(Compare(Name("c"), CmpOp("==", Str("("))),
          Assign(Name("current"), BinOp("+", Name("current"), Name("c")))
          Assign(Name("depth"), BinOp("+", Name("depth"), Int(1))),
          If(Compare(Name("c"), CmpOp("==", Str(")"))),
            Assign(Name("current"), BinOp("+", Name("current"), Name("c")))
            Assign(Name("depth"), BinOp("-", Name("depth"), Int(1)))
            If(Compare(Name("depth"), CmpOp("==", Int(0))),
              Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Name("current"))))
              Assign(Name("current"), Str("")),
              .Stmts),
            .Stmts)))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "paren_string" <- PV:Val ] [ "result" <- ref(HN1_0:Int) ] [ "current" <- str(CUR:IntSeq) ] [ "depth" <- D:Int ] [ "c" <- _:Val ], P:Parent) =>
        scope(.Map [ "paren_string" <- PV ] [ "result" <- ref(?HN1_0B:Int) ] [ "current" <- str(curAfter(CS, D, CUR)) ] [ "depth" <- depthAfter(CS, D) ] [ "c" <- ?_:Val ], P)
      ) ...
    </scopes>
    <heap> (HN1_0 |-> list(R:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(valSeqConcat(R, groupsOf(CS, D, CUR)))) ?_:Map </heap>
    <heapLoc> HLC1:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
    [all-path]

  // ---- Entry claim — result = separate_paren_groups(str(CS)) == groupsOf(CS, 0, .IntSeq).
  claim
    <k>
      FuncDef("separate_paren_groups", Params("paren_string"),
        Assign(Name("result"), ListExpr(.Exprs))
        Assign(Name("current"), Str(""))
        Assign(Name("depth"), Int(0))
        Assign(Name("c"), Str(""))
        For(Name("c"), Name("paren_string"),
          If(Compare(Name("c"), CmpOp("==", Str("("))),
            Assign(Name("current"), BinOp("+", Name("current"), Name("c")))
            Assign(Name("depth"), BinOp("+", Name("depth"), Int(1))),
            If(Compare(Name("c"), CmpOp("==", Str(")"))),
              Assign(Name("current"), BinOp("+", Name("current"), Name("c")))
              Assign(Name("depth"), BinOp("-", Name("depth"), Int(1)))
              If(Compare(Name("depth"), CmpOp("==", Int(0))),
                Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Name("current"))))
                Assign(Name("current"), Str("")),
                .Stmts),
              .Stmts)))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("separate_paren_groups"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "separate_paren_groups" <- ?_:Val ] [ "result" <- ref(?HN2_0:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?HN2_0 |-> list(groupsOf(CS, 0, .IntSeq))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
