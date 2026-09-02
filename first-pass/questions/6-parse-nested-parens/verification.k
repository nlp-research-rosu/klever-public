// verification.k — parse_nested_parens on the UNIFIED semantics. A single flat char-scan over
// `paren_string + ' '` (the trailing-space sentinel flushes the last group; a `has` flag drops
// empty groups = the canonical `if x` filter). FOUR coupled accumulators — result (list of max
// depths), depth, curmax, has — folded by the same five-case split per char code C:
//   1. C==40 '(' & D+1 >  M : depth:=D+1, curmax:=D+1, has:=true
//   2. C==40 '(' & D+1 <= M : depth:=D+1, curmax:=M,   has:=true
//   3. C==32 ' ' & HAS      : result += [M]; depth:=0, curmax:=0, has:=false
//   4. C==32 ' ' & !HAS     : no-op (drop an empty group)
//   5. else (a ')')         : depth:=D-1, curmax:=M, has:=true
// See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module PARSE-NESTED-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // parseRes(CS, RESULT, D, M, HAS) = the final result list (of max-depth ints).
  syntax ValSeq ::= parseRes(IntSeq, ValSeq, Int, Int, Bool) [function, total]
  rule parseRes(.IntSeq, RESULT:ValSeq, _D:Int, _M:Int, _HAS:Bool) => RESULT [simplification]
  rule parseRes(iCons(C:Int, S:IntSeq), RESULT:ValSeq, D:Int, M:Int, _HAS:Bool)
    => parseRes(S, RESULT, D +Int 1, D +Int 1, true) requires C ==Int 40 andBool (D +Int 1)  >Int M [simplification]
  rule parseRes(iCons(C:Int, S:IntSeq), RESULT:ValSeq, D:Int, M:Int, _HAS:Bool)
    => parseRes(S, RESULT, D +Int 1, M, true) requires C ==Int 40 andBool notBool ((D +Int 1) >Int M) [simplification]
  rule parseRes(iCons(C:Int, S:IntSeq), RESULT:ValSeq, _D:Int, M:Int, HAS:Bool)
    => parseRes(S, valSeqConcat(RESULT, vCons(M, .ValSeq)), 0, 0, false) requires C ==Int 32 andBool HAS [simplification]
  rule parseRes(iCons(C:Int, S:IntSeq), RESULT:ValSeq, D:Int, M:Int, HAS:Bool)
    => parseRes(S, RESULT, D, M, HAS) requires C ==Int 32 andBool notBool HAS [simplification]
  rule parseRes(iCons(C:Int, S:IntSeq), RESULT:ValSeq, D:Int, M:Int, _HAS:Bool)
    => parseRes(S, RESULT, D -Int 1, M, true) requires C =/=Int 40 andBool C =/=Int 32 [simplification]

  // parseDepth / parseMax / parseHas — the same five-case split, extracting the final scalar.
  syntax Int ::= parseDepth(IntSeq, Int, Int, Bool) [function, total]
  rule parseDepth(.IntSeq, D:Int, _M:Int, _HAS:Bool) => D [simplification]
  rule parseDepth(iCons(C:Int, S:IntSeq), D:Int, M:Int, _HAS:Bool) => parseDepth(S, D +Int 1, D +Int 1, true)
    requires C ==Int 40 andBool (D +Int 1)  >Int M [simplification]
  rule parseDepth(iCons(C:Int, S:IntSeq), D:Int, M:Int, _HAS:Bool) => parseDepth(S, D +Int 1, M, true)
    requires C ==Int 40 andBool notBool ((D +Int 1) >Int M) [simplification]
  rule parseDepth(iCons(C:Int, S:IntSeq), _D:Int, _M:Int, HAS:Bool) => parseDepth(S, 0, 0, false)
    requires C ==Int 32 andBool HAS [simplification]
  rule parseDepth(iCons(C:Int, S:IntSeq), D:Int, M:Int, HAS:Bool) => parseDepth(S, D, M, HAS)
    requires C ==Int 32 andBool notBool HAS [simplification]
  rule parseDepth(iCons(C:Int, S:IntSeq), D:Int, M:Int, _HAS:Bool) => parseDepth(S, D -Int 1, M, true)
    requires C =/=Int 40 andBool C =/=Int 32 [simplification]

  syntax Int ::= parseMax(IntSeq, Int, Int, Bool) [function, total]
  rule parseMax(.IntSeq, _D:Int, M:Int, _HAS:Bool) => M [simplification]
  rule parseMax(iCons(C:Int, S:IntSeq), D:Int, M:Int, _HAS:Bool) => parseMax(S, D +Int 1, D +Int 1, true)
    requires C ==Int 40 andBool (D +Int 1)  >Int M [simplification]
  rule parseMax(iCons(C:Int, S:IntSeq), D:Int, M:Int, _HAS:Bool) => parseMax(S, D +Int 1, M, true)
    requires C ==Int 40 andBool notBool ((D +Int 1) >Int M) [simplification]
  rule parseMax(iCons(C:Int, S:IntSeq), _D:Int, _M:Int, HAS:Bool) => parseMax(S, 0, 0, false)
    requires C ==Int 32 andBool HAS [simplification]
  rule parseMax(iCons(C:Int, S:IntSeq), D:Int, M:Int, HAS:Bool) => parseMax(S, D, M, HAS)
    requires C ==Int 32 andBool notBool HAS [simplification]
  rule parseMax(iCons(C:Int, S:IntSeq), D:Int, M:Int, _HAS:Bool) => parseMax(S, D -Int 1, M, true)
    requires C =/=Int 40 andBool C =/=Int 32 [simplification]

  syntax Bool ::= parseHas(IntSeq, Int, Int, Bool) [function, total]
  rule parseHas(.IntSeq, _D:Int, _M:Int, HAS:Bool) => HAS [simplification]
  rule parseHas(iCons(C:Int, S:IntSeq), D:Int, M:Int, _HAS:Bool) => parseHas(S, D +Int 1, D +Int 1, true)
    requires C ==Int 40 andBool (D +Int 1)  >Int M [simplification]
  rule parseHas(iCons(C:Int, S:IntSeq), D:Int, M:Int, _HAS:Bool) => parseHas(S, D +Int 1, M, true)
    requires C ==Int 40 andBool notBool ((D +Int 1) >Int M) [simplification]
  rule parseHas(iCons(C:Int, S:IntSeq), _D:Int, _M:Int, HAS:Bool) => parseHas(S, 0, 0, false)
    requires C ==Int 32 andBool HAS [simplification]
  rule parseHas(iCons(C:Int, S:IntSeq), D:Int, M:Int, HAS:Bool) => parseHas(S, D, M, HAS)
    requires C ==Int 32 andBool notBool HAS [simplification]
  rule parseHas(iCons(C:Int, S:IntSeq), D:Int, M:Int, _HAS:Bool) => parseHas(S, D -Int 1, M, true)
    requires C =/=Int 40 andBool C =/=Int 32 [simplification]
endmodule
