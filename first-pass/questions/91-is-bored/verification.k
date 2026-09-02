// verification.k — is_bored on the UNIFIED semantics. is_bored is a single left-to-right
// 4-state scan counting sentences that start with "I " (delimited by .?!). solution.py writes it
// as a PURE if/elif chain with no char temporaries (diff-tested 0/25461), so each iteration is one
// atomic dispatch over ord(S[i]) comparisons — case-splittable intSeqAt atoms (the 132-is-nested
// nstate/nestFold rung).
//
// TRAP-FREE (P91): canonical 1-fn shape; the FuncDef executes in the entry claim
// (a single call — the while folds via the while-invariant claim inside the callee frame), and
// boredFold below is a DEFINED total transition system mirroring the elif chain. Nothing is
// trusted beyond the shared semantics.

requires "../../reference/src/lemmas.k"

module IS-BORED-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // ---- atI: TOTAL element accessor + in-bounds bridge from the semantics' partial intSeqAt
  // (the #10 make_palindrome idiom) — without it the per-char #branch leaves an undischargeable
  // #Ceil(intSeqAt(CS, I)) undefined-branch.
  // (atI + the intSeqAt bounds bridge are SHARED: lemmas/subscript.k)

  // the 3-scalar loop state: count, phase (0 start / 1 second-char / 2 body / 3 ws-run), cand
  // (0 no / 1 saw 'I' / 2 matched "I ").
  syntax BState ::= bstate(Int, Int, Int)

  // boredFold(CS, I, N, S): fold the scan from I to N. One rule per elif-chain leaf; guards are
  // linear atoms over atI(CS, I) (WS = 9..13 or 28..32; DELIM = 46, 63, 33), phase, cand.
  syntax BState ::= boredFold(IntSeq, Int, Int, BState) [function, total]
  rule boredFold(_CS:IntSeq, I:Int, N:Int, S:BState) => S
    requires notBool (I <Int N)
    [simplification]
  // phase 3, ws-or-delim char: skip (phase reassigned 3, cand kept)
  rule boredFold(CS:IntSeq, I:Int, N:Int, bstate(CT:Int, PH:Int, CD:Int))
    => boredFold(CS, I +Int 1, N, bstate(CT, 3, CD))
    requires I <Int N andBool PH ==Int 3
     andBool (atI(CS, I) ==Int 46 orBool atI(CS, I) ==Int 63 orBool atI(CS, I) ==Int 33
              orBool (9 <=Int atI(CS, I) andBool atI(CS, I) <=Int 13)
              orBool (28 <=Int atI(CS, I) andBool atI(CS, I) <=Int 32))
    [simplification]
  // delimiter outside a ws-run: count the matched fragment, reset, enter the ws-run
  rule boredFold(CS:IntSeq, I:Int, N:Int, bstate(CT:Int, PH:Int, CD:Int))
    => boredFold(CS, I +Int 1, N, bstate(CT +Int 1, 3, 0))
    requires I <Int N andBool notBool (PH ==Int 3)
     andBool (atI(CS, I) ==Int 46 orBool atI(CS, I) ==Int 63 orBool atI(CS, I) ==Int 33)
     andBool CD ==Int 2
    [simplification]
  rule boredFold(CS:IntSeq, I:Int, N:Int, bstate(CT:Int, PH:Int, CD:Int))
    => boredFold(CS, I +Int 1, N, bstate(CT, 3, 0))
    requires I <Int N andBool notBool (PH ==Int 3)
     andBool (atI(CS, I) ==Int 46 orBool atI(CS, I) ==Int 63 orBool atI(CS, I) ==Int 33)
     andBool notBool (CD ==Int 2)
    [simplification]
  // fragment start (fresh, or leaving a ws-run on a non-ws non-delim char): capture a leading 'I'.
  // The PH==3 arm MUST exclude ws (else it overlaps the skip rule above: a ws char != 'I' entails
  // both guards and the function gets two contradictory equations).
  rule boredFold(CS:IntSeq, I:Int, N:Int, bstate(CT:Int, PH:Int, _CD:Int))
    => boredFold(CS, I +Int 1, N, bstate(CT, 1, 1))
    requires I <Int N
     andBool notBool (atI(CS, I) ==Int 46 orBool atI(CS, I) ==Int 63 orBool atI(CS, I) ==Int 33)
     andBool (PH ==Int 0 orBool (PH ==Int 3
              andBool notBool ((9 <=Int atI(CS, I) andBool atI(CS, I) <=Int 13)
                       orBool (28 <=Int atI(CS, I) andBool atI(CS, I) <=Int 32))))
     andBool atI(CS, I) ==Int 73
    [simplification]
  rule boredFold(CS:IntSeq, I:Int, N:Int, bstate(CT:Int, PH:Int, _CD:Int))
    => boredFold(CS, I +Int 1, N, bstate(CT, 1, 0))
    requires I <Int N
     andBool notBool (atI(CS, I) ==Int 46 orBool atI(CS, I) ==Int 63 orBool atI(CS, I) ==Int 33)
     andBool (PH ==Int 0 orBool (PH ==Int 3
              andBool notBool ((9 <=Int atI(CS, I) andBool atI(CS, I) <=Int 13)
                       orBool (28 <=Int atI(CS, I) andBool atI(CS, I) <=Int 32))))
     andBool notBool (atI(CS, I) ==Int 73)
    [simplification]
  // second char of a fragment: "I " completes iff cand==1 and the char is a space
  rule boredFold(CS:IntSeq, I:Int, N:Int, bstate(CT:Int, PH:Int, CD:Int))
    => boredFold(CS, I +Int 1, N, bstate(CT, 2, 2))
    requires I <Int N
     andBool notBool (atI(CS, I) ==Int 46 orBool atI(CS, I) ==Int 63 orBool atI(CS, I) ==Int 33)
     andBool PH ==Int 1
     andBool CD ==Int 1 andBool atI(CS, I) ==Int 32
    [simplification]
  rule boredFold(CS:IntSeq, I:Int, N:Int, bstate(CT:Int, PH:Int, CD:Int))
    => boredFold(CS, I +Int 1, N, bstate(CT, 2, 0))
    requires I <Int N
     andBool notBool (atI(CS, I) ==Int 46 orBool atI(CS, I) ==Int 63 orBool atI(CS, I) ==Int 33)
     andBool PH ==Int 1
     andBool notBool (CD ==Int 1 andBool atI(CS, I) ==Int 32)
    [simplification]
  // fragment body (phase 2, or any other phase value): nothing changes
  rule boredFold(CS:IntSeq, I:Int, N:Int, bstate(CT:Int, PH:Int, CD:Int))
    => boredFold(CS, I +Int 1, N, bstate(CT, PH, CD))
    requires I <Int N
     andBool notBool (atI(CS, I) ==Int 46 orBool atI(CS, I) ==Int 63 orBool atI(CS, I) ==Int 33)
     andBool notBool (PH ==Int 3) andBool notBool (PH ==Int 0) andBool notBool (PH ==Int 1)
    [simplification]

  // projections (the loop invariant threads the 3 scalars as separate store slots).
  syntax Int ::= bCt(BState) [function, total] | bPh(BState) [function, total]
               | bCd(BState) [function, total]
  rule bCt(bstate(CT:Int, _, _)) => CT
  rule bPh(bstate(_, PH:Int, _)) => PH
  rule bCd(bstate(_, _, CD:Int)) => CD

  // the final scan state and the result (the post-loop `if cand == 2: count += 1`).
  syntax BState ::= boredState(IntSeq) [function, total]
  rule boredState(CS:IntSeq) => boredFold(CS, 0, isLen(CS), bstate(0, 0, 0)) [simplification]

  syntax Int ::= boredRes(IntSeq) [function]
  rule boredRes(CS:IntSeq)
    => bCt(boredState(CS)) +Int #if bCd(boredState(CS)) ==Int 2 #then 1 #else 0 #fi
    [simplification]
endmodule
