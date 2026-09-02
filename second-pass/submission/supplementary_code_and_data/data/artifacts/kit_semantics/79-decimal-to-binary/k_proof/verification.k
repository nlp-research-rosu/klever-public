requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // binRel(N, ACC, OUT) defines the sequence produced by completing the
  // repeated-divide-by-two loop from N with the already accumulated suffix
  // ACC.  Its three guards are disjoint and cover all mathematical integers.
  syntax Bool ::= binRel(Int, IntSeq, IntSeq) [function, total]

  rule binRel(N, ACC, OUT) => ACC ==K OUT
    requires N ==Int 0

  rule binRel(N, ACC, OUT)
    => binRel(
         (N -Int pyMod(N, 2)) /Int 2,
         iCons(48 +Int pyMod(N, 2), ACC),
         OUT)
    requires N >Int 0

  rule binRel(N, _ACC, _OUT) => false
    requires N <Int 0

  // The executable loop starts with the trailing "db" already in ACC.  The
  // task-level result then has a literal leading "db" followed by TAIL.
  syntax Bool ::= decimalTailRel(Int, IntSeq) [function, total]

  rule decimalTailRel(N, TAIL)
    => TAIL ==K iCons(48, iCons(100, iCons(98, .IntSeq)))
    requires N ==Int 0

  rule decimalTailRel(N, TAIL)
    => binRel(N, iCons(100, iCons(98, .IntSeq)), TAIL)
    requires N >Int 0

  rule decimalTailRel(N, _TAIL) => false
    requires N <Int 0

  syntax Bool ::= decimalResultRel(Int, IntSeq) [function, total]

  rule decimalResultRel(N, iCons(100, iCons(98, TAIL)))
    => decimalTailRel(N, TAIL)

  rule decimalResultRel(_N, _CODES) => false [owise]
endmodule
