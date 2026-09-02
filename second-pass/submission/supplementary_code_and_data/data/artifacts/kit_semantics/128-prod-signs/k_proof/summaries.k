requires "reference-semantics/semantics.k"

module PROD-SUMMARIES-SYNTAX
  imports MPY-CORE

  syntax ValSeq ::= intVals(IntSeq) [functional]
  syntax Int ::= foldResult(IntSeq, Int, Int) [function]
  syntax Val ::= prodSignsResult(IntSeq) [function, total]
  syntax KItem ::= #typedNext(IntSeq)
endmodule

module PROD-SUMMARIES
  imports MPY
  imports PROD-SUMMARIES-SYNTAX

  rule <k> #typedNext(.IntSeq)
        => #iterDone ... </k>
  rule <k> #typedNext(iCons(VALUE:Int, REST:IntSeq))
        => #iterYield(VALUE, list(intVals(REST))) ... </k>

  rule foldResult(.IntSeq, TOTAL:Int, SIGN:Int)
    => TOTAL *Int SIGN
    [simplification]
  rule foldResult(iCons(VALUE:Int, REST:IntSeq), TOTAL:Int, SIGN:Int)
    => foldResult(
         REST,
         TOTAL +Int absInt(VALUE),
         0 -Int SIGN)
    requires VALUE <Int 0
    [simplification]
  rule foldResult(iCons(VALUE:Int, REST:IntSeq), TOTAL:Int, _SIGN:Int)
    => foldResult(
         REST,
         TOTAL +Int absInt(VALUE),
         0)
    requires notBool (VALUE <Int 0) andBool notBool (VALUE >Int 0)
    [simplification]
  rule foldResult(iCons(VALUE:Int, REST:IntSeq), TOTAL:Int, SIGN:Int)
    => foldResult(
         REST,
         TOTAL +Int absInt(VALUE),
         SIGN)
    requires VALUE >Int 0
    [simplification]

  rule prodSignsResult(.IntSeq) => noneV
  rule prodSignsResult(iCons(VALUE:Int, REST:IntSeq))
    => foldResult(iCons(VALUE, REST), 0, 1)
endmodule
