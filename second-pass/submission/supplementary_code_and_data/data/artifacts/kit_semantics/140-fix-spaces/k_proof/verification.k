requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Exact AST aliases for the implementation generated in solution.mpy.
  syntax Stmts ::= "#fixSpacesLoopBody" [function, total]
  rule #fixSpacesLoopBody
    => If(
         Compare(Name("char"), CmpOp("==", Str(" "))),
         If(
           Compare(Name("spaces"), CmpOp("==", Str("__"))),
           Assign(Name("spaces"), Str("-")),
           If(
             Compare(Name("spaces"), CmpOp("!=", Str("-"))),
             AugAssign(Name("spaces"), "+", Str("_")),
             .Stmts)),
         AugAssign(
           Name("result"),
           "+",
           BinOp("+", Name("spaces"), Name("char")))
         Assign(Name("spaces"), Str("")))

  syntax Stmts ::= "#fixSpacesBody" [function, total]
  rule #fixSpacesBody
    => Assign(Name("result"), Str(""))
       Assign(Name("spaces"), Str(""))
       Assign(Name("char"), Str(""))
       For(Name("char"), Name("text"), #fixSpacesLoopBody)
       Return(BinOp("+", Name("result"), Name("spaces")))

  // The pending-space encoding after reading one additional space.
  syntax IntSeq ::= pendingSpace(IntSeq) [function, total]
  rule pendingSpace(P:IntSeq)
    => iCons(45, .IntSeq)
    requires P ==K iCons(95, iCons(95, .IntSeq))
  rule pendingSpace(P:IntSeq)
    => P
    requires P ==K iCons(45, .IntSeq)
     andBool notBool (P ==K iCons(95, iCons(95, .IntSeq)))
  rule pendingSpace(P:IntSeq)
    => seqConcat(P, iCons(95, .IntSeq))
    requires notBool (P ==K iCons(95, iCons(95, .IntSeq)))
     andBool notBool (P ==K iCons(45, .IntSeq))

  // Exact final local-state summaries for the remaining character sequence.
  syntax IntSeq ::= resultAfter(IntSeq, IntSeq, IntSeq) [function, total]
  rule resultAfter(.IntSeq, R:IntSeq, _P:IntSeq) => R
  rule resultAfter(iCons(32, CS:IntSeq), R:IntSeq, P:IntSeq)
    => resultAfter(CS, R, pendingSpace(P))
  rule resultAfter(iCons(C:Int, CS:IntSeq), R:IntSeq, P:IntSeq)
    => resultAfter(
         CS,
         seqConcat(R, seqConcat(P, iCons(C, .IntSeq))),
         .IntSeq)
    requires C =/=Int 32
    [simplification]

  syntax IntSeq ::= pendingAfter(IntSeq, IntSeq) [function, total]
  rule pendingAfter(.IntSeq, P:IntSeq) => P
  rule pendingAfter(iCons(32, CS:IntSeq), P:IntSeq)
    => pendingAfter(CS, pendingSpace(P))
  rule pendingAfter(iCons(C:Int, CS:IntSeq), _P:IntSeq)
    => pendingAfter(CS, .IntSeq)
    requires C =/=Int 32
    [simplification]

  syntax Val ::= charAfter(IntSeq, Val) [function, total]
  rule charAfter(.IntSeq, CH:Val) => CH
  rule charAfter(iCons(C:Int, CS:IntSeq), _CH:Val)
    => charAfter(CS, str(iCons(C, .IntSeq)))

  syntax IntSeq ::= fixedSpaces(IntSeq) [function, total]
  rule fixedSpaces(CS:IntSeq)
    => seqConcat(
         resultAfter(CS, .IntSeq, .IntSeq),
         pendingAfter(CS, .IntSeq))
endmodule
