requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  syntax Bool ::= isNumericVal(Val) [function, total]
  rule isNumericVal(V:Val)
    => isInt(V) orBool isBool(V) orBool isFloat(V)

  syntax Bool ::= orderablePair(Val, Val) [function, total]
  rule orderablePair(V:Val, W:Val)
    => (isNumericVal(V) andBool isNumericVal(W))
       orBool (isStr(V) andBool isStr(W))

  // This recursive predicate exactly characterizes the list inputs for which
  // every comparison performed by the scan is defined in MPY.  The first
  // element is unrestricted because the program does not compare it.
  syntax Bool ::= scanDefined(ValSeq, Int, Val)
    [function, total, no-evaluators]
  rule scanDefined(.ValSeq, _I:Int, _P:Val) => true
    [simplification]
  rule scanDefined(vCons(V:Val, R:ValSeq), I:Int, _P:Val)
    => scanDefined(R, I +Int 1, V)
    requires I ==Int 0
    [simplification]
  rule scanDefined(vCons(V:Val, R:ValSeq), I:Int, P:Val)
    => orderablePair(V, P) andBool scanDefined(R, I +Int 1, V)
    requires I >Int 0
    [simplification]
  rule scanDefined(vCons(_V:Val, _R:ValSeq), I:Int, _P:Val) => false
    requires I <Int 0
    [simplification]

  // A total mathematical presentation of the fixed semantics' >= dispatch.
  // The ten orderable cases are disjoint and cover orderablePair exactly.
  syntax Bool ::= orderGe(Val, Val)
    [function, total, no-evaluators]
  rule orderGe(I:Int, J:Int) => I >=Int J [simplification]
  rule orderGe(B:Bool, C:Bool)
    => boolAsInt(B) >=Int boolAsInt(C)
    [simplification]
  rule orderGe(B:Bool, I:Int)
    => boolAsInt(B) >=Int I
    [simplification]
  rule orderGe(I:Int, B:Bool)
    => I >=Int boolAsInt(B)
    [simplification]
  rule orderGe(F:Float, G:Float)
    => notBool floatLt(F, G)
    [simplification]
  rule orderGe(I:Int, F:Float)
    => notBool ltIF(I, F)
    [simplification]
  rule orderGe(F:Float, I:Int)
    => notBool ltFI(F, I)
    [simplification]
  rule orderGe(B:Bool, F:Float)
    => notBool ltIF(boolAsInt(B), F)
    [simplification]
  rule orderGe(F:Float, B:Bool)
    => notBool ltFI(F, boolAsInt(B))
    [simplification]
  rule orderGe(str(A:IntSeq), str(B:IntSeq))
    => notBool strLt(A, B)
    [simplification]
  rule orderGe(V:Val, W:Val) => false
    requires notBool orderablePair(V, W)
    [simplification]

  // Mathematical left-to-right scan of the unvisited suffix.  I is the
  // current absolute index, P is the preceding value (ignored when I == 0),
  // and A is the largest matching index already seen.
  syntax Int ::= arrangeSeq(ValSeq, Int, Val, Int)
    [function, total, no-evaluators]

  rule arrangeSeq(.ValSeq, _I:Int, _P:Val, A:Int) => A
    [simplification]

  rule arrangeSeq(vCons(V:Val, R:ValSeq), I:Int, _P:Val, A:Int)
    => arrangeSeq(R, I +Int 1, V, A)
    requires I ==Int 0
    [simplification]

  rule arrangeSeq(vCons(V:Val, R:ValSeq), I:Int, P:Val, _A:Int)
    => arrangeSeq(R, I +Int 1, V, I)
    requires I >Int 0
     andBool notBool orderGe(V, P)
    [simplification]

  rule arrangeSeq(vCons(V:Val, R:ValSeq), I:Int, P:Val, A:Int)
    => arrangeSeq(R, I +Int 1, V, A)
    requires I >Int 0
     andBool orderGe(V, P)
    [simplification]

  rule arrangeSeq(vCons(_V:Val, _R:ValSeq), I:Int, _P:Val, A:Int) => A
    requires I <Int 0
    [simplification]
endmodule

module VERIFICATION
  imports VERIFICATION-BASE

  // Guarded dynamic-dispatch bridge.  connection-spec.k proves, without this
  // module, that each of its ten static cases is the corresponding MPY rule.
  rule applyCmp(">=", V:Val, W:Val) => orderGe(V, W)
    requires orderablePair(V, W)
    [simplification]
endmodule
