// spec.k — median (odd-length) reachability claim on the UNIFIED semantics (src/). Straight-
// line: m = len(l)//2 ; s = sorted(l) ; return s[m]. For odd-length l this is the median.
// sorted() is the trusted primitive (mpy-sort.k); s[m] indexes the opaque sortVS.
//
//   kompile verification.k --backend haskell \
//     --main-module MEDIAN-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module MEDIAN-SPEC

requires "verification.k"

module MEDIAN-SPEC
  imports MEDIAN-VERIFICATION

  // ---- Entry claim — after `result = median(list(VS))`, result == valSeqAt(sortVS(VS),
  // vsLen(VS)/Int 2): the middle element of the sorted list. sorted() => list(sortVS(VS));
  // len(sorted) => vsLen(VS) (sort preserves length); the middle index m = vsLen(VS)/2 >= 0.
  // Indexing the opaque sort is DEFINED because valSeqAt is [total] (mpy-subscript.k).
  claim
    <k>
      FuncDef("median", Params("l"),
        Assign(Name("m"), BinOp("//", Call(Name("len"), Name("l")), Int(2)))
        Assign(Name("s"), Call(Name("sorted"), Name("l")))
        Return(Subscript(Name("s"), Name("m"))))
      Assign(Name("result"), Call(Name("median"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "median" <- ?_:Val ]
                       [ "result" <- valSeqAt(sortVS(VS), vsLen(VS) /Int 2) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    requires vsLen(VS) >=Int 0
    [all-path]
endmodule
