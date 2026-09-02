// Probe: can kprove thread a SYMBOLIC K-Float through OPAQUE float ops (no-evaluators) in a fold?
// If yes, float map/fold problems (21/4) are provable with trusted float primitives.
module FP
  imports FLOAT
  imports INT
  imports BOOL
  syntax FloatSeq ::= ".FloatSeq" | fCons(Float, FloatSeq)
  // opaque trusted float op (like (x-lo)/d): no-evaluators -> opaque on symbolic Float
  syntax Float ::= rescale(Float, Float, Float) [function, total, no-evaluators]
  // map fold building an output FloatSeq
  syntax FloatSeq ::= mapF(FloatSeq, Float, Float) [function, total]
  rule mapF(.FloatSeq, _LO:Float, _D:Float) => .FloatSeq [simplification]
  rule mapF(fCons(X:Float, R:FloatSeq), LO:Float, D:Float)
        => fCons(rescale(X, LO, D), mapF(R, LO, D)) [simplification]
  // a driver loop that consumes a FloatSeq in the <k> cell
  syntax KItem ::= loop(FloatSeq, Float, Float, FloatSeq)
  rule <k> loop(.FloatSeq, _LO:Float, _D:Float, ACC:FloatSeq) => ACC ... </k>
  rule <k> loop(fCons(X:Float, R:FloatSeq), LO:Float, D:Float, ACC:FloatSeq)
        => loop(R, LO, D, appF(ACC, rescale(X, LO, D))) ... </k>
  syntax FloatSeq ::= appF(FloatSeq, Float) [function, total]
  rule appF(.FloatSeq, Y:Float) => fCons(Y, .FloatSeq)
  rule appF(fCons(X:Float, R:FloatSeq), Y:Float) => fCons(X, appF(R, Y))
  syntax FloatSeq ::= concatF(FloatSeq, FloatSeq) [function, total]
  rule concatF(.FloatSeq, B:FloatSeq) => B [simplification]
  rule concatF(fCons(X:Float, R:FloatSeq), B:FloatSeq) => fCons(X, concatF(R, B)) [simplification]
  // accumulator-THREADING map fold (mirrors the loop's appF exactly)
  syntax FloatSeq ::= mapFA(FloatSeq, Float, Float, FloatSeq) [function, total]
  rule mapFA(.FloatSeq, _LO:Float, _D:Float, ACC:FloatSeq) => ACC [simplification]
  rule mapFA(fCons(X:Float, R:FloatSeq), LO:Float, D:Float, ACC:FloatSeq)
        => mapFA(R, LO, D, appF(ACC, rescale(X, LO, D))) [simplification]
  configuration <k> $PGM:K </k>
endmodule
