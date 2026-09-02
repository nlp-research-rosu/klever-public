requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX

  syntax Int ::= collatzNext(Int) [function, total]
  syntax Bool ::= validCollatzTrace(ValSeq) [function, total]
  syntax Int ::= traceFirstInt(ValSeq) [function, total]
               | traceLastInt(ValSeq)  [function, total]
  syntax ValSeq ::= oddWithoutLast(ValSeq) [function, total]
                  | maybeOdd(Int)             [function, total]
endmodule

module VERIFICATION
  imports MPY
  imports VERIFICATION-SYNTAX

  // One exact source-level Collatz transition.  Python modulo by 2 is always
  // 0 or 1, so the equations are disjoint and exhaustive over Int.
  rule collatzNext(N:Int) => (N -Int pyMod(N, 2)) /Int 2
    requires pyMod(N, 2) ==Int 0
  rule collatzNext(N:Int) => (3 *Int N) +Int 1
    requires pyMod(N, 2) ==Int 1

  // A finite, nonempty Int sequence is a valid trace when every adjacent pair
  // follows collatzNext.  Recursion is structural on the supplied sequence;
  // this definition makes no assertion that every positive start reaches 1.
  rule validCollatzTrace(.ValSeq) => false
  rule validCollatzTrace(vCons(_:Int, .ValSeq)) => true
  rule validCollatzTrace(vCons(I:Int, vCons(J:Int, R:ValSeq)))
    => (J ==Int collatzNext(I))
       andBool validCollatzTrace(vCons(J, R))
  rule validCollatzTrace(_:ValSeq) => false [owise]

  rule traceFirstInt(vCons(I:Int, _:ValSeq)) => I
  rule traceFirstInt(_:ValSeq) => 0 [owise]

  rule traceLastInt(.ValSeq) => 0
  rule traceLastInt(vCons(I:Int, .ValSeq)) => I
  rule traceLastInt(vCons(_:Val, vCons(V:Val, R:ValSeq)))
    => traceLastInt(vCons(V, R))
  rule traceLastInt(_:ValSeq) => 0 [owise]

  rule maybeOdd(N:Int) => .ValSeq
    requires pyMod(N, 2) ==Int 0
  rule maybeOdd(N:Int) => vCons(N, .ValSeq)
    requires pyMod(N, 2) ==Int 1

  // Odd Int values in all positions except the final trace position.
  rule oddWithoutLast(.ValSeq) => .ValSeq
  rule oddWithoutLast(vCons(_:Val, .ValSeq)) => .ValSeq
  rule oddWithoutLast(vCons(I:Int, vCons(V:Val, R:ValSeq)))
    => oddWithoutLast(vCons(V, R))
    requires pyMod(I, 2) ==Int 0
  rule oddWithoutLast(vCons(I:Int, vCons(V:Val, R:ValSeq)))
    => vCons(I, oddWithoutLast(vCons(V, R)))
    requires pyMod(I, 2) ==Int 1
  rule oddWithoutLast(vCons(_:Val, vCons(V:Val, R:ValSeq)))
    => oddWithoutLast(vCons(V, R))
    [owise]

  // Derived from MPY-LIST's two defining equations by structural induction
  // on A.  These only normalize mathematical sequence expressions.
  rule valSeqConcat(A:ValSeq, .ValSeq) => A
    [simplification]

  rule valSeqConcat(valSeqConcat(A:ValSeq, B:ValSeq), C:ValSeq)
    => valSeqConcat(A, valSeqConcat(B, C))
    [simplification]

  rule valSeqConcat(_:ValSeq, vCons(_:Val, _:ValSeq)) ==K .ValSeq
    => false
    [simplification]

  rule .ValSeq ==K valSeqConcat(_:ValSeq, vCons(_:Val, _:ValSeq))
    => false
    [simplification]

  // Append laws for the structurally defined finite-trace observers.  Each is
  // derived by structural induction on T; none replaces program execution.
  rule traceFirstInt(valSeqConcat(T:ValSeq, vCons(J:Int, .ValSeq)))
    => traceFirstInt(T)
    requires notBool (T ==K .ValSeq)
    [simplification]

  rule traceLastInt(valSeqConcat(_:ValSeq, vCons(J:Int, .ValSeq)))
    => J
    [simplification]

  rule validCollatzTrace(
         valSeqConcat(T:ValSeq, vCons(J:Int, .ValSeq)))
    => validCollatzTrace(T)
       andBool (J ==Int collatzNext(traceLastInt(T)))
    requires notBool (T ==K .ValSeq)
    [simplification]

  rule oddWithoutLast(
         valSeqConcat(T:ValSeq, vCons(_:Int, .ValSeq)))
    => valSeqConcat(
         oddWithoutLast(T),
         maybeOdd(traceLastInt(T)))
    requires validCollatzTrace(T)
    [simplification]
endmodule
