// verif5.k — probe the "canonical solution + ONE trusted bridge" design (Shape A).
// The Python stays canonical: `for i in str(abs(num)): even += ev(int(i))`, modelled by the
// <k>-cell fold #strFold over the digit codes of str(N).  The input integer is presented as
// intOf(CS) for a symbolic digit sequence CS.  The ONLY new thing is ONE [simplification] —
// the bridge strCodes(intOf(CS)) => CS — which is trusted in K and PROVEN IN LEAN (it is the
// round-trip we already showed is true). Question: does that let the canonical fold close?

module VERIF5
  imports INT
  imports BOOL
  imports LIST
  imports MAP
  imports K-EQUAL

  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)

  syntax Int ::= ev(Int) [function, total]
  rule ev(D:Int) => #if D modInt 2 ==Int 0 #then 1 #else 0 #fi

  // the canonical loop's effect: fold even-count over the digit codes of a str value.
  syntax KItem ::= #strFold(IntSeq, Int)
  rule <k> #strFold(.IntSeq, A:Int)               => A ... </k>
  rule <k> #strFold(iCons(C:Int, T:IntSeq), A:Int) => #strFold(T, A +Int ev(C -Int 48)) ... </k>

  // the summary the fold should reach
  syntax Int ::= evenSeq(IntSeq, Int) [function]
  rule evenSeq(.IntSeq, EC:Int)               => EC
  rule evenSeq(iCons(C:Int, T:IntSeq), EC:Int) => evenSeq(T, EC +Int ev(C -Int 48))

  // intOf: an OPAQUE carrier — "the integer whose decimal digits are CS". It does not
  // reduce (no-evaluators), so the bridge below keeps matching on it.
  syntax Int ::= intOf(IntSeq) [function, total, no-evaluators, symbol(intOf)]

  // strCodes(N) = the digit codes of str(N) (what the canonical loop iterates).
  syntax IntSeq ::= strCodes(Int) [function]

  // ===== THE BRIDGE (trusted in K; the Lean obligation) =====================
  // str of the number whose digits are CS gives back CS. This is the ONE fact Lean proves.
  rule strCodes(intOf(CS:IntSeq)) => CS [simplification]
endmodule
