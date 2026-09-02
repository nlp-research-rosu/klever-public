// spec.k — filter_by_substring proof on the UNIFIED semantics (src/).
// The canonical is [x for x in strings if substring in x]; its comprehension makes
// `substring` a free var in the closure parent scope (see comprehension-free-var-predicate).
// solution.py is the equivalent explicit filter loop, still using substring `in`.

requires "verification.k"

module FILTER-BY-SUBSTRING-SPEC
  imports FILTER-BY-SUBSTRING-VERIFICATION

  // ---- Loop invariant (circularity) — substring filter. From result=list(R) the loop
  // appends each element containing substring, leaving
  // result := list(valSeqConcat(R, filterSub(SC, VS))). Induction on VS.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("x"),
        If(Compare(Name("substring"), CmpOp("in", Name("x"))),
           Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Name("x")))),
           .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "strings" <- SV:Val ] [ "substring" <- str(SC:IntSeq) ] [ "result" <- ref(HN1_0:Int) ] [ "x" <- _:Val ], P:Parent) =>
        scope(.Map [ "strings" <- SV ] [ "substring" <- str(SC) ] [ "result" <- ref(?HN1_0B:Int) ] [ "x" <- ?_:Val ], P)
      ) ...
    </scopes>
    <heap> (HN1_0 |-> list(R:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(valSeqConcat(R, filterSub(SC, VS)))) ?_:Map </heap>
    <heapLoc> HLC1:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(VS)
     andBool 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
    [all-path]

  // ---- Entry claim — result = filter_by_substring(list(VS), str(SC)) == filterSub(SC, VS).
  claim
    <k>
      FuncDef("filter_by_substring", Params("strings", "substring"),
        Assign(Name("result"), ListExpr(.Exprs))
        Assign(Name("x"), Str(""))
        For(Name("x"), Name("strings"),
          If(Compare(Name("substring"), CmpOp("in", Name("x"))),
             Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Name("x")))),
             .Stmts))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("filter_by_substring"), list(VS:ValSeq) , str(SC:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "filter_by_substring" <- ?_:Val ] [ "result" <- ref(?HN2_0:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?HN2_0 |-> list(filterSub(SC, VS))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(VS)
    [all-path]
endmodule
