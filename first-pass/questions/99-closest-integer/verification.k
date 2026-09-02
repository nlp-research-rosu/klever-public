// verification.k — closest_integer on the UNIFIED semantics, TRAP-FREE (P99).
// solution.py is canonical verbatim (docstring dropped): real import-bound
// floor/ceil, real str.count / while trailing-zero strip / [:-1] and [-2:]
// slices / float() / round(). The result is the STRUCTURAL float-rung model
// ciModel(CS): a declare-then-guard composition of the shared opaque float
// atoms (decStrToF/ceilF/floorFI/roundF) over the stripped code-seq.
// The old closest_integer_core Call trap and the closestInt decision fold
// are GONE (closestInt survives only in PROOF.md as the decimal reading).

requires "../../reference/src/lemmas.k"

module CLOSEST-INT-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // num > 0 rides the SHARED mixed Float/Int k-cell compare (lemmas/float.k);
  // round/floor/ceil/int dispatch through the SHARED simplification echoes
  // (lemmas/float.k, lemmas/builtins.k); len(value) > 0 through the shared
  // k-cell Int-compare lemmas (lemmas/core.k)

  // ---- ==K structure lemmas: str == reduces to IntSeq ==K, which never
  // auto-decomposes on cons forms --------------------------------------------
  rule iCons(A:Int, As:IntSeq) ==K iCons(B:Int, Bs:IntSeq)
    => A ==Int B andBool As ==K Bs [simplification]
  rule iCons(_:Int, _:IntSeq) ==K .IntSeq => false [simplification]
  rule .IntSeq ==K iCons(_:Int, _:IntSeq) => false [simplification]

  // ---- domain vocabulary ----------------------------------------------------
  // (signOf/bodyOf/intDigits/fracDigits/magOf: the decimal-numeral reading,
  // kept as the requires-guard vocabulary — codes '-'=45 '.'=46 '0'=48 '5'=53)
  syntax Int ::= signOf(IntSeq) [function, total]
  rule signOf(iCons(C:Int, _)) => -1 requires C ==Int 45
  rule signOf(iCons(C:Int, _)) =>  1 requires C =/=Int 45
  rule signOf(.IntSeq)         =>  1
  syntax IntSeq ::= bodyOf(IntSeq) [function, total]
  rule bodyOf(iCons(C:Int, T:IntSeq)) => T  requires C ==Int 45
  rule bodyOf(iCons(C:Int, T:IntSeq)) => iCons(C, T) requires C =/=Int 45
  rule bodyOf(.IntSeq)                => .IntSeq
  syntax IntSeq ::= intDigits(IntSeq) [function, total]
  rule intDigits(.IntSeq)                => .IntSeq
  rule intDigits(iCons(C:Int, _))        => .IntSeq                requires C ==Int 46
  rule intDigits(iCons(C:Int, T:IntSeq)) => iCons(C, intDigits(T)) requires C =/=Int 46
  syntax IntSeq ::= fracDigits(IntSeq) [function, total]
  rule fracDigits(.IntSeq)                => .IntSeq
  rule fracDigits(iCons(C:Int, T:IntSeq)) => T             requires C ==Int 46
  rule fracDigits(iCons(C:Int, T:IntSeq)) => fracDigits(T) requires C =/=Int 46
  syntax Int ::= digitsToInt(IntSeq, Int) [function, total]
  rule digitsToInt(.IntSeq, A:Int)                => A
  rule digitsToInt(iCons(C:Int, T:IntSeq), A:Int) => digitsToInt(T, (A *Int 10) +Int (C -Int 48))
  syntax Int ::= magOf(IntSeq) [function, total]
  rule magOf(D:IntSeq) => digitsToInt(D, 0)

  // ---- the while-strip machinery -------------------------------------------
  syntax IntSeq ::= dropLastIS(IntSeq) [function, total]
  rule dropLastIS(.IntSeq)                     => .IntSeq
  rule dropLastIS(iCons(_:Int, .IntSeq))       => .IntSeq
  rule dropLastIS(iCons(C:Int, iCons(D:Int, T:IntSeq)))
    => iCons(C, dropLastIS(iCons(D, T)))
  // the [:-1] slice term IS drop-last: the clamp reduces under the nonempty
  // witness, and the shared forward reshape leaves takeIS(CS, isLen(CS)-1)
  rule clampLo(isLen(CS:IntSeq) +Int -1, 1) => isLen(CS) +Int -1
    requires hasNonZ(CS) [simplification]
  rule takeIS(CS:IntSeq, isLen(CS) +Int -1) => dropLastIS(CS) [simplification]

  // the while summary: strip trailing '0' codes, one per transition, guards in
  // the execution's atom form
  syntax IntSeq ::= stripZ(IntSeq) [function, total]
  rule stripZ(CS:IntSeq) => stripZ(dropLastIS(CS))
    requires intSeqAt(CS, isLen(CS) +Int -1) ==Int 48 [simplification]
  rule stripZ(CS:IntSeq) => CS
    requires notBool (intSeqAt(CS, isLen(CS) +Int -1) ==Int 48) [simplification]

  // ---- hasNonZ: the strip terminates inside the string ----------------------
  syntax Bool ::= hasNonZ(IntSeq) [function, total]
  rule hasNonZ(.IntSeq)                => false
  rule hasNonZ(iCons(C:Int, R:IntSeq)) => C =/=Int 48 orBool hasNonZ(R)
  // a dotted numeral has a non-'0' char (the dot)
  rule hasNonZ(CS:IntSeq) => true
    requires cntSub(CS, iCons(46, .IntSeq)) ==Int 1 [simplification]
  // dropping a trailing '0' keeps the witness
  rule hasNonZ(dropLastIS(CS:IntSeq)) => true
    requires hasNonZ(CS) andBool intSeqAt(CS, isLen(CS) +Int -1) ==Int 48 [simplification]
  // the strip keeps the witness
  rule hasNonZ(stripZ(CS:IntSeq)) => true
    requires hasNonZ(CS) [simplification]
  // a witness makes the seq nonempty (both atom spellings the clamps produce)
  rule isLen(CS:IntSeq) +Int -1 <Int 0  => false requires hasNonZ(CS) [simplification]
  rule isLen(CS:IntSeq) +Int -1 >=Int 0 => true  requires hasNonZ(CS) [simplification]
  rule 0 <Int isLen(CS:IntSeq) => true requires hasNonZ(CS) [simplification]
  rule isLen(CS:IntSeq) ==Int 0 => false requires hasNonZ(CS) [simplification]

  // ---- the possibly-stripped value ------------------------------------------
  syntax IntSeq ::= sval(IntSeq) [function, total]
  rule sval(CS:IntSeq) => stripZ(CS)
    requires cntSub(CS, iCons(46, .IntSeq)) ==Int 1 [simplification]
  rule sval(CS:IntSeq) => CS
    requires notBool (cntSub(CS, iCons(46, .IntSeq)) ==Int 1) [simplification]

  // ---- the result model: the real code's opaque-float composition ----------
  // The '.5' test atom stays OPAQUE-WHOLE in the path condition (clampLo's
  // guards never feasibility-split during function evaluation), so the arms
  // guard on that ==K atom VERBATIM (dot5A), not on its decomposed meaning.
  syntax Bool ::= dot5A(IntSeq) [function, total]
  rule dot5A(S:IntSeq)
    => buildIS(S, clampLo(isLen(S) +Int -2, 1), isLen(S), 1) ==K iCons(46, iCons(53, .IntSeq))

  syntax Int ::= ciModel(IntSeq) [function, total]
  rule ciModel(CS:IntSeq) => ceilF(decStrToF(sval(CS)))
    requires dot5A(sval(CS)) andBool gtF(decStrToF(sval(CS)), 0.0) [simplification]
  rule ciModel(CS:IntSeq) => floorFI(decStrToF(sval(CS)))
    requires dot5A(sval(CS)) andBool notBool gtF(decStrToF(sval(CS)), 0.0) [simplification]
  rule ciModel(CS:IntSeq) => roundF(decStrToF(sval(CS)))
    requires notBool dot5A(sval(CS)) andBool isLen(sval(CS)) >Int 0 [simplification]
  rule ciModel(CS:IntSeq) => 0
    requires notBool dot5A(sval(CS)) andBool notBool (isLen(sval(CS)) >Int 0) [simplification]
endmodule
