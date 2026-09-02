requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY

  syntax ValSeq ::= collect(ValSeq, ValSeq) [function]
                  | appendCandidate(ValSeq, Val) [function]

  syntax Bool ::= integerVals(ValSeq) [function, total]

  syntax Int ::= scanBad(Int, Int) [function, total]
               | scanNumber(Int) [function, total]
               | afterNumber(ValSeq, Int) [function]
               | afterBad(ValSeq, Int) [function]

  syntax Val ::= afterValue(ValSeq, Val) [function, total]
endmodule

module VERIFICATION
  imports VERIFICATION-SYNTAX
  imports MPY

  // The theorem covers all integer lists; the HumanEval positive-integer
  // domain is a subset.
  rule integerVals(.ValSeq) => true
  rule integerVals(vCons(V:Val, VS:ValSeq))
    => isInt(V) andBool integerVals(VS)

  // Exact final bad-counter value of the decimal digit loop.
  rule scanBad(B:Int, N:Int) => B
    requires N <=Int 0
  rule scanBad(B:Int, N:Int)
    => scanBad(
         B +Int (#if pyMod(N, 2) ==Int 0 #then 1 #else 0 #fi),
         (N -Int pyMod(N, 10)) /Int 10)
    requires N >Int 0

  rule scanNumber(N:Int)
    => #if N >Int 0 #then 0 #else N #fi

  rule appendCandidate(VS:ValSeq, V:Val)
    => valSeqConcat(VS, vCons(V, .ValSeq))
    requires isInt(V)
     andBool scanBad(0, intOf(V)) ==Int 0
  rule appendCandidate(VS:ValSeq, V:Val) => VS
    requires isInt(V)
     andBool scanBad(0, intOf(V)) =/=Int 0

  // Exact accumulator fold for the outer loop over the admitted input domain.
  rule collect(ACC:ValSeq, .ValSeq) => ACC
  rule collect(ACC:ValSeq, vCons(V:Val, VS:ValSeq))
    => collect(appendCandidate(ACC, V), VS)
    requires isInt(V)

  // Python for-loop targets and body locals persist after the loop.
  rule afterValue(.ValSeq, V:Val) => V
  rule afterValue(vCons(V:Val, VS:ValSeq), _:Val)
    => afterValue(VS, V)

  rule afterNumber(.ValSeq, N:Int) => N
  rule afterNumber(vCons(V:Val, VS:ValSeq), _:Int)
    => afterNumber(VS, scanNumber(intOf(V)))
    requires isInt(V)

  rule afterBad(.ValSeq, B:Int) => B
  rule afterBad(vCons(V:Val, VS:ValSeq), _:Int)
    => afterBad(VS, scanBad(0, intOf(V)))
    requires isInt(V)
endmodule
