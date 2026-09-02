requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
  imports BOOL
  imports INT

  // Mathematical scan of the unprocessed suffix.  The third argument records
  // whether every prefix processed so far had nonnegative balance.
  syntax Bool ::= scanBrackets(IntSeq, Int, Bool) [function, total]
  rule scanBrackets(.IntSeq, B:Int, V:Bool)
    => V andBool B ==Int 0
  rule scanBrackets(iCons(C:Int, REST:IntSeq), B:Int, V:Bool)
    => scanBrackets(
         REST,
         #if C ==Int 40 #then B +Int 1 #else B -Int 1 #fi,
         keepValid(
           #if C ==Int 40 #then B +Int 1 #else B -Int 1 #fi,
           V))

  // This is the source-level `if balance < 0: valid = False`.
  syntax Bool ::= keepValid(Int, Bool) [function, total]
  rule keepValid(B:Int, _:Bool) => false requires B <Int 0
  rule keepValid(B:Int, V:Bool) => V     requires B >=Int 0

  // The backend does not otherwise simplify this polymorphic conditional from
  // the symbolic disequality emitted by the source-level `else` branch.
  rule (#if C ==Int 40 #then _X:Int #else Y:Int #fi) => Y
    requires C =/=Int 40
    [simplification]

  // Exact formalization of prompt.py's input domain.
  syntax Bool ::= bracketInput(IntSeq) [function, total]
  rule bracketInput(.IntSeq) => true
  rule bracketInput(iCons(C:Int, REST:IntSeq))
    => (C ==Int 40 orBool C ==Int 41) andBool bracketInput(REST)
endmodule
