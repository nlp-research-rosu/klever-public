requires "reference-semantics/semantics.k"

module STRING-XOR-VERIFICATION
  imports MPY

  // The mathematical result, expressed as an accumulator over the two
  // sequences of character codes.  The shorter input determines the length.
  syntax Bool ::= binaryCode(Int) [function, total]
  rule binaryCode(C:Int) => C ==Int 48 orBool C ==Int 49

  syntax Int ::= xorCode(Int, Int) [function]
  rule xorCode(A:Int, B:Int) => 48
    requires binaryCode(A) andBool binaryCode(B) andBool A ==Int B
  rule xorCode(A:Int, B:Int) => 49
    requires binaryCode(A) andBool binaryCode(B) andBool A =/=Int B

  syntax IntSeq ::= xorAcc(IntSeq, IntSeq, IntSeq) [function, total]
  rule xorAcc(P:IntSeq, .IntSeq, _:IntSeq) => P
  rule xorAcc(P:IntSeq, iCons(_:Int, _:IntSeq), .IntSeq) => P
  rule xorAcc(P:IntSeq, iCons(A:Int, AS:IntSeq), iCons(B:Int, BS:IntSeq))
    => xorAcc(seqConcat(P, iCons(xorCode(A, B), .IntSeq)), AS, BS)

  // The input predicate accepts only ASCII '0'/'1'.
  syntax Bool ::= binaryCodes(IntSeq) [function, total]
  rule binaryCodes(.IntSeq) => true
  rule binaryCodes(iCons(C:Int, REST:IntSeq))
    => binaryCode(C) andBool binaryCodes(REST)

  // Values left in the loop variables after zip terminates.  Initializing
  // x and y in solution.py makes these total even when the loop is empty.
  syntax IntSeq ::= xorLastX(IntSeq, IntSeq, IntSeq) [function, total]
                  | xorLastY(IntSeq, IntSeq, IntSeq) [function, total]
  rule xorLastX(.IntSeq, _:IntSeq, X:IntSeq) => X
  rule xorLastX(iCons(_:Int, _:IntSeq), .IntSeq, X:IntSeq) => X
  rule xorLastX(iCons(A:Int, AS:IntSeq), iCons(_:Int, BS:IntSeq), _:IntSeq)
    => xorLastX(AS, BS, iCons(A, .IntSeq))
  rule xorLastY(.IntSeq, _:IntSeq, Y:IntSeq) => Y
  rule xorLastY(iCons(_:Int, _:IntSeq), .IntSeq, Y:IntSeq) => Y
  rule xorLastY(iCons(_:Int, AS:IntSeq), iCons(B:Int, BS:IntSeq), _:IntSeq)
    => xorLastY(AS, BS, iCons(B, .IntSeq))

  // Exact constructors emitted by py2mpy.py for the loop and function body.
  syntax Expr ::= "stringXorTarget" [function]
  rule stringXorTarget => TupleExpr(Name("x"), Name("y"))

  syntax Stmts ::= "stringXorLoopBody" [function]
  rule stringXorLoopBody
    => If(Compare(Name("x"), CmpOp("==", Name("y"))),
          Assign(Name("result"), BinOp("+", Name("result"), Str("0"))),
          Assign(Name("result"), BinOp("+", Name("result"), Str("0"))))

  syntax Stmts ::= "stringXorBody" [function]
  rule stringXorBody
    => Expr(Str("Return the bitwise XOR of two binary strings."))
       Assign(Name("result"), Str(""))
       Assign(Name("x"), Str(""))
       Assign(Name("y"), Str(""))
       For(stringXorTarget, Call(Name("zip"), Name("a"), Name("b")),
           stringXorLoopBody)
       Return(Name("result"))

  syntax Val ::= "stringXorClosure" [function]
  rule stringXorClosure
    => closureVal(("a", "b", .ParamNames), stringXorBody, 0)

  syntax Module ::= "stringXorModule" [function]
  rule stringXorModule
    => Module(
         ImportFrom("typing", "List")
         FuncDef("string_xor", Params("a", "b"), stringXorBody))
endmodule
