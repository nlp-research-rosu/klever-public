// verification.k — summary for the decode_cyclic proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module DECODE-CYCLIC-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  // proof-only: let a Val sit in expression position (so str(CS) can be a Call arg).
  syntax Expr ::= Val

  // ---- summary functions = the spec (differential-tested vs CPython: 0/50k) ----
  // FIVE accumulators threaded over CS: result, c0, c1 (the first two chars of the current
  // group), buf (the raw partial group), count.  Four branch-split cases per char C, all on
  // the FREE count (kprove-splittable):
  //   COUNT==0 : c0:=C ; buf+=C ; count:=1
  //   COUNT==1 : c1:=C ; buf+=C ; count:=2
  //   COUNT==2 : EMIT result += C c0 c1 ; buf:="" ; count:=0   (the third char closes a group)
  //   else     : buf+=C ; count:=COUNT+1                       (unreachable; kept for totality)
  // All [total] (scope-map values, ../NOTES.md).

  // count cycles 0->1->2->0 ...
  syntax Int ::= decCount(IntSeq, Int) [function, total]
  rule decCount(.IntSeq, COUNT:Int) => COUNT [simplification]
  rule decCount(iCons(_:Int, S:IntSeq), COUNT:Int) => decCount(S, 1)         requires COUNT ==Int 0 [simplification]
  rule decCount(iCons(_:Int, S:IntSeq), COUNT:Int) => decCount(S, 2)         requires COUNT ==Int 1 [simplification]
  rule decCount(iCons(_:Int, S:IntSeq), COUNT:Int) => decCount(S, 0)         requires COUNT ==Int 2 [simplification]
  rule decCount(iCons(_:Int, S:IntSeq), COUNT:Int) => decCount(S, COUNT +Int 1)
    requires COUNT =/=Int 0 andBool COUNT =/=Int 1 andBool COUNT =/=Int 2 [simplification]

  // c0 = first char of the current group (set when count==0).
  syntax IntSeq ::= decC0(IntSeq, IntSeq, Int) [function, total]
  rule decC0(.IntSeq, C0:IntSeq, _COUNT:Int) => C0 [simplification]
  rule decC0(iCons(C:Int, S:IntSeq), _C0:IntSeq, COUNT:Int) => decC0(S, iCons(C, .IntSeq), 1) requires COUNT ==Int 0 [simplification]
  rule decC0(iCons(_:Int, S:IntSeq), C0:IntSeq, COUNT:Int) => decC0(S, C0, 2)                 requires COUNT ==Int 1 [simplification]
  rule decC0(iCons(_:Int, S:IntSeq), C0:IntSeq, COUNT:Int) => decC0(S, C0, 0)                 requires COUNT ==Int 2 [simplification]
  rule decC0(iCons(_:Int, S:IntSeq), C0:IntSeq, COUNT:Int) => decC0(S, C0, COUNT +Int 1)
    requires COUNT =/=Int 0 andBool COUNT =/=Int 1 andBool COUNT =/=Int 2 [simplification]

  // c1 = second char of the current group (set when count==1).
  syntax IntSeq ::= decC1(IntSeq, IntSeq, Int) [function, total]
  rule decC1(.IntSeq, C1:IntSeq, _COUNT:Int) => C1 [simplification]
  rule decC1(iCons(_:Int, S:IntSeq), C1:IntSeq, COUNT:Int) => decC1(S, C1, 1)                 requires COUNT ==Int 0 [simplification]
  rule decC1(iCons(C:Int, S:IntSeq), _C1:IntSeq, COUNT:Int) => decC1(S, iCons(C, .IntSeq), 2) requires COUNT ==Int 1 [simplification]
  rule decC1(iCons(_:Int, S:IntSeq), C1:IntSeq, COUNT:Int) => decC1(S, C1, 0)                 requires COUNT ==Int 2 [simplification]
  rule decC1(iCons(_:Int, S:IntSeq), C1:IntSeq, COUNT:Int) => decC1(S, C1, COUNT +Int 1)
    requires COUNT =/=Int 0 andBool COUNT =/=Int 1 andBool COUNT =/=Int 2 [simplification]

  // buf = raw chars of the current group (reset on emit); appended unchanged after the loop.
  syntax IntSeq ::= decBuf(IntSeq, IntSeq, Int) [function, total]
  rule decBuf(.IntSeq, BUF:IntSeq, _COUNT:Int) => BUF [simplification]
  rule decBuf(iCons(C:Int, S:IntSeq), BUF:IntSeq, COUNT:Int) => decBuf(S, seqConcat(BUF, iCons(C, .IntSeq)), 1) requires COUNT ==Int 0 [simplification]
  rule decBuf(iCons(C:Int, S:IntSeq), BUF:IntSeq, COUNT:Int) => decBuf(S, seqConcat(BUF, iCons(C, .IntSeq)), 2) requires COUNT ==Int 1 [simplification]
  rule decBuf(iCons(_:Int, S:IntSeq), _BUF:IntSeq, COUNT:Int) => decBuf(S, .IntSeq, 0)                          requires COUNT ==Int 2 [simplification]
  rule decBuf(iCons(C:Int, S:IntSeq), BUF:IntSeq, COUNT:Int) => decBuf(S, seqConcat(BUF, iCons(C, .IntSeq)), COUNT +Int 1)
    requires COUNT =/=Int 0 andBool COUNT =/=Int 1 andBool COUNT =/=Int 2 [simplification]

  // result = the emitted output (each closed group rotated to c2 c0 c1).
  syntax IntSeq ::= decRes(IntSeq, IntSeq, IntSeq, IntSeq, Int) [function, total]
  rule decRes(.IntSeq, RESULT:IntSeq, _C0:IntSeq, _C1:IntSeq, _COUNT:Int) => RESULT [simplification]
  rule decRes(iCons(C:Int, S:IntSeq), RESULT:IntSeq, _C0:IntSeq, C1:IntSeq, COUNT:Int) => decRes(S, RESULT, iCons(C, .IntSeq), C1, 1) requires COUNT ==Int 0 [simplification]
  rule decRes(iCons(C:Int, S:IntSeq), RESULT:IntSeq, C0:IntSeq, _C1:IntSeq, COUNT:Int) => decRes(S, RESULT, C0, iCons(C, .IntSeq), 2) requires COUNT ==Int 1 [simplification]
  rule decRes(iCons(C:Int, S:IntSeq), RESULT:IntSeq, C0:IntSeq, C1:IntSeq, COUNT:Int)
    => decRes(S, seqConcat(seqConcat(seqConcat(RESULT, iCons(C, .IntSeq)), C0), C1), C0, C1, 0) requires COUNT ==Int 2 [simplification]
  rule decRes(iCons(C:Int, S:IntSeq), RESULT:IntSeq, C0:IntSeq, C1:IntSeq, COUNT:Int) => decRes(S, RESULT, C0, C1, COUNT +Int 1)
    requires COUNT =/=Int 0 andBool COUNT =/=Int 1 andBool COUNT =/=Int 2 [simplification]
endmodule
