// verification.k — summary for the fix_spaces proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module FIX-SPACES-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // ---- summary functions = the spec (differential-tested vs CPython: 0/50k) ----
  // Two accumulators: result and the space run-length rl.  Codes: ' '=32, NUL=0, '-'=45,
  // '_'=95.  Per char C: space increments rl; the NUL sentinel applies the TRAILING flush
  // (rl>2 -> "-", rl in {1,2} -> single "_") and resets rl; any other char applies the
  // IN-LOOP flush (rl>2 -> "-", rl==2 -> "__", rl==1 -> "_") then appends C and resets rl.
  // All branches on the FREE rl / input char; both [total] (scope-map values, ../NOTES.md).

  // rl: only spaces increment it; every non-space (incl. the sentinel) resets it.
  syntax Int ::= fixRl(IntSeq, Int) [function, total]
  rule fixRl(.IntSeq, RL:Int) => RL [simplification]
  rule fixRl(iCons(C:Int, S:IntSeq), RL:Int) => fixRl(S, RL +Int 1) requires C ==Int 32 [simplification]
  rule fixRl(iCons(C:Int, S:IntSeq), RL:Int) => fixRl(S, 0)         requires C =/=Int 32 [simplification]

  syntax IntSeq ::= fixRes(IntSeq, IntSeq, Int) [function, total]
  rule fixRes(.IntSeq, RESULT:IntSeq, _RL:Int) => RESULT [simplification]
  // space: result unchanged, rl+1.
  rule fixRes(iCons(C:Int, S:IntSeq), RESULT:IntSeq, RL:Int) => fixRes(S, RESULT, RL +Int 1)
    requires C ==Int 32 [simplification]
  // sentinel NUL: trailing flush, rl:=0.
  rule fixRes(iCons(C:Int, S:IntSeq), RESULT:IntSeq, RL:Int) => fixRes(S, seqConcat(RESULT, iCons(45, .IntSeq)), 0)
    requires C ==Int 0 andBool RL >Int 2 [simplification]
  rule fixRes(iCons(C:Int, S:IntSeq), RESULT:IntSeq, RL:Int) => fixRes(S, seqConcat(RESULT, iCons(95, .IntSeq)), 0)
    requires C ==Int 0 andBool RL >Int 0 andBool notBool (RL >Int 2) [simplification]
  rule fixRes(iCons(C:Int, S:IntSeq), RESULT:IntSeq, RL:Int) => fixRes(S, RESULT, 0)
    requires C ==Int 0 andBool notBool (RL >Int 0) [simplification]
  // other char: in-loop flush, append C, rl:=0.
  rule fixRes(iCons(C:Int, S:IntSeq), RESULT:IntSeq, RL:Int)
    => fixRes(S, seqConcat(seqConcat(RESULT, iCons(45, .IntSeq)), iCons(C, .IntSeq)), 0)
    requires C =/=Int 32 andBool C =/=Int 0 andBool RL >Int 2 [simplification]
  rule fixRes(iCons(C:Int, S:IntSeq), RESULT:IntSeq, RL:Int)
    => fixRes(S, seqConcat(seqConcat(RESULT, iCons(95, iCons(95, .IntSeq))), iCons(C, .IntSeq)), 0)
    requires C =/=Int 32 andBool C =/=Int 0 andBool RL ==Int 2 [simplification]
  rule fixRes(iCons(C:Int, S:IntSeq), RESULT:IntSeq, RL:Int)
    => fixRes(S, seqConcat(seqConcat(RESULT, iCons(95, .IntSeq)), iCons(C, .IntSeq)), 0)
    requires C =/=Int 32 andBool C =/=Int 0 andBool RL ==Int 1 [simplification]
  rule fixRes(iCons(C:Int, S:IntSeq), RESULT:IntSeq, RL:Int)
    => fixRes(S, seqConcat(RESULT, iCons(C, .IntSeq)), 0)
    requires C =/=Int 32 andBool C =/=Int 0 andBool notBool (RL >Int 2) andBool RL =/=Int 2 andBool RL =/=Int 1 [simplification]
endmodule
