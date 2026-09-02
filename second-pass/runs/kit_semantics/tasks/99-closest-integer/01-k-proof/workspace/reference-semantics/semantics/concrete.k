// reference/src/semantics/concrete.k — MPY-CONCRETE
// Concrete-execution-only rules, visible ONLY to the llvm build (run.sh kompiles
// MPY-CONCRETE; verification builds import MPY and never see these). Rationale:
// a k-cell rule matching value constructors NARROWS abstract Vals in the haskell
// backend ([concrete] is not respected on rewrite rules) — probed on
// 26-remove-duplicates, where element compares branched into deepEqVS.

module MPY-CONCRETE
  imports MPY

  // deep equality for list compares whose elements are heap objects
  // (list-of-lists): Python == is structural at every depth.
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
  rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)

  // ==== keyed sort, concrete leg ============================================
  // Computes each key by a REAL call through the uniform #callee machinery
  // (closures, len, type objects all work), stable-inserts on the key, and
  // allocates the result. priority(40) beats sort.k's opaque rules, so krun
  // runs this and proofs (which never see MPY-CONCRETE) keep sortKeyVS.
  syntax Val ::= kvP(Val, Val)
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)

  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)

  syntax Bool ::= kLt(Val, Val) [function]
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
  // v3: mixed Int/Float keys via the exact v2 bridges (float.k), bool keys by
  // the bool->int promotion (True==1, False==0). Unordered pairs (int vs str)
  // stay without a leg — stuck, like CPython's TypeError.
  rule kLt(I:Int, F:Float)   => ltIF(I, F)
  rule kLt(F:Float, I:Int)   => ltFI(F, I)
  rule kLt(B:Bool, V:Val)    => kLt(boolAsInt(B), V) requires isInt(V) orBool isFloat(V)
  rule kLt(V:Val, B:Bool)    => kLt(V, boolAsInt(B)) requires isInt(V) orBool isFloat(V)
  rule kLt(B1:Bool, B2:Bool) => boolAsInt(B1) <Int boolAsInt(B2)

  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
  rule unpairVS(.ValSeq) => .ValSeq
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]

  // ==== non-keyed reverse sorted(), concrete leg (v3) =======================
  // sort.k's condRev(sortVS(VS), true) reverses equal-key runs — invisible on
  // the all-Int / all-str lists sortVS used to accept, visible once sortVS
  // orders mixed numerics (CPython keeps FIRST-seen order among equal keys
  // under reverse=True). rev-in/rev-out over the same stable ascending sortVS
  // is exactly CPython's stable descending sort, and is output-identical on the
  // old homogeneous domains. krun-only (priority 40; proofs keep sort.k's
  // condRev(sortVS(VS), RB) term unchanged).
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", true), .Vals))
        => #alloc(list(revVS(sortVS(revVS(VS))))) ... </k>
       [priority(40)]

  // ==== numeric cross-type membership (Python: 1 == True == 1.0) =============
  // `x in list` / `x not in list` compare elements with ==K in list.k, which does
  // NOT collapse across the numeric types (true =/=K 1, 1 =/=K 1.0). Under krun,
  // override the membership fold with a numeric-aware equality so `in` and
  // unique()-style dedup behave like CPython for mixed int/bool/float elements.
  // (set.k needs no change: setV holds int char codes, compared with ==Int, so a
  // cross-type ==K collapse never arises there.)
  // krun-only (priority 40 beats list.k's default rules); kprove uses the
  // structural ==K rules in list.k unchanged.
  syntax Bool ::= numOrKEq(Val, Val) [function]
  rule numOrKEq(A:Val, B:Val) => applyCmp("==", A, B)
       requires (isInt(A) orBool isBool(A) orBool isFloat(A))
        andBool (isInt(B) orBool isBool(B) orBool isFloat(B))
  rule numOrKEq(A:Val, B:Val) => A ==K B [owise]

  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires numOrKEq(E, V) [priority(40)]
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool numOrKEq(E, V) [priority(40)]
endmodule
