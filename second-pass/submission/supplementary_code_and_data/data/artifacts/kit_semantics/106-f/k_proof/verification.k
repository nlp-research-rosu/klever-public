requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Definitional summary of the final factorial accumulator after the source
  // loop processes indices I through N, starting with accumulator F.
  syntax Int ::= factRun(Int, Int, Int)
    [function, total, no-evaluators]
  rule factRun(I, N, F) => factRun(I +Int 1, N, F *Int I)
    requires I <=Int N
    [concrete]
  rule factRun(I, N, F) => F
    requires I >Int N
    [concrete]
  rule factRun(I +Int 1, N, F *Int I) => factRun(I, N, F)
    requires I <=Int N
    [simplification]
  rule factRun(I, N, F) => F
    requires I >Int N
    [simplification]

  // The analogous summary for the running triangular-number accumulator.
  syntax Int ::= totalRun(Int, Int, Int)
    [function, total, no-evaluators]
  rule totalRun(I, N, T) => totalRun(I +Int 1, N, T +Int I)
    requires I <=Int N
    [concrete]
  rule totalRun(I, N, T) => T
    requires I >Int N
    [concrete]
  rule totalRun(I +Int 1, N, T +Int I) => totalRun(I, N, T)
    requires I <=Int N
    [simplification]
  rule totalRun(I, N, T) => T
    requires I >Int N
    [simplification]

  // Definitional summary of the final list after the same source iterations.
  // Its equations are exhaustive and disjoint: the loop is finished, the
  // current index is even, or the current index is odd.
  syntax ValSeq ::= resultRun(ValSeq, Int, Int, Int, Int)
    [function, total, no-evaluators]
  rule resultRun(VS, I, N, F, T)
    => resultRun(
         valSeqConcat(VS, vCons(F *Int I, .ValSeq)),
         I +Int 1,
         N,
         F *Int I,
         T +Int I)
    requires I <=Int N andBool pyMod(I, 2) ==Int 0
    [concrete]
  rule resultRun(VS, I, N, F, T)
    => resultRun(
         valSeqConcat(
           VS,
           vCons(T +Int I, .ValSeq)),
         I +Int 1,
         N,
         F *Int I,
         T +Int I)
    requires I <=Int N andBool pyMod(I, 2) =/=Int 0
    [concrete]
  rule resultRun(VS, I, N, _F, _T) => VS
    requires I >Int N
    [concrete]

  rule resultRun(
         valSeqConcat(VS, vCons(F *Int I, .ValSeq)),
         I +Int 1,
         N,
         F *Int I,
         T +Int I)
    => resultRun(VS, I, N, F, T)
    requires I <=Int N andBool pyMod(I, 2) ==Int 0
    [simplification]
  rule resultRun(
         valSeqConcat(VS, vCons(T +Int I, .ValSeq)),
         I +Int 1,
         N,
         F *Int I,
         T +Int I)
    => resultRun(VS, I, N, F, T)
    requires I <=Int N andBool pyMod(I, 2) =/=Int 0
    [simplification]
  rule resultRun(VS, I, N, _F, _T) => VS
    requires I >Int N
    [simplification]
endmodule
