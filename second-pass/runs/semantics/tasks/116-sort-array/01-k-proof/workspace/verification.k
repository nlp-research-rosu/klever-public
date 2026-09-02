requires "reference-semantics/semantics.k"

module SORT-ARRAY-VERIFICATION
  imports MPY

  // This is the translated program, factored into named terms so that the
  // specification can refer to exactly the code in solution.mpy.
  syntax Expr ::= "sortArrayLambda" [function, total]
  rule sortArrayLambda
    => Lambda(
         Params("value"),
         CellVars(.ParamNames),
         FreeVars(.ParamNames),
         IfExp(
           Compare(Name("value"), CmpOp("<", Int(0))),
           Int(0),
           Call(
             Attribute(Call(Name("bin"), Name("value")), "count"),
             Str("1"))))

  syntax Stmts ::= "sortArrayBody" [function, total]
  rule sortArrayBody
    => Return(
         Call(
           Name("sorted"),
           Call(Name("sorted"), Name("arr")),
           KwArg("key", sortArrayLambda)))

  syntax Val ::= "sortArrayClosure" [function, total]
  rule sortArrayClosure
    => closureVal("arr", sortArrayBody, 0)

  syntax Module ::= "sortArrayModule" [function, total]
  rule sortArrayModule
    => Module(FuncDef("sort_array", Params("arr"), sortArrayBody))

  // Evaluation of the annotated lambda above produces this closure.  The
  // reference semantics models keyed sorting by the trusted sortKeyVS
  // primitive, and ordinary integer sorting by sortVS.
  syntax Val ::= "popcountKeyClosure" [function, total]
  rule popcountKeyClosure
    => closureValC(
         "value",
         .ParamNames,
         Return(
           IfExp(
             Compare(Name("value"), CmpOp("<", Int(0))),
             Int(0),
             Call(
               Attribute(Call(Name("bin"), Name("value")), "count"),
               Str("1")))),
         .Map)

  syntax ValSeq ::= sortArraySpec(ValSeq) [function, total]
  rule sortArraySpec(VS:ValSeq)
    => sortKeyVS(sortVS(VS), popcountKeyClosure)

  syntax Bool ::= allNonNegativeInts(ValSeq) [function, total]
  rule allNonNegativeInts(.ValSeq) => true
  rule allNonNegativeInts(vCons(I:Int, REST:ValSeq))
    => I >=Int 0 andBool allNonNegativeInts(REST)
  rule allNonNegativeInts(vCons(_:Val, _:ValSeq)) => false [owise]
endmodule
