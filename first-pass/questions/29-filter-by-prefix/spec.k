// spec.k — filter_by_prefix proof on the UNIFIED semantics (src/).
// The canonical is [x for x in strings if x.startswith(prefix)]; its comprehension
// makes `prefix` a free var in the closure PARENT scope, whose re-matching on each
// circularity step prevents unifying the two symbolic prefixes. solution.py is the
// equivalent explicit filter loop (prefix in the SAME scope), still using .startswith.

requires "verification.k"

module FILTER-BY-PREFIX-SPEC
  imports FILTER-BY-PREFIX-VERIFICATION

  // ---- Loop invariant (circularity) — string-prefix filter. From result=list(R) the
  // loop appends each element that starts with prefix, leaving
  // result := list(valSeqConcat(R, filterPrefix(PC, VS))). Induction on VS.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("x"),
        If(Call(Attribute(Name("x"), "startswith"), Name("prefix")),
           Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Name("x")))),
           .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "strings" <- SV:Val ] [ "prefix" <- str(PC:IntSeq) ] [ "result" <- ref(HN1_0:Int) ] [ "x" <- _:Val ], P:Parent) =>
        scope(.Map [ "strings" <- SV ] [ "prefix" <- str(PC) ] [ "result" <- ref(?HN1_0B:Int) ] [ "x" <- ?_:Val ], P)
      ) ...
    </scopes>
    <heap> (HN1_0 |-> list(R:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(valSeqConcat(R, filterPrefix(PC, VS)))) ?_:Map </heap>
    <heapLoc> HLC1:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(VS)
     andBool 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
    [all-path]

  // ---- Entry claim — result = filter_by_prefix(list(VS), str(PC)) == filterPrefix(PC, VS).
  claim
    <k>
      FuncDef("filter_by_prefix", Params("strings", "prefix"),
        Assign(Name("result"), ListExpr(.Exprs))
        Assign(Name("x"), Str(""))
        For(Name("x"), Name("strings"),
          If(Call(Attribute(Name("x"), "startswith"), Name("prefix")),
             Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Name("x")))),
             .Stmts))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("filter_by_prefix"), list(VS:ValSeq) , str(PC:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "filter_by_prefix" <- ?_:Val ] [ "result" <- ref(?HN2_0:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?HN2_0 |-> list(filterPrefix(PC, VS))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(VS)
    [all-path]
endmodule
