// verification.k — bf on the UNIFIED semantics, INTERCEPTION-FREE (P148,
// purged). solution.py is canonical verbatim; the proof runs the REAL tuple
// machinery end to end: #memberAcc unrolls over the concrete 8-planet tuple
// (str-injective ==K leaf atoms), idxOfVS and the slices reduce CONCRETELY
// on every in-branch (the membership atoms entail idxOfVS's own guards).
// No k-cell rules here.

requires "../../reference/src/lemmas.k"

module BF-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // `planet in planet_names` inside the BoolOp("or", ...) short-circuit is heated as an OPERAND,
  // so the Compare falls through operators.k's [owise] to applyCmp("in"/"not in", str, tuple) —
  // for which the only rules are str-vs-str (substring); it sticks. Echo it to the SAME memberVS
  // the top-level Compare => #memberAcc route (lemmas/list.k) produces, so both paths converge.
  rule applyCmp("in", V:Val, tuple(VS:ValSeq)) => memberVS(V, VS) [simplification]
  rule applyCmp("not in", V:Val, tuple(VS:ValSeq)) => notBool memberVS(V, VS) [simplification]

  // idxOfVS (tuple.index) is PARTIAL, so idxOfVS(A) <Int idxOfVS(B) carries partial fns and the If's
  // #branch cannot lift it — a neither-true-nor-false ghost survives (the P146 wall). Give it a TOTAL
  // twin (fallthrough returns the running offset; only reached for a non-member, which membership
  // rules out) and bridge every occurrence, so the index-compare atom lifts. atI-total-accessor idiom.
  syntax Int ::= tIdxOfVS(ValSeq, Val, Int) [function, total]
  rule tIdxOfVS(.ValSeq, _:Val, I:Int) => I [simplification]
  rule tIdxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V [simplification]
  rule tIdxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => tIdxOfVS(R, V, I +Int 1)
    requires notBool (A ==K V) [simplification]
  rule idxOfVS(VS:ValSeq, V:Val, I:Int) => tIdxOfVS(VS, V, I) [simplification]

  // the slice pl8[idxX+1 : idxY] wraps its bounds in slAdjust/clampHi index normalization, which
  // stays stuck on the opaque tIdxOfVS index (its bounds aren't SMT-visible). For a member the
  // index is in [0, len), so idx and idx+1 are within [0, len] and the clamp is the identity —
  // reduce it directly under membership so the executed slice matches the model's raw-index form.
  rule slAdjust(tIdxOfVS(VS:ValSeq, X:Val, 0) +Int 1, LEN:Int, 1) => tIdxOfVS(VS, X, 0) +Int 1
    requires memberVS(X, VS) andBool vsLen(VS) ==Int LEN [simplification]
  rule slAdjust(tIdxOfVS(VS:ValSeq, X:Val, 0), LEN:Int, 1) => tIdxOfVS(VS, X, 0)
    requires memberVS(X, VS) andBool vsLen(VS) ==Int LEN [simplification]

  // buildVS (the slice builder) is PARTIAL through valSeqAt, so #Ceil(buildVS(..)) sticks the
  // implication on the distinct-planets slice arm. The slice is pl8[idxX+1 : idxY]; both members
  // (memberVS) so both indices are in [0, len), the step-1 walk only reads in-bounds, defined.
  rule #Ceil(buildVS(VS:ValSeq, tIdxOfVS(VS, X:Val, 0) +Int 1, tIdxOfVS(VS, Y:Val, 0), 1)) => #Top
    requires memberVS(X, VS) andBool memberVS(Y, VS) [simplification]

  // the concrete planet tuple and the membership disjunction (the real
  // #memberAcc leaf atoms after str-injectivity, concrete codes LEFT)
  syntax ValSeq ::= "pl8" [function, total]
  rule pl8 => vCons(str(iCons(77, iCons(101, iCons(114, iCons(99, iCons(117, iCons(114, iCons(121, .IntSeq)))))))), vCons(str(iCons(86, iCons(101, iCons(110, iCons(117, iCons(115, .IntSeq)))))), vCons(str(iCons(69, iCons(97, iCons(114, iCons(116, iCons(104, .IntSeq)))))), vCons(str(iCons(77, iCons(97, iCons(114, iCons(115, .IntSeq))))), vCons(str(iCons(74, iCons(117, iCons(112, iCons(105, iCons(116, iCons(101, iCons(114, .IntSeq)))))))), vCons(str(iCons(83, iCons(97, iCons(116, iCons(117, iCons(114, iCons(110, .IntSeq))))))), vCons(str(iCons(85, iCons(114, iCons(97, iCons(110, iCons(117, iCons(115, .IntSeq))))))), vCons(str(iCons(78, iCons(101, iCons(112, iCons(116, iCons(117, iCons(110, iCons(101, .IntSeq)))))))), .ValSeq))))))))
  // membership over the concrete tuple as the executed memberVS atom (str-injective ==K leaves,
  // over pl8 which unfolds to the same concrete ValSeq the TupleExpr produces)
  syntax Bool ::= pIn8(IntSeq) [function, total]
  rule pIn8(P:IntSeq) => memberVS(str(P), pl8) [simplification]

  // ---- the result model, arms = the executed atoms verbatim ----------------
  syntax Val ::= bfRes(Val, Val) [function, total]
  rule bfRes(str(A:IntSeq), _:Val) => tuple(.ValSeq)
    requires notBool memberVS(str(A), pl8) [simplification]
  rule bfRes(str(A:IntSeq), str(B:IntSeq)) => tuple(.ValSeq)
    requires memberVS(str(A), pl8) andBool notBool memberVS(str(B), pl8) [simplification]
  rule bfRes(str(A:IntSeq), str(B:IntSeq)) => tuple(.ValSeq)
    requires memberVS(str(A), pl8) andBool memberVS(str(B), pl8) andBool A ==K B [simplification]
  rule bfRes(str(A:IntSeq), str(B:IntSeq))
    => tuple(buildVS(pl8, idxOfVS(pl8, str(A), 0) +Int 1, idxOfVS(pl8, str(B), 0), 1))
    requires memberVS(str(A), pl8) andBool memberVS(str(B), pl8) andBool notBool (A ==K B)
     andBool idxOfVS(pl8, str(A), 0) <Int idxOfVS(pl8, str(B), 0) [simplification]
  rule bfRes(str(A:IntSeq), str(B:IntSeq))
    => tuple(buildVS(pl8, idxOfVS(pl8, str(B), 0) +Int 1, idxOfVS(pl8, str(A), 0), 1))
    requires memberVS(str(A), pl8) andBool memberVS(str(B), pl8) andBool notBool (A ==K B)
     andBool notBool (idxOfVS(pl8, str(A), 0) <Int idxOfVS(pl8, str(B), 0)) [simplification]
endmodule
