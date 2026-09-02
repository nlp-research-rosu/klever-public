// verification.k — summary for the separate_paren_groups proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module SEPARATE-PAREN-GROUPS-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // groupsOf(CS, D, CUR) = the list of completed groups (a group is emitted when depth
  // returns to 0 on a ')'). '(' = 40, ')' = 41; other chars (spaces) are ignored.
  syntax ValSeq ::= groupsOf(IntSeq, Int, IntSeq) [function, total]
  rule groupsOf(.IntSeq, _:Int, _:IntSeq) => .ValSeq [simplification]
  rule groupsOf(iCons(C:Int, S:IntSeq), D:Int, CUR:IntSeq)
    => groupsOf(S, D +Int 1, seqConcat(CUR, iCons(C, .IntSeq))) requires C ==Int 40 [simplification]
  rule groupsOf(iCons(C:Int, S:IntSeq), D:Int, CUR:IntSeq)
    => vCons(str(seqConcat(CUR, iCons(C, .IntSeq))), groupsOf(S, 0, .IntSeq))
    requires C ==Int 41 andBool D -Int 1 ==Int 0 [simplification]
  rule groupsOf(iCons(C:Int, S:IntSeq), D:Int, CUR:IntSeq)
    => groupsOf(S, D -Int 1, seqConcat(CUR, iCons(C, .IntSeq))) requires C ==Int 41 andBool D -Int 1 =/=Int 0 [simplification]
  rule groupsOf(iCons(C:Int, S:IntSeq), D:Int, CUR:IntSeq)
    => groupsOf(S, D, CUR) requires C =/=Int 40 andBool C =/=Int 41 [simplification]

  // curAfter(CS, D, CUR) = the final `current` string codes.
  syntax IntSeq ::= curAfter(IntSeq, Int, IntSeq) [function, total]
  rule curAfter(.IntSeq, _:Int, CUR:IntSeq) => CUR [simplification]
  rule curAfter(iCons(C:Int, S:IntSeq), D:Int, CUR:IntSeq)
    => curAfter(S, D +Int 1, seqConcat(CUR, iCons(C, .IntSeq))) requires C ==Int 40 [simplification]
  rule curAfter(iCons(C:Int, S:IntSeq), D:Int, _CUR:IntSeq)
    => curAfter(S, 0, .IntSeq) requires C ==Int 41 andBool D -Int 1 ==Int 0 [simplification]
  rule curAfter(iCons(C:Int, S:IntSeq), D:Int, CUR:IntSeq)
    => curAfter(S, D -Int 1, seqConcat(CUR, iCons(C, .IntSeq))) requires C ==Int 41 andBool D -Int 1 =/=Int 0 [simplification]
  rule curAfter(iCons(C:Int, S:IntSeq), D:Int, CUR:IntSeq)
    => curAfter(S, D, CUR) requires C =/=Int 40 andBool C =/=Int 41 [simplification]

  // depthAfter(CS, D) = the final depth.
  syntax Int ::= depthAfter(IntSeq, Int) [function, total]
  rule depthAfter(.IntSeq, D:Int) => D [simplification]
  rule depthAfter(iCons(C:Int, S:IntSeq), D:Int) => depthAfter(S, D +Int 1) requires C ==Int 40 [simplification]
  rule depthAfter(iCons(C:Int, S:IntSeq), D:Int) => depthAfter(S, D -Int 1) requires C ==Int 41 [simplification]
  rule depthAfter(iCons(C:Int, S:IntSeq), D:Int) => depthAfter(S, D) requires C =/=Int 40 andBool C =/=Int 41 [simplification]

endmodule
