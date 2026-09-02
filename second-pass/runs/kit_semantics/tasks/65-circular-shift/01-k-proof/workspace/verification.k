requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // K's Int2String hook always emits an ASCII decimal representation.  The
  // supplied strToCodes definition is partial only because arbitrary String
  // values may contain non-ASCII characters; this composition is defined.
  rule #Ceil(strToCodes(Int2String(X:Int))) => #Top [simplification]

  // Exact transliteration of solution.mpy's function value.  This is only a
  // compact syntax name for use in the three complementary claims; calls
  // still execute the supplied lookup, argument, frame, body, and return rules.
  syntax Val ::= "circularShiftClosure" [function, total]
  rule circularShiftClosure
    => closureVal(
         ("x", "shift", .ParamNames),
         Assign(Name("s"), Call(Name("str"), (Name("x"), .Exprs)))
         Return(
           IfExp(
             Compare(
               Name("shift"),
               CmpOp(">", Call(Name("len"), (Name("s"), .Exprs)))),
             Subscript(
               Name("s"),
               Slice(NoBound, NoBound, UnaryOp("-", Int(1)))),
             IfExp(
               Compare(Name("shift"), CmpOp("<", Int(0))),
               Name("s"),
               Subscript(
                 BinOp("+", Name("s"), Name("s")),
                 Slice(
                   BinOp(
                     "-",
                     Call(Name("len"), (Name("s"), .Exprs)),
                     Name("shift")),
                   BinOp(
                     "-",
                     BinOp(
                       "*",
                       Int(2),
                       Call(Name("len"), (Name("s"), .Exprs))),
                     Name("shift")),
                   NoBound)))))
         .Stmts,
         0)

  // Mathematical result of the Python function, expressed entirely with the
  // fixed semantics' decimal conversion and string-slice functions.
  syntax Str ::= circularShiftResult(Int, Int) [function, total]

  rule circularShiftResult(X:Int, SHIFT:Int)
    => str(buildIS(
         strToCodes(Int2String(X)),
         isLen(strToCodes(Int2String(X))) -Int 1,
         -1,
         -1))
    requires SHIFT >Int isLen(strToCodes(Int2String(X)))

  rule circularShiftResult(X:Int, SHIFT:Int)
    => str(strToCodes(Int2String(X)))
    requires notBool (
               SHIFT >Int isLen(strToCodes(Int2String(X))))
      andBool SHIFT <Int 0

  rule circularShiftResult(X:Int, SHIFT:Int)
    => str(buildIS(
         seqConcat(
           strToCodes(Int2String(X)),
           strToCodes(Int2String(X))),
         slAdjust(
           isLen(strToCodes(Int2String(X))) -Int SHIFT,
           isLen(seqConcat(
             strToCodes(Int2String(X)),
             strToCodes(Int2String(X)))),
           1),
         slAdjust(
           (2 *Int isLen(strToCodes(Int2String(X)))) -Int SHIFT,
           isLen(seqConcat(
             strToCodes(Int2String(X)),
             strToCodes(Int2String(X)))),
           1),
         1))
    requires notBool (
               SHIFT >Int isLen(strToCodes(Int2String(X))))
      andBool notBool (SHIFT <Int 0)
endmodule
