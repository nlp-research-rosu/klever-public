// verification.k — move_one_ball proof scaffolding + summaries, on the UNIFIED semantics.
// solution.py is a cyclic-descent count (the canonical builds sorted(arr) + a rotation and
// compares — sort not modelled; see ./PROOF.md). An array is sortable by right-shifts iff
// its cyclic-descent count (internal descents + the wrap last>first) is <= 1. Symbolic input
// is `list(VS:ValSeq)`; the summaries fold VS, comparing elements via projectIntTotal.

requires "../../reference/src/lemmas.k"

module MOVE-ONE-BALL-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL   // #if _ #then _ #else _ #fi in the entry postcondition

  // proof-only: let a Val sit in expression position.
  syntax Expr ::= Val

  // ---- summary functions = the spec (differential-tested vs CPython: 0/200k) ----------
  //
  // descCount(VS, IDX, PREV, D) = #internal descents after folding VS from index IDX,
  // previous element PREV (a raw Val), running count D. Branch-splits on
  // (IDX>=1 andBool x<prev) — exactly the body's `if i>=1: if x<prev: descents+=1`.
  // [total]: exhaustive; lands in the scope map.
  syntax Int ::= descCount(ValSeq, Int, Val, Int) [function, total]
  rule descCount(.ValSeq, _:Int, _:Val, D:Int) => D [simplification]
  rule descCount(vCons(X:Val, CS:ValSeq), IDX:Int, PREV:Val, D:Int)
    => descCount(CS, IDX +Int 1, X, D +Int 1)
    requires IDX >=Int 1 andBool projectIntTotal(X) <Int projectIntTotal(PREV)  [simplification]
  rule descCount(vCons(X:Val, CS:ValSeq), IDX:Int, PREV:Val, D:Int)
    => descCount(CS, IDX +Int 1, X, D)
    requires notBool (IDX >=Int 1 andBool projectIntTotal(X) <Int projectIntTotal(PREV)) [simplification]

  // firstFold(VS, IDX, F) = arr[0] (captured when i==0), threaded as F otherwise.
  // Mirrors `if i==0: first = x`. F is a raw Val.
  syntax Val ::= firstFold(ValSeq, Int, Val) [function, total]
  rule firstFold(.ValSeq, _:Int, F:Val) => F [simplification]
  rule firstFold(vCons(X:Val, CS:ValSeq), IDX:Int, _F:Val)
    => firstFold(CS, IDX +Int 1, X) requires IDX ==Int 0  [simplification]
  rule firstFold(vCons(_X:Val, CS:ValSeq), IDX:Int, F:Val)
    => firstFold(CS, IDX +Int 1, F) requires IDX =/=Int 0 [simplification]

  // prev accumulator: last element of VS (or PV if empty).
  syntax Val ::= lastOfV(ValSeq, Val) [function, total]
  rule lastOfV(.ValSeq, PV:Val)               => PV [simplification]
  rule lastOfV(vCons(V:Val, S:ValSeq), _:Val) => lastOfV(S, V) [simplification]

  // knownIntM(V): "V casts to an int" incl. the opaque summaries (the P90 kit);
  // BOTH refutation forms — falsity legs (substituted branches) and ML equation
  // killers (kept-equation branches) — plus clauses for the two summaries
  syntax Bool ::= knownIntM(Val) [function]
  rule knownIntM(V:Val) => true requires isInt(V) [simplification]
  rule knownIntM(lastOfV(VS:ValSeq, PV:Val)) => true
    requires allInt(VS) andBool knownIntM(PV) [simplification]
  rule knownIntM(firstFold(VS:ValSeq, _:Int, F:Val)) => true
    requires allInt(VS) andBool knownIntM(F) [simplification]
  rule knownIntM(ref(_:Int))     => false [simplification]
  rule knownIntM(cellRef(_:Int)) => false [simplification]
  rule { V:Val #Equals ref(_:Int) }     => #Bottom requires knownIntM(V) [simplification]
  rule { ref(_:Int) #Equals V:Val }     => #Bottom requires knownIntM(V) [simplification]
  rule { V:Val #Equals cellRef(_:Int) } => #Bottom requires knownIntM(V) [simplification]
  rule { cellRef(_:Int) #Equals V:Val } => #Bottom requires knownIntM(V) [simplification]
  rule applyCmp("<", V:Val, W:Val) => projectIntTotal(V) <Int projectIntTotal(W)
    requires knownIntM(V) andBool knownIntM(W) [simplification]

  // The post-loop wrap compare `prev > first` runs on the folded Val accumulators
  // lastOfV(VS,0) and firstFold(VS,0,0). Both are ints under allInt, but the reference's
  // operator cast bridge (applyCmp(OP,V,W) requires isInt(V) andBool isInt(W)) can't fire:
  // kore can't decide isInt of an opaque summary term. Echo the cast for exactly these two
  // operands via projectIntTotal (their int value). Guarded by allInt/isInt so it is a true
  // statement; problem-local (kept here, not in shared lemmas).
  rule applyCmp(OP:String, lastOfV(VS:ValSeq, P:Val), firstFold(WS:ValSeq, IDX:Int, F:Val))
    => applyCmp(OP, projectIntTotal(lastOfV(VS, P)), projectIntTotal(firstFold(WS, IDX, F)))
    requires allInt(VS) andBool isInt(P) andBool allInt(WS) andBool isInt(F)  [simplification]
endmodule
