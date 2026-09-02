requires "reference-semantics/semantics.k"

module CIRCULAR-SHIFT-VERIFICATION
  imports MPY

  // This is the exact function value produced by loading solution.mpy.
  syntax Val ::= "circularShiftClosure" [macro]
  rule circularShiftClosure
    => closureVal(
         ("x", "shift"),
         ( Assign(Name("s"), Call(Name("str"), Name("x")))
           If(
             Compare(
               Name("shift"),
               CmpOp(">", Call(Name("len"), Name("s")))
             ),
             Return(
               Subscript(
                 Name("s"),
                 Slice(NoBound, NoBound, UnaryOp("-", Int(1)))
               )
             ),
             .Stmts
           )
           Return(
             BinOp(
               "+",
               Subscript(
                 Name("s"),
                 Slice(UnaryOp("-", Name("shift")), NoBound, NoBound)
               ),
               Subscript(
                 Name("s"),
                 Slice(NoBound, UnaryOp("-", Name("shift")), NoBound)
               )
             )
           )
         ),
         0
       )

  // An executable, program-independent statement of the contract.  The first
  // rule is reversal.  The second takes the suffix of length SHIFT and then
  // the remaining prefix, which is a right circular shift.
  syntax Val ::= circularShiftSpec(Int, Int, Int) [function]
  rule circularShiftSpec(X:Int, SHIFT:Int, LEN:Int)
    => doSlice(
         str(strToCodes(Int2String(X))),
         noB,
         noB,
         someB(-1)
       )
    requires SHIFT >Int LEN

  rule circularShiftSpec(X:Int, SHIFT:Int, LEN:Int)
    => applyBin(
         "+",
         doSlice(
           str(strToCodes(Int2String(X))),
           someB(0 -Int SHIFT),
           noB,
           noB
         ),
         doSlice(
           str(strToCodes(Int2String(X))),
           noB,
           someB(0 -Int SHIFT),
           noB
         )
       )
    requires SHIFT <=Int LEN
endmodule
