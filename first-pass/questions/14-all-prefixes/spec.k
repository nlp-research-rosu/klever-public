// spec.k — all_prefixes proof on the UNIFIED semantics (src/).
// The canonical is [string[:i+1] for i in range(len(string))] — a symbolic slice,
// intractable; solution.py is the equivalent growing-accumulator scan
// (acc = acc + c; result = result + [acc]).

requires "verification.k"

module ALL-PREFIXES-SPEC
  imports ALL-PREFIXES-VERIFICATION

  // ---- Loop invariant (circularity) — scan with two accumulators. From
  // (acc=str(A), result=list(R)) the loop leaves acc := str(seqConcat(A, CS)) and
  // result := list(valSeqConcat(R, prefixList(A, CS))). Induction on CS.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("c"),
        Assign(Name("acc"), BinOp("+", Name("acc"), Name("c")))
        Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Name("acc")))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "string" <- SV:Val ] [ "result" <- ref(HN1_0:Int) ] [ "acc" <- str(A:IntSeq) ] [ "c" <- _:Val ], P:Parent) =>
        scope(.Map [ "string" <- SV ] [ "result" <- ref(?HN1_0B:Int) ] [ "acc" <- str(seqConcat(A, CS)) ] [ "c" <- ?_:Val ], P)
      ) ...
    </scopes>
    <heap> (HN1_0 |-> list(R:ValSeq)) HRST1:Map
        => (?HN1_0B |-> list(valSeqConcat(R, prefixList(A, CS)))) ?_:Map </heap>
    <heapLoc> HLC1:Int => ?_:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int HN1_0 andBool HN1_0 <Int HLC1 andBool keysBelow(HRST1, HLC1)
    [all-path]

  // ---- Entry claim — result = all_prefixes(str(CS)) == prefixList(.IntSeq, CS).
  claim
    <k>
      FuncDef("all_prefixes", Params("string"),
        Assign(Name("result"), ListExpr(.Exprs))
        Assign(Name("acc"), Str(""))
        Assign(Name("c"), Str(""))
        For(Name("c"), Name("string"),
          Assign(Name("acc"), BinOp("+", Name("acc"), Name("c")))
          Assign(Name("result"), BinOp("+", Name("result"), ListExpr(Name("acc")))))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("all_prefixes"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "all_prefixes" <- ?_:Val ] [ "result" <- ref(?HN2_0:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?HN2_0 |-> list(prefixList(.IntSeq, CS))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
