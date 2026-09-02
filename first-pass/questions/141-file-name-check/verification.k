// verification.k — file_name_check on the UNIFIED semantics, TRAP-FREE
// (P141). solution.py is canonical verbatim: real split(sep='.') kwarg call,
// real subscripts, real isalpha/isdigit, real listcomp count. All PC atoms
// PARTIAL-FREE; membership and the digit count follow the P124/P153 kits.

requires "../../reference/src/lemmas.k"

module FILE-NAME-CHECK-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  rule 0 <Int 1 +Int vsLen(_:ValSeq) => true [simplification]

  // ==K structure lemmas
  rule iCons(A:Int, As:IntSeq) ==K iCons(B:Int, Bs:IntSeq)
    => A ==Int B andBool As ==K Bs [simplification]
  rule iCons(_:Int, _:IntSeq) ==K .IntSeq => false [simplification]
  rule .IntSeq ==K iCons(_:Int, _:IntSeq) => false [simplification]

  // ---- total split vocabulary (P144 kit) ------------------------------------
  syntax Int ::= splitCountC(IntSeq, Int) [function, total]
  rule splitCountC(.IntSeq, _:Int)                => 1
  rule splitCountC(iCons(C:Int, T:IntSeq), S:Int) => 1 +Int splitCountC(T, S) requires C ==Int S
  rule splitCountC(iCons(C:Int, T:IntSeq), S:Int) => splitCountC(T, S)        requires C =/=Int S
  syntax IntSeq ::= takeFieldC(IntSeq, Int) [function, total]
  rule takeFieldC(.IntSeq, _:Int)                => .IntSeq
  rule takeFieldC(iCons(C:Int, _), S:Int)        => .IntSeq requires C ==Int S
  rule takeFieldC(iCons(C:Int, T:IntSeq), S:Int) => iCons(C, takeFieldC(T, S)) requires C =/=Int S
  syntax IntSeq ::= fieldSeqC(Int, IntSeq, Int) [function, total]
  rule fieldSeqC(0, CS:IntSeq, S:Int)                  => takeFieldC(CS, S)
  rule fieldSeqC(I:Int, .IntSeq, _:Int)                => .IntSeq requires I >Int 0
  rule fieldSeqC(I:Int, iCons(C:Int, T:IntSeq), S:Int) => fieldSeqC(I -Int 1, T, S) requires I >Int 0 andBool C ==Int S
  rule fieldSeqC(I:Int, iCons(C:Int, T:IntSeq), S:Int) => fieldSeqC(I, T, S)        requires I >Int 0 andBool C =/=Int S

  rule vsLen(splitSep(CS:IntSeq, S:Int, .IntSeq)) => splitCountC(CS, S) [simplification]
  // a 2-field split's subscripts reduce to the total field vocabulary
  // (valSeqAt-headed lemmas — the split value itself stays the real
  // splitSep term; normIdx has already resolved the index)
  rule valSeqAt(splitSep(CS:IntSeq, 46, .IntSeq), 0) => str(fieldSeqC(0, CS, 46))
    requires splitCountC(CS, 46) ==Int 2 [simplification]
  rule valSeqAt(splitSep(CS:IntSeq, 46, .IntSeq), 1) => str(fieldSeqC(1, CS, 46))
    requires splitCountC(CS, 46) ==Int 2 [simplification]

  // ---- entailment-gated compare echoes (the P81 class) ----------------------
  // str == canonicalizes to the inner code-seq equation (str is injective)
  rule str(A:IntSeq) ==K str(B:IntSeq) => A ==K B [simplification]
  // length compares on opaque Int fn terms (isLen / vsLen / splitCountC)
  syntax Bool ::= knownIL(Val) [function, total, no-evaluators]
  rule knownIL(isLen(_:IntSeq))          => true [simplification]
  rule knownIL(vsLen(_:ValSeq))          => true [simplification]
  rule knownIL(splitCountC(_:IntSeq, _:Int)) => true [simplification]
  rule knownIL(str(_:IntSeq))            => false [simplification]
  rule applyCmp("!=", V:Val, N:Int) => notBool (projectIntTotal(V) ==Int N)
    requires knownIL(V) [simplification]
  rule applyCmp("==", V:Val, N:Int) => projectIntTotal(V) ==Int N
    requires knownIL(V) [simplification]
  rule applyCmp(">", V:Val, N:Int) => projectIntTotal(V) >Int N
    requires knownIL(V) [simplification]
  rule projectIntTotal(isLen(CS:IntSeq)) => isLen(CS) [simplification]
  rule projectIntTotal(vsLen(VS:ValSeq)) => vsLen(VS) [simplification]
  rule projectIntTotal(splitCountC(CS:IntSeq, S:Int)) => splitCountC(CS, S) [simplification]

  // suffix membership in the EXECUTED vocabulary: memberVS stays opaque on
  // undecided leaves (the stepwise design), so the branch PC carries the
  // whole application — mem3 must be that exact atom
  syntax Bool ::= mem3(IntSeq) [function, total]
  rule mem3(CS:IntSeq)
    => memberVS(str(fieldSeqC(1, CS, 46)),
         vCons(str(iCons(116, iCons(120, iCons(116, .IntSeq)))),
         vCons(str(iCons(101, iCons(120, iCons(101, .IntSeq)))),
         vCons(str(iCons(100, iCons(108, iCons(108, .IntSeq)))), .ValSeq))))

  // the first char of a symbolic field: total head accessor
  syntax Int ::= head0(IntSeq) [function, total, no-evaluators]
  rule head0(iCons(C:Int, _:IntSeq)) => C [simplification]
  rule intSeqAt(F:IntSeq, 0) => head0(F) [simplification]

  // ---- the digit-filter comp fold (P153 upSeq analog) ------------------------
  syntax ValSeq ::= digSeq(IntSeq, ValSeq) [function, total]
  rule digSeq(.IntSeq, ACC:ValSeq) => ACC [simplification]
  rule digSeq(iCons(C:Int, R:IntSeq), ACC:ValSeq)
    => digSeq(R, valSeqConcat(ACC, vCons(str(iCons(C, .IntSeq)), .ValSeq)))
    requires isDigitC(C) [simplification]
  rule digSeq(iCons(C:Int, R:IntSeq), ACC:ValSeq) => digSeq(R, ACC)
    requires notBool isDigitC(C) [simplification]

  // ---- the result model -------------------------------------------------------
  syntax Val ::= fnRes(IntSeq) [function, total]
  syntax IntSeq ::= f0(IntSeq) [function, total]
  rule f0(CS:IntSeq) => fieldSeqC(0, CS, 46)
  syntax Val ::= f1(IntSeq) [function, total]
  rule f1(CS:IntSeq) => str(fieldSeqC(1, CS, 46))
  syntax Bool ::= alpha0(IntSeq) [function, total]
  // exactly the executed atom: the subscript's singleton iCons is never
  // empty, so only the range test survives
  rule alpha0(CS:IntSeq) => isAlphaC(head0(f0(CS)))

  syntax Val ::= "noV" [function, total]
  rule noV => str(iCons(78, iCons(111, .IntSeq)))
  syntax Val ::= "yesV" [function, total]
  rule yesV => str(iCons(89, iCons(101, iCons(115, .IntSeq))))

  rule fnRes(CS:IntSeq) => noV
    requires notBool (splitCountC(CS, 46) ==Int 2) [simplification]
  rule fnRes(CS:IntSeq) => noV
    requires splitCountC(CS, 46) ==Int 2
     andBool notBool (mem3(CS)) [simplification]
  rule fnRes(CS:IntSeq) => noV
    requires splitCountC(CS, 46) ==Int 2 andBool mem3(CS)
     andBool isLen(f0(CS)) ==Int 0 [simplification]
  rule fnRes(CS:IntSeq) => noV
    requires splitCountC(CS, 46) ==Int 2 andBool mem3(CS)
     andBool notBool (isLen(f0(CS)) ==Int 0) andBool notBool alpha0(CS) [simplification]
  rule fnRes(CS:IntSeq) => noV
    requires splitCountC(CS, 46) ==Int 2 andBool mem3(CS)
     andBool notBool (isLen(f0(CS)) ==Int 0) andBool alpha0(CS)
     andBool vsLen(digSeq(f0(CS), .ValSeq)) >Int 3 [simplification]
  rule fnRes(CS:IntSeq) => yesV
    requires splitCountC(CS, 46) ==Int 2 andBool mem3(CS)
     andBool notBool (isLen(f0(CS)) ==Int 0) andBool alpha0(CS)
     andBool notBool (vsLen(digSeq(f0(CS), .ValSeq)) >Int 3) [simplification]
endmodule
