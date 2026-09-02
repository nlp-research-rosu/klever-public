requires "reference-semantics/semantics.k"

module REMOVE-DUPLICATES-VERIFICATION
  imports MPY

  // HumanEval's input type is List[int].  The predicate is carried as the
  // symbolic precondition, excluding the other Val constructors in MPY.
  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(V:Val, REST:ValSeq))
    => isIntV(V) andBool allInts(REST)

  // Mathematical specification in accumulator form.  The form mirrors the
  // program loop and therefore also serves as its induction invariant.
  syntax ValSeq ::= keepSinglesAcc(ValSeq, ValSeq, ValSeq) [function, total]
  rule keepSinglesAcc(ACC:ValSeq, .ValSeq, _ALL:ValSeq) => ACC
    [simplification]
  rule keepSinglesAcc(ACC:ValSeq,
                      vCons(V:Val, REST:ValSeq),
                      ALL:ValSeq)
    => keepSinglesAcc(
         valSeqConcat(ACC, vCons(V, .ValSeq)),
         REST,
         ALL)
    requires 1 ==Int cntOccVS(ALL, V)
    [simplification]
  rule keepSinglesAcc(ACC:ValSeq,
                      vCons(V:Val, REST:ValSeq),
                      ALL:ValSeq)
    => keepSinglesAcc(ACC, REST, ALL)
    requires notBool (1 ==Int cntOccVS(ALL, V))
    [simplification]

  // The exact loop body emitted by py2mpy for solution.py.
  syntax Stmts ::= "#removeDuplicatesBody" [macro]
  rule #removeDuplicatesBody
    => If(
         Compare(
           Call(
             Attribute(Name("numbers"), "count"),
             Name("number"), .Exprs),
           CmpOp("==", Int(1))),
         Expr(
           Call(
             Attribute(Name("result"), "append"),
             Name("number"), .Exprs))
         .Stmts,
         .Stmts)
       .Stmts

  // Exact translated function body used by the entry-point claims.
  syntax Val ::= "#removeDuplicatesClosure" [macro]
  rule #removeDuplicatesClosure
    => closureVal(
         "numbers",
         Assign(Name("result"), ListExpr(.Exprs))
         For(
           Name("number"),
           Name("numbers"),
           #removeDuplicatesBody)
         Return(Name("result"))
         .Stmts,
         0)
endmodule
