requires "reference-semantics/semantics.k"

module CONCATENATE-VERIFICATION
  imports MPY

  // A symbolic type predicate for the List[str] precondition.
  syntax Bool ::= isStringValue(Val) [function, total]
  rule isStringValue(str(_:IntSeq)) => true
  rule isStringValue(_:Val) => false [owise]

  syntax Bool ::= allStringValues(ValSeq) [function, total]
  rule allStringValues(.ValSeq) => true
  rule allStringValues(vCons(V:Val, VS:ValSeq))
    => isStringValue(V) andBool allStringValues(VS)

  // This projection is only used under isStringValue(V). The extra applyBin
  // rule is a symbolic generalization of MPY-STR's concrete str/str rule:
  // when V is a string, both rules produce the identical term.
  syntax IntSeq ::= stringCodes(Val) [function, total]
  rule stringCodes(str(S:IntSeq)) => S
  rule applyBin("+", str(A:IntSeq), V:Val)
    => str(seqConcat(A, stringCodes(V)))
    requires isStringValue(V)

  // The accumulator and loop-variable folds used in the postcondition.
  syntax IntSeq ::= concatenateValues(IntSeq, ValSeq) [function, total]
  rule concatenateValues(A:IntSeq, .ValSeq) => A
  rule concatenateValues(A:IntSeq, vCons(V:Val, VS:ValSeq))
    => concatenateValues(seqConcat(A, stringCodes(V)), VS)

  syntax Val ::= finalLoopValue(Val, ValSeq) [function, total]
  rule finalLoopValue(OLD:Val, .ValSeq) => OLD
  rule finalLoopValue(_:Val, vCons(V:Val, VS:ValSeq))
    => finalLoopValue(V, VS)

  // These definitions are the literal terms emitted in solution.mpy. Naming
  // them keeps the claims readable without introducing any semantic shortcut.
  syntax Stmts ::= "concatenateLoopBody" [function, total]
  rule concatenateLoopBody
    => AugAssign(Name("result"), "+", Name("string")) .Stmts

  syntax Stmts ::= "concatenateBody" [function, total]
  rule concatenateBody
    => Assign(Name("result"), Str(""))
       Assign(Name("string"), Str(""))
       For(Name("string"), Name("strings"), concatenateLoopBody)
       Return(Name("result"))
       .Stmts

  syntax Module ::= "concatenateModule" [function, total]
  rule concatenateModule
    => Module(
         ImportFrom("typing", "List")
         FuncDef("concatenate", Params("strings"), concatenateBody)
       )
endmodule
